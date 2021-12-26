from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTType(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.type, i)
        self.id = ""
        self.type_pattern = -1
        self.type_mod = ""
        self._param_tuple = None
        self._parsing_info = None
        if "VariableType" in i.last_positions_by_rule:
            self.zfrom = i.corrected_position('GeneralType')
            self.zto = i.last_positions_by_rule['VariableType'].pos_to_str()
        elif "GeneralType" in i.last_positions_by_rule:
            self.zfrom = i.corrected_position('Type')
            self.zto = i.last_positions_by_rule['GeneralType'].pos_to_str()
        elif "Type" in i.last_positions_by_rule:
            self.zto = i.last_positions_by_rule['Type'].pos_to_str()
            self.zfrom = i.last_positions_by_rule['Type'].pos_to_str()

    def set_type(self, var_type):
        self.id = var_type.generalType.id
        self.type_mod = var_type.generalType.type_mod
        self.type_pattern = var_type.generalType.type_pattern
        self._parsing_info = var_type

    def make(self):
        if self._param_tuple is not None:
            type_node = AuxSTType(self._parsing_info)
            type_node.parent = self
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
