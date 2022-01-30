from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTSelf(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.selfInstance, i)
        self.reference = None
        self.number_ats = 0
        self.id = AuxSymbolTable.selfInstance
        self.zto = i.last_positions_by_rule['self'].pos_to_str()
        self.zfrom = i.corrected_position('self')

    def to_string(self):
        ret = "@" * self.number_ats + "self"
        for child in self.children:
            ret += child.to_string()
        return ret

    def clone(self):
        other = AuxSTSelf(self._i)
        other.number_ats = self.number_ats
        other.id = self.id
        other.zto = self.zto
        other.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other

