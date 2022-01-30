from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTArgs(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.arg_list, i)
        self.zto = i.last_positions_by_rule['RightParen'].pos_to_str()
        self.zfrom = i.last_positions_by_rule['LeftParen'].pos_to_str()

    def to_string(self):
        ret = "args["
        for child in self.children:
            ret += child.to_string()
        ret += "]"
        return ret

    def clone(self):
        other = AuxSTArgs(self._i)
        other.zto = self.zto
        other.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other
