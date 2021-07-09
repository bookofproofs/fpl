from classes.AuxInterpretation import AuxInterpretation
from classes.AuxScope import AuxScope


class AuxDeclaredVariable(AuxInterpretation):
    __name = ""  # Name of the variable
    __value = None  # Value of the variable
    __type = None  # Type of the variable

    def __init__(self, inter: AuxInterpretation):
        self.clone(inter)
        self.__name = self.get_interpretation()

    def set_value(self, value):
        self.__value = value

    def set_type(self, fpl_type):
        self.__type = fpl_type

    def get_type(self):
        return self.__type

    def get_value(self):
        return self.__value

    def register_in_block(self, scope: AuxScope):
        scope.register_identifier(self.__name)
