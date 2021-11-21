from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextSignature import ContextSignature
from poc.classes.DefinitionPredicate import DefinitionPredicate


class ContextDefinitionPredicate:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.predicateDeclaration, i.get_debug_parsing_info(parsing_info))
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxContext.predicateDeclaration], i.get_debug_parsing_info(parsing_info))
        p_info = DefinitionPredicate(i.parse_list, parsing_info)
        node = i.pop_node()  # forget the predicate declaration node
        p_info.predicate.parent = node  # link the parsed predicate to the node of the predicate declaration
        i.parse_list.append(parsing_info)
