from anytree import AnyNode


class AuxSTOutline(AnyNode):
    """
    A class for elements of the symbol table of the FPL interpreter that have an an outline
    """

    def __init__(self, parent: AnyNode, outline: str):
        super().__init__()
        self.outline = outline
        self.parent = parent


class AuxST(AuxSTOutline):
    """
    A class for outline elements of the symbol table of the FPL interpreter that have an ast_info and errors
    """

    def __init__(self, outline: str, parsing_info):
        super().__init__(parent=None, outline=outline)
        self._errors = parsing_info.get_errors()
        self.info = parsing_info.get_ast_info()

    def register_child(self, node: AuxSTOutline):
        if not issubclass(type(node), AuxSTOutline):
            raise TypeError("Argument type was {0}, must be derived from AuxSTOutline".format(str(type(node))))
        node.parent = self

    def get_errors(self):
        return self._errors


class AuxSTBlock(AuxST):
    def __init__(self, outline: str, parsing_info):
        super().__init__(outline=outline, parsing_info=parsing_info)
        self.id = ""
        self._relative_id = ""

    def set_relative_id(self, name_of_parent: str):
        if name_of_parent == "":
            self._relative_id = self.id
        else:
            self._relative_id = ".".join([name_of_parent, self.id])

    def get_relative_id(self):
        return self._relative_id
