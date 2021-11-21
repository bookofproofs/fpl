from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.PrimePredicate import PrimePredicate


class ContextPrimePredicate:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        p_info = PrimePredicate(i.parse_list, parsing_info)
        i.parse_list.append(p_info)
