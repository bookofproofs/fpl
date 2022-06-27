from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTRuleOfInference(AuxSTBlockWithSignature):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_ir, i)
        self.zfrom = i.last_positions_by_rule['PredicateIdentifier'].pos_to_str()
        self.zto = i.last_positions_by_rule['RuleOfInference'].pos_to_str()

    def evaluate(self, sem):
        raise NotImplementedError()
