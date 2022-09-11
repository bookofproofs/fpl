from anytree import search
from gid import Guid
from poc.fplerror import FplErrorManager
from poc.fplerror import FplVariableAlreadyDeclared
from poc.fplerror import FplTemplateMisused
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable

"""
The class AuxInstanceVariable stores the type and a list of occurrences of the variable inside a block.
"""


class AuxInstanceVariable:
    def __init__(self, occurrences: list, type_node):
        self.type_node = type_node.clone()
        self.occurrences = occurrences


"""
The class AuxNodeInstanceHandler simplifies the handling of building block instances. 
An instance is identified by a Guid and stores internally a dictionary of 
all instances of variables declared in the block by their name.
"""


class AuxNodeInstanceHandler(dict):
    def __init__(self):
        super().__init__()

    def add_instance(self):
        guid = Guid()
        self[str(guid)] = dict()
        return str(guid)

    def add_instance_variable(self, guid: Guid, var_id: str, occurrences: list, type_node):
        self[guid][var_id] = AuxInstanceVariable(occurrences, type_node)


class AuxSTBuildingBlock(AuxST):
    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self.id = ""
        self._relative_id = ""
        self._declared_vars = dict()
        self._used_vars = tuple()
        self._base_id = None
        # If the signature of the block has no parameters at all, the constant value
        # will be set after the evaluate method of the block will be called the very first time.
        # This is to prevent the block being re-evaluated each time whenever it is referred to in the FPL code.
        # The evaluate method will check if the static value is not None and simply return its value
        self._constant_value = None
        # instance_handler of variables declared for the block
        self._handler = AuxNodeInstanceHandler()
        self._main_guid = self._handler.add_instance()
        # a flag that will be set to True once the very first evaluation was used to enrich the self-containment graph
        self._sc_ready_flag = False

    def set_relative_id(self, name_of_parent: str):
        if name_of_parent == "":
            self._relative_id = self.id
        else:
            self._relative_id = ".".join([name_of_parent, self.id])

    def get_relative_id(self):
        return self._relative_id

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        """
         Initializes the declared variables of a building block and its used variables.
         This method might be overridden in derived classes by specific implementations.
         :return: None
         """
        # blocks's variable declarations
        _declared_vars_tuple = search.findall_by_attr(self, "var_decl", "outline")
        for var_declaration in _declared_vars_tuple:
            if var_declaration.id not in self._declared_vars:
                # set the scope of the variable
                var_declaration.initialize_scope(self.zto)
                # add the variable declaration into a dictionary for fast searching
                self._declared_vars[var_declaration.id] = var_declaration
            else:
                # we have a potential duplicate variable declaration
                self.append_variable_already_declared(var_declaration, error_mgr, filename)

        # blocks's used variables
        self._used_vars = search.findall_by_attr(self, "var", "outline")
        self.filter_misused_templates(error_mgr, filename)

    def filter_misused_templates(self, error_mgr, filename):
        result = filter(lambda x: not x.id.startswith("tpl"), self._used_vars)
        ok_vars = tuple(result)
        if len(ok_vars) < len(self._used_vars):
            for node in self._used_vars:
                if node.id.startswith("tpl"):
                    error_mgr.add_error(FplTemplateMisused(node.id, node.zfrom, filename))
                    # set the declared type of this var
                    node.set_declared_type(InbuiltUndefined(node))
        self._used_vars = ok_vars

    def append_variable_already_declared(self, var_declaration, error_mgr: FplErrorManager, filename):
        # In implicit declarations like a,b,c: BinOp(x,y: tpl)
        # The names "x,y" would create false positives of FplVariableAlreadyDeclared errors if only checking the
        # names x,y. Semantically, the above declaration means a.x, b.x, c.x, a.y, b.y, c.y, and there is no
        # conflict. To prevent these false positives, we also check if the name of the variables correlates
        # to its unique position in the source code.
        if str(var_declaration.zfrom) == str(self._declared_vars[var_declaration.id].zfrom):
            # ignore the false positive
            pass
        else:
            # we have a duplicate variable declaration
            error_mgr.add_error(
                FplVariableAlreadyDeclared(var_declaration.zfrom,
                                           self._declared_vars[var_declaration.id].zfrom,
                                           var_declaration.id,
                                           filename))

    def get_declared_vars(self):
        """
        A dictionary of all declared variables in the scope of the node
        (and possibly) all its relevant outer scopes.
        The keys are ids of the declared variables.
        The values are the AuxSTVarDec objects.
        :return: dictionary of declared variables in the building block
        """
        return self._declared_vars

    def get_used_vars(self):
        """
        A tuple of all used variables in the scope of the
        :return: tuple of used variables
        """
        return self._used_vars

    def get_node_type_str(self):
        d = str(type(self)).split(".")
        return d[-1][5:-2]

    def base_id(self):
        if self._base_id is None:
            irrelevant_prefix = ".".join(self.get_qualified_id().split(".")[0:-1])
            self._base_id = self.id[len(irrelevant_prefix):]
        return self._base_id

    def constant_value(self):
        return self._constant_value

    def set_constant_value(self, value):
        if self._constant_value is None:
            self._constant_value = value
        else:
            raise AssertionError("Constant value already set.")

    def add_var_to_main_instance(self, var_id: str, occurrences: list, type_node):
        self._handler.add_instance_variable(self._main_guid, var_id, occurrences, type_node)

    def clone_main_instance(self):
        guid = self._handler.add_instance()
        for var_id in self._handler[self._main_guid]:
            self._handler.add_instance_variable(guid, var_id,
                                                self._handler[self._main_guid][var_id].occurrences,
                                                self._handler[self._main_guid][var_id].type_node)
        return guid

    def clear_instance_handler(self):
        for guid in self._handler:
            # remove all but the main instance of the node
            if guid != self._main_guid:
                for var_id in self._handler[guid]:
                    self._handler[guid][var_id].occurrences.clear()
                    AuxSymbolTable.remove_node_recursively(self._handler[guid][var_id].type_node)
                self._handler[guid].clear
                del self._handler[guid]

    def get_instance(self, guid: str):
        return self._handler[guid]

    def get_main_instance(self):
        return self._handler[self._main_guid]

    def evaluate(self, sem):
        raise NotImplementedError(str(sem.eval_stack[-1].node))

    def is_sc_ready(self):
        return self._sc_ready_flag

    def set_sc_ready(self):
        self._sc_ready_flag = True
