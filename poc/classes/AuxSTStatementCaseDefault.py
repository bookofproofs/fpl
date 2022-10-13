from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTStatementCaseDefault(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxSTStatement.__init__(self, AuxSTConstants.statement_case_default, i)
        self.zfrom = i.corrected_position('else')
        self.zto = i.last_positions_by_rule['DefaultResult'].pos_to_str()

    def clone(self):
        return AuxSTStatementCaseDefault(self._i)

    def evaluate(self, sem):
        # evaluate the statement list with result inside the default case
        EvaluateParams.evaluate_recursion(sem, self.children[0])
        # set the resulting value of the default case to be the value of the last statement inside the list
        sem.eval_stack[-1].value = sem.last_value

    def get_declared_type(self):
        if self._declared_type is None:
            # the declared type of the default case is the table of the whole case statement
            self._declared_type = self.parent.get_declared_type()
        return self._declared_type
