from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTQualified(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.qualified, i)
        # the resolved_parent is the node in the symbol table that can possibly be identified
        # during the semantic analysis
        self._resolved_parent = None

    def to_string(self):
        ret = "dot["
        for child in self.children:
            ret += child.to_string()
        ret += "]"
        return ret

    def clone(self):
        my_copy = self._copy(AuxSTQualified(self._i))
        my_copy._resolved_parent = self._resolved_parent
        return my_copy

    def _initialize_qualified_id_from_parent(self, sem):
        """
        Initializes the _qualified_id attribute of AuxSTQualified based on the parent
        :param sem: evaluation path where the but-last element is the parent node of AuxSTQualified in the symbol table
        :return: None
        """
        if sem.eval_stack[-2].node.outline == AuxSTConstants.var:
            self._qualified_id = sem.eval_stack[-2].node.get_declared_type().get_qualified_id()
        elif sem.eval_stack[-2].node.outline == AuxSTConstants.selfInstance:
            self._qualified_id = sem.eval_stack[-2].node.get_qualified_id()
        else:
            raise NotImplementedError()

    def evaluate(self, sem):
        self._initialize_qualified_id_from_parent(sem)
        propagated_expected_type = sem.eval_stack[-1].expected_type
        # there is (syntactically) only one child node of AuxSTQualified so
        check = EvaluateParams.evaluate_recursion(sem, self.children[0], expected_type=propagated_expected_type)
        # set the value of the evaluation to the value retrieved
        sem.eval_stack[-1].value = check.value

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.to_string()
        return self._long_id
