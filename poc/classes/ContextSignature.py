from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextMapping import ContextMapping
from poc.classes.Signature import Signature
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextSignature:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.signature, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxContext.signature], i.get_debug_parsing_info(parsing_info))
        signature_info = Signature(i.parse_list, parsing_info)
        # Now, when we have parsed and interpreted the signature, we have to dispatch it depending on the context
        # similar to the dispatching done in ContextPredicateIdentifier.
        ContextSignature.dispatch(i, signature_info)
        if i.context.is_parsing_context([AuxContext.functionalTerm]):
            ContextMapping.start(i, signature_info)
        else:
            i.parse_list.append(signature_info)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, signature_info: Signature):
        # This dispatch method must be synchronized with the ContextPredicateIdentifier.dispatch
        if i.context.is_parsing_context([AuxContext.inferenceRule]) \
                or i.context.is_parsing_context([AuxContext.theoremLikeStmtConj]) \
                or i.context.is_parsing_context([AuxContext.theoremLikeStmtCor]) \
                or i.context.is_parsing_context([AuxContext.theoremLikeStmtProp]) \
                or i.context.is_parsing_context([AuxContext.theoremLikeStmtLem]) \
                or i.context.is_parsing_context([AuxContext.theoremLikeStmtThm]) \
                or i.context.is_parsing_context([AuxContext.predicateDeclaration]) \
                or i.context.is_parsing_context([AuxContext.functionalTerm]) \
                or i.context.is_parsing_context([AuxContext.classConstructor]) \
                or i.context.is_parsing_context([AuxContext.axiom]):
            # as a signature of an building block
            AuxSymbolTable.set_global_id(i.touch_node(), signature_info)
        else:
            if i.verbose:
                print("########### Unhandled context in ContextSignature.dispatch" + str(
                    i.context.get_context()) + " " + str(signature_info))
