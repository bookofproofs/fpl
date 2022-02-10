from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTArgs(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.arg_list, i)
        self.zto = i.last_positions_by_rule['RightParen'].pos_to_str()
        self.zfrom = i.last_positions_by_rule['LeftParen'].pos_to_str()

    def clone(self):
        return self._copy(AuxSTArgs(self._i))
