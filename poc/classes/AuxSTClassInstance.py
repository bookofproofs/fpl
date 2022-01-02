from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTClassInstance(AuxSTInstance):

    def __init__(self, i):
        super().__init__(i)
        self.def_type = AuxSymbolTable.classInstance
        self.zfrom = i.corrected_position('VariableType')
        self.zto = i.last_positions_by_rule['ClassInstance'].pos_to_str()
