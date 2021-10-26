from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextSignature import ContextSignature


class ContextTheoremLikeStatement:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if parsing_info.get_cst() == 'thm' or parsing_info.get_cst() == 'theorem':
            i.context.push_context(AuxContext.theoremLikeStmtThm, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'prop' or parsing_info.get_cst() == 'proposition':
            i.context.push_context(AuxContext.theoremLikeStmtProp, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'lem' or parsing_info.get_cst() == 'lemma':
            i.context.push_context(AuxContext.theoremLikeStmtLem, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'cor' or parsing_info.get_cst() == 'corollary':
            i.context.push_context(AuxContext.theoremLikeStmtCor, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'conj' or parsing_info.get_cst() == 'conjecture':
            i.context.push_context(AuxContext.theoremLikeStmtConj, i.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected keyword in ContextTheoremLikeStatement.start " + parsing_info.get_cst())
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if i.context.is_parsing_context([AuxContext.theoremLikeStmtThm]):
            i.context.pop_context([AuxContext.theoremLikeStmtThm], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxContext.theoremLikeStmtProp]):
            i.context.pop_context([AuxContext.theoremLikeStmtProp], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxContext.theoremLikeStmtLem]):
            i.context.pop_context([AuxContext.theoremLikeStmtLem], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxContext.theoremLikeStmtCor]):
            i.context.pop_context([AuxContext.theoremLikeStmtCor], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxContext.theoremLikeStmtConj]):
            i.context.pop_context([AuxContext.theoremLikeStmtConj], i.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected context in ContextTheoremLikeStatement.stop " + parsing_info.get_cst())
        i.pop_node()  # forget the theorem-like statement node
        i.parse_list.append(parsing_info)


