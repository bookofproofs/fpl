from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTEbnfTerm(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.ebnf_term, i)
