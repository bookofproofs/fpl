from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTStatement(AuxST):

    def __init__(self, statement_type: str, parsing_info):
        super().__init__(AuxSymbolTable.statement, parsing_info)
        self.type = statement_type

