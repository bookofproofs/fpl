from anytree import AnyNode
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate, EvaluatedPredicate
from poc.classes.AuxEvaluation import EvaluateParams
from fplerror import FplPremiseNotSatisfiable


class AuxSTPredicate(AuxST):

    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self._is_asserted = False
        self._is_revoked = False
        self.set_declared_type(InbuiltPredicate())

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
            sem.eval_stack[-1].value = EvaluatedPredicate(True)
            return
        elif self._is_revoked:
            sem.eval_stack[-1].value = EvaluatedPredicate(False)
            return
        else:
            if self.outline == AuxSymbolTable.predicate_true:
                sem.eval_stack[-1].value = EvaluatedPredicate(True)
                return
            elif self.outline == AuxSymbolTable.predicate_false:
                sem.eval_stack[-1].value = EvaluatedPredicate(False)
                return
            elif self.outline == AuxSymbolTable.predicate_negation:
                check = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if check.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                else:
                    sem.eval_stack[-1].value = EvaluatedPredicate(not check.returned_value.get_repr())
                return
            elif self.outline == AuxSymbolTable.predicate_conjunction:
                ret = True
                for child in self.children:
                    check = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate())
                    if check.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                        return
                    else:
                        ret = ret and check.returned_value.get_repr()
                    if not ret:
                        # stop further conjunction with False
                        break
                sem.eval_stack[-1].value = EvaluatedPredicate(ret)
                return
            elif self.outline == AuxSymbolTable.predicate_disjunction:
                ret = False
                for child in self.children:
                    check = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate())
                    if check.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                        return
                    else:
                        ret = ret or check.returned_value.get_repr()
                    if ret:
                        # stop further disjunction with True
                        break
                sem.eval_stack[-1].value = EvaluatedPredicate(ret)
                return
            elif self.outline == AuxSymbolTable.predicate_equivalence:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], InbuiltPredicate())
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(
                    p.returned_value.get_repr() == q.returned_value.get_repr())
                return
            elif self.outline == AuxSymbolTable.predicate_exclusiveOr:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], InbuiltPredicate())
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(
                    (p.returned_value.get_repr() and not q.returned_value.get_repr()) or
                    (q.returned_value.get_repr() and not p.returned_value.get_repr()))
                return
            elif self.outline == AuxSymbolTable.predicate_implication:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], InbuiltPredicate())
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(
                    not p.returned_value.get_repr() or q.returned_value.get_repr())
                return
            elif self.outline == AuxSymbolTable.intrinsic:
                # we set intrinsic predicates as being True per default
                sem.eval_stack[-1].value = EvaluatedPredicate(True)
                return
            elif self.outline == AuxSymbolTable.predicate_all:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(p.returned_value.get_repr())
                return
            elif self.outline == AuxSymbolTable.pre:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                elif not p.returned_value.get_repr():
                    sem.analyzer.error_mgr.add_error(FplPremiseNotSatisfiable(self))
                    sem.eval_stack[-1].value = InbuiltUndefined()
                else:
                    # since the premise is satisfiable, we 'assume' it to be true for the theory to come
                    sem.eval_stack[-1].value = EvaluatedPredicate(True)
            elif self.outline == AuxSymbolTable.con:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate())
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined()
                else:
                    sem.eval_stack[-1].value = EvaluatedPredicate(p.returned_value.get_repr())
            elif self.outline == AuxSymbolTable.undefined:
                # the syntax allows it, but not the semantics
                sem.eval_stack[-1].value = InbuiltUndefined()
            elif self.outline == AuxSymbolTable.ids:
                # the syntax allows it, but not the semantics
                sem.eval_stack[-1].value = InbuiltUndefined()
            else:
                raise NotImplementedError(self.outline)

    def clone(self):
        return self._copy(AuxSTPredicate(self.outline, self._i))
