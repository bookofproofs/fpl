from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTArgs import AuxSTArgs


class AuxSTType(AuxST):

    def __init__(self, i):
        super().__init__("type", i)
        self.id = ""
        self.type_pattern = -1
        self.type_mod = ""
        self._parsing_info = None

    def set_type(self, var_type):
        if var_type.generalType is not None:
            self.id = var_type.generalType.id
            self.type_mod = var_type.generalType.type_mod
            self.type_pattern = var_type.generalType.type_pattern
            self.zfrom = var_type.generalType.zfrom
            self.zto = var_type.generalType.zto
        self._parsing_info = var_type

    def make(self):
        if self._parsing_info.paramTuple is not None:
            type_node = AuxSTType(self._i)
            type_node = type_node.clone()
            type_node.parent = self
            for next_var_declaration in self._parsing_info.paramTuple.tuple:
                AuxSymbolTable.add_vars_to_node(self._i, type_node, next_var_declaration)

    def to_string(self):
        ret = self.id
        if len(self.children) > 0:
            for child in self.children:
                ret += child.to_string()
        return ret

    def clone(self):
        other = self._copy(AuxSTType(self._i))
        if self.type_pattern == -1:
            # prevent cloning type when, in fact the type has params.
            # In this case replace the node by an AuxSTArgs node
            args = AuxSTArgs(self._i)
            # but make sure it has the same children as the cloned type
            args.children = other.children
            return args
        else:
            other.id = self.id
            other.type_mod = self.type_mod
            other.type_pattern = self.type_pattern
            other._parsing_info = self._parsing_info
            return other
