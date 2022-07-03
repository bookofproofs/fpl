from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplTypeMismatch


class EvaluateParams:
    """
    Optional params for the evaluate method of any node in the AuxSymbolTable recursively
    """

    def __init__(self):
        # Identifier of a parent AuxSTQualified (if any, to identify the right override)
        self.parent_identifier = ""
        # Type in which this recursive call is being used (and should return a compatible type)
        self.expected_type = None
        # a list of types helping to find the matching override (needed only for AuxSTPredicateWithArgs)
        self.arg_types_list = list()
        # a list of values to be used to call the matched override (needed only for AuxSTPredicateWithArgs)
        self.arg_value_list = list()
        # the returned value after recursion
        # (could be any type, since FPL has the same syntax for all)
        self.value = None
        # actual type of the value
        self.actual_type = None
        # as value, but might be None if an error occurred (e.g. a type mismatch)
        self.returned_value = None
        # node within which these params are being evaluated
        self.node = None

    def type_mismatch(self):
        """
        True, if the type of the returned value is different from the type of the expected_value
        :return: Boolean Value
        """
        if self.expected_type is None and self.actual_type is not None:
            return True
        elif self.expected_type is not None and self.actual_type is None:
            return True
        elif self.expected_type is None and self.actual_type is None:
            return False
        else:
            return self.expected_type != self.actual_type

    @staticmethod
    def evaluate_recursion(sem, node, expected_type, args=list()):
        # create a new evaluation params set
        eval_params = EvaluateParams()
        eval_params.node = node
        # whose expected type is the required one
        eval_params.expected_type = expected_type
        if len(args) > 0:
            # remember the optional arguments in the EvaluateParams instance
            eval_params.arg_value_list = args
        # push it on the stack
        sem.eval_stack.append(eval_params)
        node.evaluate(sem)  # start recursion
        eval_params = sem.eval_stack.pop()  # garbage-collect the stack
        # check if there is a type mismatch
        if eval_params.type_mismatch():
            sem.analyzer.error_mgr.add_error(
                FplTypeMismatch(node, eval_params.expected_type, eval_params.actual_type)
            )
            # since we have a type mismatch, we have to return None
            eval_params.returned_value = None
        else:
            eval_params.returned_value = eval_params.value

        # as a last step, we have to set the evaluated value of the symbol table element
        node.set_value(eval_params.value)
        return eval_params

    @staticmethod
    def propagate(sem, eval_params):
        sem.eval_stack[-1].value = eval_params.value
        sem.eval_stack[-1].actual_type = eval_params.actual_type
