from anytree import AnyNode
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicate(AuxST):

    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self._is_asserted = False
        self._is_revoked = False

    def set_id(self, identifier: str):
        self.id = identifier  # noqa

    def assert_predicate(self):
        self._is_asserted = True

    def revoke_predicate(self):
        self._is_asserted = False
        self._is_revoked = True

    def register_reference(self, reference: AnyNode):
        self.reference = reference  # noqa

    def evaluate(self):
        if self._is_asserted:
            return True
        elif self._is_revoked:
            return False
        else:
            if self.outline == AuxSymbolTable.predicate_true:
                return True
            elif self.outline == AuxSymbolTable.predicate_false:
                return False
            elif self.outline == AuxSymbolTable.predicate_negation:
                return not self.children[0].evaluate()
            elif self.outline == AuxSymbolTable.predicate_conjunction:
                ret = True
                for child in self.children:
                    ret = ret and child.evaluate()
                    if not ret:
                        break
                return ret
            elif self.outline == AuxSymbolTable.predicate_disjunction:
                ret = False
                for child in self.children:
                    ret = ret or child.evaluate()
                    if ret:
                        break
                return ret
            elif self.outline == AuxSymbolTable.predicate_equivalence:
                p = self.children[0].evaluate()
                q = self.children[1].evaluate()
                return p == q
            elif self.outline == AuxSymbolTable.predicate_exclusiveOr:
                p = self.children[0].evaluate()
                q = self.children[1].evaluate()
                return (p and not q) or (q and not p)
            elif self.outline == AuxSymbolTable.predicate_implication:
                p = self.children[0].evaluate()
                q = self.children[1].evaluate()
                return not p or q
            else:
                raise NotImplementedError(self.outline)

    def clone(self):
        return self._copy(AuxSTPredicate(self.outline, self._i))
