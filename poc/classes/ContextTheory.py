from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext


class ContextTheory:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.theory, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxContext.theory], i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)
