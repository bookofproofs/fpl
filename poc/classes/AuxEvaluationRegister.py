from poc.classes.AuxInbuiltTypes import InbuiltUndefined

"""
The class AuxEvaluationRegister stores all context-sensitive information for a symbol table node being 
semantically evaluated. 
"""


class AuxEvaluationRegister:
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
        self.instance = None
        self.is_dirty = True

    def type_mismatch(self):
        """
        True, if the type of the returned value is different from the type of the expected_value
        :return: Boolean value
        """
        if self.value is None:
            self.value = InbuiltUndefined(self.node)
        return self.expected_type.id != self.value.id
