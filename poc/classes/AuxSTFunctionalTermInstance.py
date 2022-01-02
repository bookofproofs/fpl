from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTFunctionalTermInstance(AuxSTInstance):

    def __init__(self, i):
        super().__init__(i)
        self.def_type = AuxSymbolTable.functionalTermInstance
        self.zfrom = i.corrected_position('FunctionalTermHeader')
        self.zto = i.last_positions_by_rule['FunctionalTermInstance'].pos_to_str()
        self.keyword = ""


