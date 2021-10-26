from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextMapping import ContextMapping


class ContextSignature:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.signature, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxContext.signature], i.get_debug_parsing_info(parsing_info))
        if i.context.is_parsing_context([AuxContext.functionalTerm]):
            ContextMapping.start(i, parsing_info)
        else:
            i.parse_list.append(parsing_info)
