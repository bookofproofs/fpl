from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextSignature import ContextSignature


class ContextParen:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.paren, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if i.context.is_parsing_context([AuxContext.varDeclaration]):
            # we end the context of variable declaration (if any)
            # This may happen inside before a ParamTuple is parsed completely
            i.context.pop_context([AuxContext.varDeclaration])
        i.context.pop_context([AuxContext.paren], i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)
