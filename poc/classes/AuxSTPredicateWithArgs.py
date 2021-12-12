from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.predicate_with_arguments, parsing_info)
        self.reference = None
