from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxEvaluation import EvaluateParams


class AuxEvaluationPredicate:
    def __init__(self):
        # we add this attribute to the class to make it clear that this class is meant to be used as a mixin
        self.children = list()

    def evaluate_children(self, sem):
        expressions = list()
        bool_values = list()
        errors = list()
        for child in self.children:
            check = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
            expressions.append(check.value.get_expression())
            errors.append(check.evaluation_error)
            bool_values.append(check.value.get_value())
        return expressions, bool_values, errors
