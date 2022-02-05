from poc.classes.AuxST import AuxST


class AuxSTArgs(AuxST):

    def __init__(self, i):
        super().__init__("arguments", i)
        self.zto = i.last_positions_by_rule['RightParen'].pos_to_str()
        self.zfrom = i.last_positions_by_rule['LeftParen'].pos_to_str()

    def clone(self):
        return self._copy(AuxSTArgs(self._i))
