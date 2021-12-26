from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTUsedTheory(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.used, i)
        self.modifier = None
        self.zfrom = i.corrected_position('NamespaceIdentifier')
        self.zto = i.last_positions_by_rule['WildcardTheoryNamespace'].pos_to_str()

