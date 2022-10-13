from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTStatementCase(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxSTStatement.__init__(self, AuxSTConstants.statement_cases, i)
        self.zfrom = i.corrected_position('case')
        self.zto = i.last_positions_by_rule['CaseStatement'].pos_to_str()

    def clone(self):
        return AuxSTStatementCase(self._i)

    def evaluate(self, sem):
        determined_case = None
        for child in self.children:
            if isinstance(child, AuxInterfaceSTType):
                # call evaluation differently for all children that have predefined types
                determined_case = EvaluateParams.evaluate_recursion(sem, child, expected_type=child.get_declared_type())
            else:
                EvaluateParams.evaluate_recursion(sem, child)
        sem.eval_stack[-1].value = determined_case.value

    def get_declared_type(self):
        if self._declared_type is None:
            # the declared type of the FPL cases statement depends on the context of its placement in the FPL code
            if self.parent.parent.outline == AuxSTConstants.classConstructor:
                self._declared_type = self.parent.parent.get_declared_type()
            else:
                NotImplementedError(str(self))
        return self._declared_type
