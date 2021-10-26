from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.Axiom import Axiom
from poc.classes.ContextSignature import ContextSignature


class ContextAxiom:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.axiom, i.get_debug_parsing_info(parsing_info))
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        axiom_info = Axiom(i.parse_list, parsing_info)
        i.context.pop_context([AuxContext.axiom], i.get_debug_parsing_info(parsing_info))
        i.pop_node()  # forget the axiom node
        i.parse_list.append(axiom_info)
