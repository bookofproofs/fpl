from anytree import AnyNode
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxEvaluation import EvaluateParams


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

    def evaluate(self, sem):
        if self._is_asserted:
            sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
            sem.eval_stack[-1].value = True
            return
        elif self._is_revoked:
            sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
            sem.eval_stack[-1].value = False
            return
        else:
            if self.outline == AuxSymbolTable.predicate_true:
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                sem.eval_stack[-1].value = True
                return
            elif self.outline == AuxSymbolTable.predicate_false:
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                sem.eval_stack[-1].value = False
                return
            elif self.outline == AuxSymbolTable.predicate_negation:
                check = EvaluateParams.evaluate_recursion(sem, self.children[0], AuxSymbolTable.predicate)
                if check.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                else:
                    sem.eval_stack[-1].value = not check.returned_value
                    sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            elif self.outline == AuxSymbolTable.predicate_conjunction:
                ret = True
                for child in self.children:
                    check = EvaluateParams.evaluate_recursion(sem, child, AuxSymbolTable.predicate)
                    if check.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                        return
                    else:
                        ret = ret and check.returned_value
                    if not ret:
                        # stop further conjunction with False
                        break
                EvaluateParams.propagate(sem, check)
                sem.eval_stack[-1].value = ret
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            elif self.outline == AuxSymbolTable.predicate_disjunction:
                ret = False
                for child in self.children:
                    check = EvaluateParams.evaluate_recursion(sem, child, AuxSymbolTable.predicate)
                    if check.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                        return
                    else:
                        ret = ret or check.returned_value
                    if ret:
                        # stop further disjunction with True
                        break
                sem.eval_stack[-1].value = ret
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            elif self.outline == AuxSymbolTable.predicate_equivalence:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], AuxSymbolTable.predicate)
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], AuxSymbolTable.predicate)
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = p.returned_value == q.returned_value
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            elif self.outline == AuxSymbolTable.predicate_exclusiveOr:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], AuxSymbolTable.predicate)
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], AuxSymbolTable.predicate)
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = (p.returned_value and not q.returned_value) or (
                            q.returned_value and not p.returned_value)
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            elif self.outline == AuxSymbolTable.predicate_implication:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], AuxSymbolTable.predicate)
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], AuxSymbolTable.predicate)
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = not p.returned_value or q.returned_value
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            elif self.outline == AuxSymbolTable.intrinsic:
                # we set intrinsic predicates as being True per default
                sem.eval_stack[-1].value = True
                sem.eval_stack[-1].actual_type = AuxSymbolTable.predicate
                return
            else:
                raise NotImplementedError(self.outline)

    def clone(self):
        return self._copy(AuxSTPredicate(self.outline, self._i))

    def get_type_signature(self):  # noqa
        return AuxSymbolTable.predicate
