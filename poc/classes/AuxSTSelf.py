from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTTheory import AuxSTTheory
from poc.classes.AuxSTCoords import AuxSTCoords
from poc.classes.AuxSTRange import AuxSTRange
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxPredicateState import AuxPredicateState
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTSelf(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.selfInstance, i)
        self.reference = None
        self.number_ats = 0
        self.id = AuxSTConstants.selfInstance
        self._predicate_state = AuxPredicateState(self)

    def to_string(self):
        ret = "@" * self.number_ats + "self"
        for child in self.children:
            ret += child.to_string()
        return ret

    def clone(self):
        other = self._copy(AuxSTSelf(self._i))
        other.number_ats = self.number_ats
        other.id = self.id
        return other

    def get_declared_type(self):
        if self._declared_type is None:
            self._initialize_reference()
        return self._declared_type

    def _initialize_reference(self):
        test_node = self
        maximum_reached = False
        at = 0
        while at <= self.number_ats and not maximum_reached:
            test_node = test_node.parent
            if isinstance(test_node, AuxSTBuildingBlock):
                at += 1
            if isinstance(test_node.parent, AuxSTTheory):
                maximum_reached = True
        if at > self.number_ats and not maximum_reached:
            # the test_node points to the intended node referenced by 'self'
            # also remember the node in the this qualified identifier
            self.reference = test_node
            self._declared_type = test_node.get_declared_type()
            if self._declared_type is None:
                declared_type = InbuiltUndefined(self)
        # initializes the qualified id of self depending on the determined self._declared_type
        self.get_qualified_id()

    def get_qualified_id(self):
        if self._qualified_id is None:
            # initialize the qualified id of self to the qualified id of its declared type
            self._qualified_id = self.reference.get_qualified_id()
        return self._qualified_id

    def evaluate(self, sem):
        # initialize the reference of self, depending on the number of '@'
        propagated_expected_type = sem.eval_stack[-1].expected_type
        if self.reference is None:
            self._initialize_reference()
        if len(self.children) > 0:
            for child in self.children:
                if isinstance(child, AuxSTCoords):
                    raise NotImplementedError()
                elif isinstance(child, AuxSTRange):
                    raise NotImplementedError()
                elif isinstance(child, AuxSTQualified):
                    # due to the structure of symbol table, there can be only one child of self that is AuxSTQualified
                    check = EvaluateParams.evaluate_recursion(sem, child, expected_type=propagated_expected_type)
                    # set the value of self's evaluation to the value of the qualified identifier
                    sem.eval_stack[-1].value = check.value
                else:
                    raise NotImplementedError()
        else:
            EvaluateParams.evaluate_recursion(sem, self.reference, expected_type=propagated_expected_type)

    def get_state(self):
        return self._predicate_state

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id
