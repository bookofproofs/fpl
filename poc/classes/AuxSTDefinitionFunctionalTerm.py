from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTDefinitionFunctionalTerm(AuxSTBlock):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.block_def, parsing_info)
        self.def_type = AuxSymbolTable.functionalTerm
        self.id = ""
