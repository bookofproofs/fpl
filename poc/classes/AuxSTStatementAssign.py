from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTStatementAssign(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_assign, i)
        self.zfrom = i.corrected_position('Assignee')
        self.zto = i.last_positions_by_rule['AssignmentStatement'].pos_to_str()

    def clone(self):
        return AuxSTStatementAssign(self._i)

    def evaluate(self, sem):
        # first, establish the type of the assignee
        if isinstance(self.children[0], AuxInterfaceSTType):
            assignee_type = self.children[0].get_declared_type()
        else:
            raise NotImplementedError(str(type(self.children[0])))
        ret = EvaluateParams.evaluate_recursion(sem, self.children[1], assignee_type)
        sem.eval_stack[-1].value = ret.value
