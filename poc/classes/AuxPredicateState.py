import z3
from poc.classes.AuxSTConstants import AuxSTConstants

"""
The class AuxPredicateState provides and administers the states of FPL predicates (AuxSTPredicate)
that can occur during their evaluation process. The results of the evaluation might interfere with the state of
the predicate.
"""


class AuxPredicateState:

    def __init__(self, parent):
        self._parent_with_this_state = parent
        # first state ever
        self._initial = 0
        # the predicate is formally incorrect, e.g. it binds variables that ar already bound
        self._formallyIncorrect = 1
        # the predicate is formally correct
        self._formallyCorrect = 2
        # the predicate is unsatisfiable
        self._satisfiability_check_done = 4
        # the predicate is satisfiable
        self._satisfiable = 50
        self._model = None
        # the predicate was asserted, e.g. in an axiom, a premise, or via the FPL assert statement
        self._asserted = 60
        # the predicate was assumed via the FPL assume statement
        self._assumed = 70
        # the predicate was assumed via the FPL revoke statement
        self._revoked = 80
        # the predicate is being checked for satisfaction
        self._questioned = 90
        # the predicate is was checked for satisfaction
        self._answered = 100
        # set the current state to initial
        self.current = self._initial
        self.expression = None
        self.block_node = None
        self.block_instance = None

    def initialize(self):
        if self.current != self._initial:
            return
        else:
            self.block_node = self._parent_with_this_state.get_scope()
            self.block_instance = self.block_node.get_main_instance()
            self._construct_expression()

    def _construct_expression(self):
        if self._parent_with_this_state.outline == AuxSTConstants.predicate_false:
            self.expression = False
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_true:
            self.expression = True
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_negation:
            args = self._gather_children()
            self.expression = z3.Not(args[0])
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_disjunction:
            self.expression = z3.Or(self._gather_children())
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_conjunction:
            self.expression = z3.And(self._gather_children())
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_equivalence:
            args = self._gather_children()
            self.expression = args[0] == args[1]
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_exclusiveOr:
            args = self._gather_children()
            self.expression = z3.Xor(args[0], args[1])
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_implication:
            args = self._gather_children()
            self.expression = z3.Implies(args[0], args[1])
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_all:
            self._construct_quantifiers_expression(z3.ForAll)
        elif self._parent_with_this_state.outline == AuxSTConstants.predicate_exists:
            self._construct_quantifiers_expression(z3.Exists)
        elif self._parent_with_this_state.outline == AuxSTConstants.pre:
            self._copy_expression_from_child()
        elif self._parent_with_this_state.outline == AuxSTConstants.con:
            self._gather_children()
        elif self._parent_with_this_state.outline in [AuxSTConstants.undefined, AuxSTConstants.intrinsic]:
            self._register(self._parent_with_this_state.outline)
        elif self._parent_with_this_state.outline in [AuxSTConstants.extDigit, AuxSTConstants.ids,
                                                      AuxSTConstants.variadic_var]:
            self._register(self._parent_with_this_state.outline + "_" + self._parent_with_this_state.id)
        elif self._parent_with_this_state.outline in [AuxSTConstants.predicate_with_arguments, AuxSTConstants.var,
                                                      AuxSTConstants.variadic_var, AuxSTConstants.index_value,
                                                      AuxSTConstants.statement_assert,
                                                      AuxSTConstants.statement_assign,
                                                      AuxSTConstants.statement_cases,
                                                      AuxSTConstants.statement_case,
                                                      AuxSTConstants.statement_case_default,
                                                      AuxSTConstants.statement_is,
                                                      AuxSTConstants.statement_loop,
                                                      AuxSTConstants.statement_py,
                                                      AuxSTConstants.statement_range,
                                                      AuxSTConstants.statement_return, AuxSTConstants.selfInstance,
                                                      AuxSTConstants.preReferenced]:
            self._register_and_set_expression()
        else:
            raise NotImplementedError(self._parent_with_this_state.outline)
            pass

    def _gather_children(self):
        args = list()
        for child in self._parent_with_this_state.children:
            if hasattr(child, AuxSTConstants.predicate_state):
                args.append(child.get_state().expression)
        return args

    def _copy_expression_from_child(self):
        args = self._gather_children()
        if len(args) != 1:
            raise AssertionError("Exactly one predicate was expected, cannot create a copy of " + str(args))
        else:
            self.expression = args[0]

    def _register_and_set_expression(self):
        get_long_id = self._parent_with_this_state.get_long_id()
        self._register(get_long_id)
        self.expression = self.block_instance.get_identifiers_expression(get_long_id)

    def _determine_satisfiability(self):
        if self.current & self._satisfiability_check_done == 0:
            # determine satisfiability if the check has never been done yet
            s = z3.Solver()
            if self.expression is None:
                print("")
            s.add(self.expression)
            if s.check() == z3.sat:
                self.current |= self._satisfiable
                self._model = s.model()
            # mark satisfiability as determined
            self.current |= self._satisfiability_check_done

    def is_satisfiable(self):
        self._determine_satisfiability()
        return self.current & self._satisfiable > 0

    def _register(self, identifier):
        p = z3.Bool(identifier)
        self.block_instance.add_identifier_with_expression(identifier, p)

    def _construct_quantifiers_expression(self, delegate):
        list_bound_vars = list()
        for bound_var in self._parent_with_this_state.bound_vars:
            # transform the FPL list of bound vars into a z3-like list of bound vars
            try:
                list_bound_vars.append(self.block_instance.get_identifiers_expression(bound_var))
            except KeyError:
                # make sure, the instance registers all bound variables
                self._register(bound_var)
                list_bound_vars.append(self.block_instance.get_identifiers_expression(bound_var))
        self.expression = delegate(list_bound_vars, self._copy_expression_from_child())
