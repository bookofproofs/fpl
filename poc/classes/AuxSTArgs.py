from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTArgs(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.arg_list, i)
        self.zto = i.last_positions_by_rule['RightParen'].pos_to_str()
        self.zfrom = i.last_positions_by_rule['LeftParen'].pos_to_str()

    def clone(self):
        return self._copy(AuxSTArgs(self._i))

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = "("
            for arg in self.children:
                self._long_id += arg.get_long_id()
            self._long_id += ")"
        return self._long_id
