from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTClassInstance(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.property, i)
        self.def_type = AuxSymbolTable.classProperty
        self.zfrom = i.corrected_position('VariableType')
        self.zto = i.last_positions_by_rule['ClassInstance'].pos_to_str()
        self.mandatory = False