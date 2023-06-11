from anytree import search
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxParamsArgsMatcher import AuxParamsArgsMatcher
from poc.classes.AuxSTBuildingBlockInstanceHandlers import AuxSTBuildingBlockInstanceHandlers
from poc.classes.AuxSTWithId import AuxSTWithId
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplErrorManager, FplVariableAlreadyDeclared, FplTemplateMisused

"""
The class AuxSTBuildingBlock is a base class for all FPL building blocks
"""


class AuxSTBuildingBlock(AuxSTWithId, AuxInterfaceSTType):
    def __init__(self, outline: str, i):
        AuxInterfaceSTType.__init__(self)
        AuxSTWithId.__init__(self, outline, i)
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
        # instance handlers for the block
        self._handlers = AuxSTBuildingBlockInstanceHandlers()
        # a flag that will be set to True once the very first evaluation was used to enrich the self-containment graph
        self._sc_ready_flag = False
        self._next_input_arguments = None

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
        _declared_vars_tuple = search.findall_by_attr(self, AuxSTConstants.var_decl, AuxSTConstants.outline)
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
        self._handlers.main_instance.add_instance_variable(var_id, occurrences, type_node)

    def clone_main_instance(self):
        instance_clone = self._handlers.add_instance()
        main_instance_vars = self._handlers.main_instance.get_vars()
        for var_id in main_instance_vars:
            instance_clone.add_instance_variable(var_id,
                                                 main_instance_vars[var_id].occurrences,
                                                 main_instance_vars[var_id].type_node)
        return instance_clone

    def get_instance(self, guid: str):
        return self._handlers[guid]

    def remove_instance(self, guid):
        instance = self.get_instance(guid)
        instance.clear_instance()
        del self._handlers[guid]

    def get_main_instance(self):
        return self._handlers.main_instance

    def is_sc_ready(self):
        return self._sc_ready_flag

    def set_sc_ready(self):
        self._sc_ready_flag = True

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
        return self._long_id

    def arguments_match(self, evaluated_arguments):
        signature_node = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.signature)
        matcher = AuxParamsArgsMatcher()
        match_successful = matcher.try_match(evaluated_arguments, list(signature_node.children))
        if match_successful:
            self._set_next_input_arguments(evaluated_arguments)
        else:
            if self._next_input_arguments is not None:
                self._next_input_arguments.clear()
            self._next_input_arguments = None
        return match_successful

    def _set_next_input_arguments(self, evaluated_arguments):
        self._next_input_arguments = evaluated_arguments

    def get_input_arguments(self):
        return self._next_input_arguments

    def get_signature_types(self):
        signature_node = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.signature)
        signature_types = list()
        if signature_node is not None:
            for child in signature_node.children:
                signature_types.append(child.children[0].to_string2())
        else:
            return AuxSTConstants.classDeclaration
        return str(signature_types)
