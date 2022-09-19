from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.fplerror import FplTypeMismatch


class EvaluateParams:
    """
    Optional params for the evaluate method of any node in the AuxSymbolTable recursively
    """

    def __init__(self):
        # Type in which this recursive call is being used (and should return a compatible type)
        self.expected_type = None
        # a list of types to be used to call the matched override (needed only for AuxSTPredicateWithArgs)
        self.arg_type_list = list()
        # check args is a flag indicating if arg_type_list is a representation
        # of arguments of some AuxSTPredicateWithArgs (even if empty)
        self.check_args = False
        # a possible argument error when assigning the arg_type_list to the parameters of override's signature
        self.argument_error = None
        # the returned value after recursion
        # (could be any type, since FPL has the same syntax for all)
        self.value = None
        # as value, but might be None if an error occurred (e.g. a type mismatch)
        self.returned_value = None
        # node within which these params are being evaluated
        self.node = None

    def type_mismatch(self):
        """
        True, if the type of the returned value is different from the type of the expected_value
        :return: Boolean Value
        """
        if self.expected_type is None:
            self.expected_type = InbuiltUndefined(self.node)
        if self.value is None:
            self.value = InbuiltUndefined(self.node)
        return self.expected_type.id != self.value.id

    @staticmethod
    def evaluate_recursion(sem, node, expected_type, args=list(), check_args=False):
        # create a new evaluation params set
        eval_params = EvaluateParams()
        eval_params.check_args = check_args
        eval_params.node = node
        # whose expected type is the required one
        eval_params.expected_type = expected_type
        if len(args) > 0:
            # remember the optional arguments in the EvaluateParams instance
            eval_params.arg_type_list = args
        # push it on the stack
        sem.eval_stack.append(eval_params)

        node.evaluate(sem)  # start recursion
        eval_params = sem.eval_stack.pop()  # garbage-collect the stack
        # check if there is a type mismatch

        if eval_params.type_mismatch():
            sem.error_mgr.add_error(
                FplTypeMismatch(node, eval_params.expected_type.id, eval_params.value.id)
            )
            # since we have a type mismatch, we have to return None
            eval_params.returned_value = None
        else:
            eval_params.returned_value = eval_params.value

        # as a last step, we have to set the evaluated value of the symbol table element
        node.get_declared_type().set_repr(eval_params.value)
        return eval_params
