from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTEbnfFactor(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.ebnf_factor, parsing_info)
