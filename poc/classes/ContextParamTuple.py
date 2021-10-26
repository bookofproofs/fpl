from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.ParamTuple import ParamTuple


class ContextParamTuple:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        param_tuple = ParamTuple(i.parse_list, parsing_info)
        i.parse_list.append(param_tuple)

