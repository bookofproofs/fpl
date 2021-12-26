from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTFunctionalTermInstance(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.property, i)
        self.def_type = AuxSymbolTable.functionalTerm
        self.zfrom = i.corrected_position('FunctionalTermHeader')
        self.zto = i.last_positions_by_rule['FunctionalTermInstance'].pos_to_str()
        self.keyword = ""
        self.mandatory = False


