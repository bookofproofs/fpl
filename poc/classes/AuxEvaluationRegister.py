from poc.classes.AuxBits import AuxBits

"""
The class AuxEvaluationRegister stores all context-sensitive information for a symbol table node being 
semantically evaluated. 
"""


class AuxEvaluationRegister:
    def __init__(self, node, expected_type):
        # Type in which this recursive call is being used (and should return a compatible type)
        self.expected_type = expected_type
        # a possible argument error when assigning the arg_type_list to the parameters of override's signature
        self.argument_error = None
        # the returned value after recursion
        # (could be any type, since FPL has the same syntax for all)
        self.value = None
        # as value, but might be None if an error occurred (e.g. a type mismatch)
        self.node = node
        # true if an evaluation error occurred
        self.evaluation_error = False
        # the (recursively) last building block, inside which we evaluate a new instance
        self.building_block = None
        # instance guid inside the building block handler,
        # separating the scope from other calls of the same building block
        self.instance_guid = None
        self.instance = None
        self.is_dirty = True
