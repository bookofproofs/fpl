from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTDefinitionPredicate(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_def, i)
        self.def_type = AuxSymbolTable.predicateDeclaration
        self.id = ""
        self.zfrom = i.corrected_position('PredicateHeader')
        self.zto = i.last_positions_by_rule['DefinitionPredicate'].pos_to_str()
