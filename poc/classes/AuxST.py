from poc.classes.AuxSTOutline import AuxSTOutline


class AuxST(AuxSTOutline):
    """
    A class for outline elements of the symbol table that have an ast_info and errors
    """

    def __init__(self, outline: str, i):
        super().__init__(parent=None, outline=outline)  # noqa
        self._i = i
        if self._i is not None:
            self._error_mgr = i.errors
        self.zto = ""
        self.zfrom = ""
        self._qualified_id = None

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
        instance._copied_path = self.path
        instance._i = self._i
        instance._error_mgr = self._error_mgr
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = instance
        return instance


