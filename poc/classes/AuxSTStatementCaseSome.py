from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxInbuiltValues import InbuiltValueUndefined


class AuxSTStatementCaseSome(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxSTStatement.__init__(self, AuxSTConstants.statement_case, i)
        self.zfrom = i.corrected_position('Predicate')
        self.zto = i.last_positions_by_rule['ConditionFollowedByResult'].pos_to_str()
        # the default case statement's type is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementCaseSome(self._i)

    def evaluate(self, sem):
        case_predicate = self.children[0]
        ret_case_predicate = EvaluateParams.evaluate_recursion(sem, case_predicate,
                                                               expected_type=InbuiltPredicate(case_predicate))
        if ret_case_predicate.value.get_declared_type().is_predicate() and \
                isinstance(ret_case_predicate.value.get_value(), bool) and \
                ret_case_predicate.value.get_value():
            # if the predicate evaluation was successful and its value is indeed a boolean and evan it is true,
            # evaluate also the statement list inside the case
            ret = EvaluateParams.evaluate_recursion(sem, self.children[1])
            # set the resulting value of the case to be the value of the last statement inside the list
            sem.eval_stack[-1].value = ret.value
        else:
            # the case result is undefined
            sem.eval_stack[-1].value = InbuiltValueUndefined(self)
