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
        self.node = None
        # true if an evaluation error occurred
        self.evaluation_error = False
        # the (recursively) last building block, inside which we evaluate a new instance
        self.building_block = None
        # instance guid inside the building block handler,
        # separating the scope from other calls of the same building block
        self.instance_guid = None

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
    def evaluate_recursion(sem, node, expected_type, arg_type_list=None, check_args=None, building_block=None,
                           instance_guid=None):
        # create a new evaluation params set
        eval_params = EvaluateParams()
        eval_params.check_args = check_args
        eval_params.node = node
        if building_block is None:
            # propagate the last building block and its guid
            eval_params.building_block = sem.eval_stack[-1].building_block
            eval_params.instance_guid = sem.eval_stack[-1].instance_guid
            eval_params.arg_type_list = sem.eval_stack[-1].arg_type_list
            eval_params.check_args = sem.eval_stack[-1].check_args
        else:
            eval_params.building_block = building_block
            eval_params.instance_guid = instance_guid
            eval_params.arg_type_list = arg_type_list
            eval_params.check_args = check_args

        # whose expected type is the required one
        eval_params.expected_type = expected_type
        # push it on the stack
        sem.eval_stack.append(eval_params)

        node.evaluate(sem)  # start recursion
        eval_params = sem.eval_stack.pop()  # garbage-collect the stack
        # check if there is a type mismatch

        if eval_params.type_mismatch():
            sem.error_mgr.add_error(
                FplTypeMismatch(node, eval_params.expected_type.id, eval_params.value.id)
            )
            eval_params.evaluation_error = True

        # as a last step, we have to set the evaluated value of the symbol table element
        node.get_declared_type().set_repr(eval_params.value)
        return eval_params
