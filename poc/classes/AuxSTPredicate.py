import z3
from anytree import AnyNode, search, PreOrderIter
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxEvaluationPredicate import AuxEvaluationPredicate
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTConstants import AuxSTConstants
from fplerror import FplPremiseNotSatisfiable


class AuxSTPredicate(AuxST, AuxInterfaceSTType, AuxEvaluationPredicate):

    def __init__(self, outline: str, i):
        super().__init__(outline, i)
        self._is_asserted = False
        self._is_revoked = False
        self._bound_vars_marked = False
        self.set_declared_type(InbuiltPredicate(self))

    def assert_predicate(self):
        self._is_asserted = True

    def revoke_predicate(self):
        self._is_asserted = False
        self._is_revoked = True

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        register = sem.eval_stack[-1]
        register.value = new_value
        if self._is_asserted:
            new_value.set_true()
            return
        elif self._is_revoked:
            new_value.set_false()
            return
        else:
            if self.outline == AuxSTConstants.predicate_true:
                new_value.set_true()
                new_value.set_expression(True)
                return
            elif self.outline == AuxSTConstants.predicate_false:
                new_value.set_false()
                new_value.set_expression(False)
                return
            elif self.outline == AuxSTConstants.predicate_negation:
                check = EvaluateParams.evaluate_recursion(sem, self.children[0], InbuiltPredicate(self.children[0]))
                new_value.set_expression(z3.Not(check.value.get_expression()))
                if check.evaluation_error:
                    new_value.set_undetermined()
                else:
                    new_value.set_to(not check.value.get_value())
                return
            elif self.outline == AuxSTConstants.predicate_conjunction:
                expressions, bool_values, errors = self.evaluate_children(sem)
                new_value.set_expression(z3.And(expressions))
                if True in errors:
                    new_value.set_undetermined()
                else:
                    ret = True
                    for bool_value in bool_values:
                        ret = ret and bool_value
                        if not ret:
                            break
                    new_value.set_to(ret)
                return
            elif self.outline == AuxSTConstants.predicate_disjunction:
                expressions, bool_values, errors = self.evaluate_children(sem)
                new_value.set_expression(z3.Or(expressions))
                if True in errors:
                    new_value.set_undetermined()
                else:
                    ret = False
                    for bool_value in bool_values:
                        ret = ret or bool_value
                        if ret:
                            break
                    new_value.set_to(ret)
                return
            elif self.outline == AuxSTConstants.predicate_equivalence:
                expressions, bool_values, errors = self.evaluate_children(sem)
                new_value.set_expression(expressions[0] == expressions[1])
                if True in errors:
                    new_value.set_undetermined()
                else:
                    new_value.set_to(bool_values[0] == bool_values[1])
                return
            elif self.outline == AuxSTConstants.predicate_exclusiveOr:
                expressions, bool_values, errors = self.evaluate_children(sem)
                new_value.set_expression(z3.Xor(expressions[0], expressions[1]))
                if True in errors:
                    new_value.set_undetermined()
                else:
                    new_value.set_to(bool_values[0] != bool_values[1])
                return
            elif self.outline == AuxSTConstants.predicate_implication:
                expressions, bool_values, errors = self.evaluate_children(sem)
                new_value.set_expression(z3.Implies(expressions[0], expressions[1]))
                if True in errors:
                    new_value.set_undetermined()
                else:
                    new_value.set_to(not bool_values[0] or bool_values[1])
                return
            elif self.outline == AuxSTConstants.intrinsic:
                # we set intrinsic predicates as being undetermined per default
                new_value.set_undetermined()
                new_value.set_expression(z3.Bool(self.get_long_id()))
                return
            elif self.outline == AuxSTConstants.predicate_all:
                new_value.set_expression(z3.Bool(self.get_long_id()))
                self._mark_bound_vars()
                p = EvaluateParams.evaluate_recursion(sem, self.children[0],
                                                      expected_type=InbuiltPredicate(self.children[0]))
                if p.evaluation_error:
                    new_value.set_undetermined()
                    return
                new_value.set_to(p.value.get_value())
                return
            elif self.outline == AuxSTConstants.predicate_exists:
                new_value.set_expression(z3.Bool(self.get_long_id()))
                self._mark_bound_vars()
                p = EvaluateParams.evaluate_recursion(sem, self.children[0],
                                                      expected_type=InbuiltPredicate(self.children[0]))
                if p.evaluation_error:
                    new_value.set_undetermined()
                    return
                new_value.set_to(p.value.get_value())
                return
            elif self.outline == AuxSTConstants.pre:
                new_value.set_expression(z3.Bool(self.get_long_id()))
                p = EvaluateParams.evaluate_recursion(sem, self.children[0],
                                                      expected_type=InbuiltPredicate(self.children[0]))
                if p.evaluation_error:
                    new_value.set_undetermined()
                elif not p.value.is_satisfiable():
                    sem.error_mgr.add_error(FplPremiseNotSatisfiable(self))
                    new_value.set_false()
                else:
                    # since the premise is satisfiable, we 'assume' it to be true for the theory to come
                    new_value.set_true()
            elif self.outline == AuxSTConstants.con:
                new_value.set_expression(z3.Bool(self.get_long_id()))
                p = EvaluateParams.evaluate_recursion(sem, self.children[0],
                                                      expected_type=InbuiltPredicate(self.children[0]))
                if p.evaluation_error:
                    new_value.set_undetermined()
                else:
                    new_value.set_to(p.value.get_value())
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

    def get_long_id(self):
        if self._long_id is None:
            if self.outline in [AuxSTConstants.extDigit, AuxSTConstants.ids, AuxSTConstants.variadic_var]:
                self._long_id = self.id + "."
            else:
                self._long_id = self.outline + "."
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
