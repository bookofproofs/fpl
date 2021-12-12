from poc.classes.AuxST import AuxST


class AuxSTVarDec(AuxST):

    def __init__(self, parsing_info):
        super().__init__("var_dec", parsing_info)
        self.id = ""
        self.type_pattern = None
        self.type_mod = None
        self.type = None
