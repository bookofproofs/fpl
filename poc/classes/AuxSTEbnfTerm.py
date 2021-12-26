from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTEbnfTerm(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.ebnf_term, i)
