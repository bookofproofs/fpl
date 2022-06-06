from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs



class AuxSTQualified(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.qualified, i)
        # the resolved_parent is the node in the symbol table that can possibly be identified
        # during the semantic analysis
        self._resolved_parent = None

    def to_string(self):
        ret = "dot["
        for child in self.children:
            ret += child.to_string()
        ret += "]"
        return ret

    def clone(self):
        my_copy = self._copy(AuxSTQualified(self._i))
        my_copy._resolved_parent = self._resolved_parent
        return my_copy

