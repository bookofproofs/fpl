from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTCorollary(AuxSTBlock):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.block_cor, parsing_info)
