from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.IsOperator import IsOperator


class ContextIsOperator:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = IsOperator(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
