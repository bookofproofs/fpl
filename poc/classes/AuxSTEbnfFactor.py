from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTEbnfFactor(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.ebnf_factor, i)
