from classes.AuxInterpretation import AuxInterpretation


class AuxScope:
    __outer_scope = None
    __type = None
    __scope_start = None
    __scope_end = None
    __objects_in_scope = dict()

    def __init__(self):
        self.__objects_in_scope['IDs'] = set()

    def set_start(self, scope_beginning_interpretation: AuxInterpretation):
        # remember the position of the scope start
        self.__scope_start = scope_beginning_interpretation

    def set_end(self, scope_ending_interpretation: AuxInterpretation):
        # remember the position of the scope end
        self.__scope_end = scope_ending_interpretation

    def get_start(self):
        # remember the position of the scope start
        return self.__scope_start

    def get_end(self):
        # remember the position of the scope end
        return self.__scope_end

    def set_type(self, scope_type: str):
        self.__type = scope_type

    def get_type(self):
        return self.__type

    def __str__(self):
        return str(type(self).__name__) + "[" + str(self.__type) + "] " + str(self.__scope_start) + " " + \
               str(self.__scope_end) + ": " + \
               str(self.__objects_in_scope)

    def register_identifier(self, identifier: str):
        """
        Register a new identifier in this Scope.
        If the identifier already exists in the Scope or in any of the outer_scopes, an error is raised.
        :param identifier:
        :return:
        """
        scope = self.get_scope_where_registered(identifier)
        if scope is not None:
            raise ReferenceError("identifier [" + identifier + "] already registered the scope of [" + scope + "]")
        else:
            self.__objects_in_scope["IDs"].add(identifier)

    def get_scope_where_registered(self, identifier):
        """
        Search for an identifier in this Scope and all outer_scopes
        and return either the type of the Scope, in which the identifier was found or None
        :param identifier:
        :return:
        """
        if identifier in self.__objects_in_scope["IDs"]:
            return self.type
        elif self.outer_scope is not None:
            return self.outer_scope.get_scope_where_registered(identifier)
        else:
            return None
