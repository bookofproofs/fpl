from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTArgumentParam(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.arg_id, i)
        self.id = ""
        self.zto = i.last_positions_by_rule['ArgumentParam'].pos_to_str()
        self.zfrom = i.corrected_position('ArgumentIdentifier')

    def clone(self):
        other = AuxSTArgumentParam(self._i)
        other.id = self.id
        other.zto = self.zto
        other.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other