from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTConjecture(AuxSTBlock):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.block_conj, parsing_info)
