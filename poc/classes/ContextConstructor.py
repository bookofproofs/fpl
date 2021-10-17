from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.ContextSignature import ContextSignature


class ContextConstructor:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxOutlines.classConstructor, i.get_debug_parsing_info(parsing_info))
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxOutlines.classConstructor], i.get_debug_parsing_info(parsing_info))
        i.working_stack.pop()
        i.parse_list.append(parsing_info)

