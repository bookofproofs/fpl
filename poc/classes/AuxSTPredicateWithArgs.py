from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
        self.reference = None
        self.zto = i.last_positions_by_rule['PredicateWithArguments'].pos_to_str()
        self.zfrom = i.corrected_position('Identifier')

    def clone(self):
        other = AuxSTPredicateWithArgs(self._i)
        other.zto = self.zto
        other.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other

