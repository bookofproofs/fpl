from anytree import AnyNode
import re
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTOutline(AnyNode):
    """
    A class for elements of the symbol table of the FPL transformer that have an an outline
    """

    def __init__(self, parent: AnyNode, outline: str):
        super().__init__()
        self.outline = outline
        self.parent = parent
        self._declared_type = None

    def set_declared_type(self, type_node):
        self._declared_type = type_node

    def get_declared_type(self):
        return self._declared_type


class AuxST(AuxSTOutline):
    """
    A class for outline elements of the symbol table of the FPL transformer that have an ast_info and errors
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
        instance._declared_type = self._declared_type
        instance._i = self._i
        instance._error_mgr = self._error_mgr
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = instance
        return instance

    def get_qualified_id(self):
        if self._qualified_id is None:
            self._qualified_id = re.sub(AuxSTConstants.qualified_re, "", self.id)
        return self._qualified_id

