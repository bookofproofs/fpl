from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTDefinitionFunctionalTerm(AuxSTBlockWithSignature):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_def, i)
        self.def_type = AuxSymbolTable.functionalTerm
        self.zfrom = i.corrected_position('FunctionalTermHeader')
        self.zto = i.last_positions_by_rule['DefinitionFunctionalTerm'].pos_to_str()