from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVarSpecList(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.var_spec)
        # var spec lists have the inbuilt undefined type per default
        self.set_declared_type(InbuiltUndefined(self.parent))

    def clone(self):  # noqa
        return AuxSTVarSpecList()

    def evaluate(self, sem):
        for child in self.children:
            expected_type = self._determine_exptected_type(child)
            EvaluateParams.evaluate_recursion(sem, child, expected_type)
        sem.eval_stack[-1].value = InbuiltUndefined(self.parent)

    def _determine_exptected_type(self, child):
        if child.outline == AuxSTConstants.statement_assign:
            # the expected type of the assignment is the type of the variable to which we assign the value
            return child.children[0].get_declared_type()
        elif child.outline == AuxSTConstants.statement_return:
            return child.get_declared_type()
        elif child.outline == AuxSTConstants.var_decl:
            # the expected type of var declarations is undefined, which is also initialize
            child.set_declared_type(InbuiltUndefined(child))
            return child.get_declared_type()
        else:
            raise NotImplementedError(child)
