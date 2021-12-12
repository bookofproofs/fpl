from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTClassInstance(AuxSTBlock):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.property, parsing_info)
        self.def_type = AuxSymbolTable.classProperty

