from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTArgumentParam(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.arg_id, i)
        self.id = ""
        self.zto = i.last_positions_by_rule['ArgumentParam'].pos_to_str()
        self.zfrom = i.corrected_position('ArgumentIdentifier')

    def clone(self):
        other = self._copy(AuxSTArgumentParam(self._i))
        other.id = self.id
        return other
