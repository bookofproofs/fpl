from poc.classes.AuxST import AuxST


class AuxSTVarDec(AuxST):

    def __init__(self, i):
        super().__init__("var_decl", i)
        self.id = ""
        self.type_pattern = None
        self.type_mod = None
        self.type = None
        self.zto = ""
        self.zfrom = ""
