from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate


class AuxSTStatementAssert(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_assert, i)
        self.zfrom = i.corrected_position('assert')
        self.zto = i.last_positions_by_rule['AssertionStatement'].pos_to_str()
        # the assert statement is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementAssert(self._i)

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        register = sem.eval_stack[-1]
        register.value = new_value
        # evaluate the predicate of the assertion statement
        assertion_predicate = self.children[0]
        ret = EvaluateParams.evaluate_recursion(sem,self.children[0], expected_type=InbuiltPredicate(self))
        ret.instance.add_asserted_predicate(assertion_predicate.get_long_id(), assertion_predicate)
        new_value.set_true()
        new_value.set_expression(ret.value.get_expression())
