from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
        self.reference = None
        self._signature_correct = None  # None=>never checked, False=>wrong, True=>correct

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateWithArgs(self._i))
        new_predicate.id = self.id
        new_predicate.outline = self.outline
        new_predicate._signature_correct = self._signature_correct
        new_predicate.reference = self.reference
        return new_predicate

    def get_type_signature(self):
        return self.reference.get_type_signature()

    def type_signature_correct(self):
        return self._signature_correct

    def set_type_signature_correctness(self, correct):
        self._signature_correct = correct
