from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxPredicateState import AuxPredicateState
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTStatement(AuxST):

    def __init__(self, statement_type: str, i):
        super().__init__(AuxSTConstants.statement, i)
        self._statement_type = statement_type
        self._predicate_state = AuxPredicateState(self)

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined(self)

    def get_state(self):
        return self._predicate_state

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self._statement_type
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id
