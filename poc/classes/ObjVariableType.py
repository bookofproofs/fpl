class ObjVariableType:
    ancestor_type = None
    fpl_type = None

    def __init__(self, var_type):
        if not type(var_type) is str:
            raise TypeError("var_type must be a string, was " + str(var_type))
        self.fpl_type = var_type

    def inherit_from(self, ancestor_type):
        if not type(ancestor_type) is ObjVariableType:
            raise TypeError("ancestor_type must be a VariableType, was " + str(ancestor_type))
        if ancestor_type.fpl_type == "tpl" or ancestor_type.fpl_type == "template":
            raise TypeError("inheritance from a template type is not possible " + str(ancestor_type.fpl_type))
        self.ancestor_type = ancestor_type

    '''
    Compares a given type along the inheritance chain of types and returns True if this type
    is contained in that chain, otherwise False
    '''

    def is_of_type(self, var_type):
        if var_type is None:
            return False
        if self.fpl_type is None:
            return False
        if not type(var_type) is str:
            raise TypeError("var_type must be a VariableType, was " + str(var_type))
        elif var_type == self.fpl_type:
            return True
        else:
            return self.ancestor_type.is_of_type(var_type)
