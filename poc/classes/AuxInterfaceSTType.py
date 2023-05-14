class AuxInterfaceSTType:
    """
    A class for elements of the symbol table that have an outline with type
    """

    def __init__(self):
        self._declared_type = None

    def set_declared_type(self, type_node):
        self._declared_type = type_node

    def get_declared_type(self):
        if self._declared_type is None:
            raise AssertionError("The declared type of " + str(type(self)) + " is unexpectedly None")
        return self._declared_type

    def get_long_id(self):
        raise NotImplementedError(str(type(self)))
