import z3
from anytree import AnyNode, search, PreOrderIter
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate, EvaluatedPredicate
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxPredicateState import AuxPredicateState
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTConstants import AuxSTConstants
from fplerror import FplPremiseNotSatisfiable


class AuxSTPredicate(AuxST):

    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self._predicate_state = AuxPredicateState(self)
        self._is_asserted = False
        self._is_revoked = False
        self._bound_vars_marked = False
        self.set_declared_type(InbuiltPredicate(self))

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
            sem.eval_stack[-1].value = EvaluatedPredicate(self, True)
            return
        elif self._is_revoked:
            sem.eval_stack[-1].value = EvaluatedPredicate(self, False)
            return
        else:
            if self.outline == AuxSTConstants.predicate_true:
                sem.eval_stack[-1].value = EvaluatedPredicate(self, True)
                return
            elif self.outline == AuxSTConstants.predicate_false:
                sem.eval_stack[-1].value = EvaluatedPredicate(self, False)
                return
            elif self.outline == AuxSTConstants.predicate_negation:
                check = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if check.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                else:
                    sem.eval_stack[-1].value = EvaluatedPredicate(self, not check.returned_value.get_repr())
                return
            elif self.outline == AuxSTConstants.predicate_conjunction:
                ret = True
                for child in self.children:
                    check = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate(child))
                    if check.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined(self)
                        return
                    else:
                        ret = ret and check.returned_value.get_repr()
                    if not ret:
                        # stop further conjunction with False
                        break
                sem.eval_stack[-1].value = EvaluatedPredicate(self, ret)
                return
            elif self.outline == AuxSTConstants.predicate_disjunction:
                ret = False
                for child in self.children:
                    check = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate(child))
                    if check.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined(self)
                        return
                    else:
                        ret = ret or check.returned_value.get_repr()
                    if ret:
                        # stop further disjunction with True
                        break
                sem.eval_stack[-1].value = EvaluatedPredicate(self, ret)
                return
            elif self.outline == AuxSTConstants.predicate_equivalence:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], InbuiltPredicate(self.children[1]))
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(self,
                                                              p.returned_value.get_repr() == q.returned_value.get_repr())
                return
            elif self.outline == AuxSTConstants.predicate_exclusiveOr:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], InbuiltPredicate(self.children[1]))
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(self,
                                                              (
                                                                      p.returned_value.get_repr() and not q.returned_value.get_repr()) or
                                                              (
                                                                      q.returned_value.get_repr() and not p.returned_value.get_repr()))
                return
            elif self.outline == AuxSTConstants.predicate_implication:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                q = EvaluateParams.evaluate_recursion(sem, self.children[1], InbuiltPredicate(self.children[1]))
                if q.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(self,
                                                              not p.returned_value.get_repr() or q.returned_value.get_repr())
                return
            elif self.outline == AuxSTConstants.intrinsic:
                # we set intrinsic predicates as being True per default
                sem.eval_stack[-1].value = EvaluatedPredicate(self, True)
                return
            elif self.outline == AuxSTConstants.predicate_all:
                self._mark_bound_vars()
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(self, p.returned_value.get_repr())
                return
            elif self.outline == AuxSTConstants.predicate_exists:
                self._mark_bound_vars()
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                    return
                sem.eval_stack[-1].value = EvaluatedPredicate(self, p.returned_value.get_repr())
                return
            elif self.outline == AuxSTConstants.pre:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                elif not self.check_satisfiability():
                    sem.error_mgr.add_error(FplPremiseNotSatisfiable(self))
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                else:
                    # since the premise is satisfiable, we 'assume' it to be true for the theory to come
                    sem.eval_stack[-1].value = EvaluatedPredicate(self, True)
            elif self.outline == AuxSTConstants.con:
                p = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                if p.returned_value is None:
                    sem.eval_stack[-1].value = InbuiltUndefined(self)
                else:
                    sem.eval_stack[-1].value = EvaluatedPredicate(self, p.returned_value.get_repr())
            elif self.outline == AuxSTConstants.undefined:
                # the syntax allows it, but not the semantics
                sem.eval_stack[-1].value = InbuiltUndefined(self)
            elif self.outline == AuxSTConstants.ids:
                # the syntax allows it, but not the semantics
                sem.eval_stack[-1].value = InbuiltUndefined(self)
            else:
                raise NotImplementedError(self.outline)

    def clone(self):
        return self._copy(AuxSTPredicate(self.outline, self._i))

    def _mark_bound_vars(self):
        """
        In case this predicate is an exist or an all quantor, this method will
        marks in the symbol table the variables bound by it inside the block of this quantor.
        For performance reasons, an auxiliary variable self._bound_vars_marked is used to prevent
        repeating this single time job when reevaluating the quantor during the semantical analysis.
        :return: None
        """
        if not self._bound_vars_marked:
            for var_name in self.bound_vars:
                occurs = search.findall(self, lambda node: isinstance(node, AuxSTVariable) and node.id == var_name)
                for var in occurs:
                    var.set_is_bound()
            self._bound_vars_marked = True

    def check_satisfiability(self):
        """
        This method checks if the current predicate is satisfiable.
        :return: True if this AuxSTPredicate is satisfiable, False if not
        """
        return self._predicate_state.is_satisfiable()

    def get_state(self):
        return self._predicate_state

    def get_long_id(self):
        if self._long_id is None:
            if self.outline in [AuxSTConstants.extDigit, AuxSTConstants.ids, AuxSTConstants.variadic_var]:
                self._long_id = self.id
            else:
                self._long_id = self.outline
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def get_used_vars(self):
        """
        Get a list of all variables used in this predicate in the pre-order of their occurrence in the symbol table
        :return: a list of these variables
        """
        return list(n for n in PreOrderIter(self, filter_=lambda n1: isinstance(n1, AuxSTVariable)))

    def get_used_var_names_set(self):
        """
        Get a set of all variable names used in this predicate
        :return: a set of these variable names
        """
        used_vars = self.get_used_vars()
        s = set()
        for var in used_vars:
            if var.id not in s:
                s.add(var.id)
        return s
