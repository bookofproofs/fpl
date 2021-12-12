from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTType(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.type, parsing_info)
        self.id = ""
        self.type_pattern = -1
        self.type_mod = ""
        self._param_tuple = None

    def set_type(self, var_type):
        self.id = var_type.generalType.id
        self.type_mod = var_type.generalType.type_mod
        self.type_pattern = var_type.generalType.type_pattern
        self.info = var_type.get_ast_info()
        self._parsing_info = var_type

    def make(self):
        if self._param_tuple is not None:
            type_node = AuxSTType(self._parsing_info)
            type_node.parent=self
            for next_var_declaration in self._parsing_info.paramTuple.tuple:
                AuxSymbolTable.add_vars_to_node(type_node, next_var_declaration)

    def to_string(self):
        ret = self.id
        if len(self.children) > 0:
            ret += "["
            for child in self.children:
                ret += child.to_string()
            ret += "]"
        return ret
