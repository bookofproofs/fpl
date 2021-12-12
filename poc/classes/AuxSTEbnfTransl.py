from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTEbnfTransl(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.ebnf_transl, parsing_info)
