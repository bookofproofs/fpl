from classes.AuxInterpretation import AuxInterpretation


class Type(AuxInterpretation):
    isTemplate = False

    def __init__(self, inter: AuxInterpretation):
        self.clone(inter)
        self.isTemplate = False
        cst = inter.get_cst()
        if type(cst) is tuple and (cst[0] == 'template' or cst[0] == 'tpl') and len(cst) == 2:
            self.set_interpretation(cst[0] + cst[1])
            self.isTemplate = True
        else:
            self.set_interpretation(cst)
