from anytree import AnyNode, search
from poc.fplerror import FplErrorManager
from poc.fplerror import FplVariableAlreadyDeclared
from poc.fplerror import FplTemplateMisused


class AuxSTOutline(AnyNode):
    """
    A class for elements of the symbol table of the FPL transformer that have an an outline
    """

    def __init__(self, parent: AnyNode, outline: str):
        super().__init__()
        self.outline = outline
        self.parent = parent


class AuxST(AuxSTOutline):
    """
    A class for outline elements of the symbol table of the FPL transformer that have an ast_info and errors
    """

    def __init__(self, outline: str, i):
        super().__init__(parent=None, outline=outline)  # noqa
        self._i = i
        self._error_mgr = i.errors
        self.zto = ""
        self.zfrom = ""

    def register_child(self, node: AuxSTOutline):
        if not issubclass(type(node), AuxSTOutline):
            raise TypeError("Argument type was {0}, must be derived from AuxSTOutline".format(str(type(node))))
        node.parent = self

    def get_error_mgr(self):
        return self._error_mgr

    def to_string(self):
        return ""

    def _copy(self, instance):
        instance.zto = self.zto
        instance.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = instance
        return instance


class AuxSTBlock(AuxST):
    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self.id = ""
        self._relative_id = ""
        self._declared_vars = dict()
        self._used_vars = tuple()

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
