from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.ParenthesisedGeneralType import ParenthesisedGeneralType


class ContextParenthesisedGeneralType:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        param_tuple = ParenthesisedGeneralType(i.parse_list, parsing_info)
        i.parse_list.append(param_tuple)

