import z3

from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate


class AuxSTStatementIsOp(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_is, i)
        self.zfrom = i.corrected_position('is')
        self.zto = i.last_positions_by_rule['IsOperator'].pos_to_str()
        # the is operator's type is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementIsOp(self._i)

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        register = sem.eval_stack[-1]
        register.value = new_value
        something = self.children[0]
        is_what = self.children[1]
        ret_something = EvaluateParams.evaluate_recursion(sem, something, expected_type=something.get_declared_type())
        new_value.set_to(AuxSTStatementIsOp.try_establish_is_operator(ret_something.value, is_what))
        new_value.set_expression(z3.Bool(self.get_long_id()))

    @staticmethod
    def try_establish_is_operator(something, is_what):
        type_of_something = something.get_declared_type()
        return (type_of_something.type_pattern & is_what.type_pattern) > 0
