from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextSignature import ContextSignature


class ContextClassInstance:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.classInstanceDeclaration, i.get_debug_parsing_info(parsing_info))
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxContext.classInstanceDeclaration], i.get_debug_parsing_info(parsing_info))
        i.pop_node()  # remove the class instance node from the working stack
        i.parse_list.append(parsing_info)

