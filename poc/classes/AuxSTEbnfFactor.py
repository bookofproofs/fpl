from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTEbnfFactor(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.ebnf_factor, i)
