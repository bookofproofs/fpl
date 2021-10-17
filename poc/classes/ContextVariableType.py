from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.VariableType import VariableType


class ContextVariableType:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        var_type_info = VariableType(i.parse_list, parsing_info)
        i.parse_list.append(var_type_info)
