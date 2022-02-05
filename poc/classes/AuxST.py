from anytree import AnyNode


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
        self._errors = i.errors
        self.zto = ""
        self.zfrom = ""

    def register_child(self, node: AuxSTOutline):
        if not issubclass(type(node), AuxSTOutline):
            raise TypeError("Argument type was {0}, must be derived from AuxSTOutline".format(str(type(node))))
        node.parent = self

    def get_errors(self):
        return self._errors

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

    def set_relative_id(self, name_of_parent: str):
        if name_of_parent == "":
            self._relative_id = self.id
        else:
            self._relative_id = ".".join([name_of_parent, self.id])

    def get_relative_id(self):
        return self._relative_id
