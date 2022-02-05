from poc.classes.AuxST import AuxST


class AuxSTVarDec(AuxST):

    def __init__(self, i):
        super().__init__("var_decl", i)

    def clone(self):
        other = self._copy(AuxSTVarDec(self._i))
        other.id = self.id
        return other
