from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.ContextSignature import ContextSignature


class ContextTheoremLikeStatement:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if parsing_info.get_cst() == 'thm' or parsing_info.get_cst() == 'theorem':
            i.context.push_context(AuxOutlines.theoremLikeStmtThm, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'prop' or parsing_info.get_cst() == 'proposition':
            i.context.push_context(AuxOutlines.theoremLikeStmtProp, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'lem' or parsing_info.get_cst() == 'lemma':
            i.context.push_context(AuxOutlines.theoremLikeStmtLem, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'cor' or parsing_info.get_cst() == 'corollary':
            i.context.push_context(AuxOutlines.theoremLikeStmtCor, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'conj' or parsing_info.get_cst() == 'conjecture':
            i.context.push_context(AuxOutlines.theoremLikeStmtConj, i.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected keyword in ContextTheoremLikeStatement.start " + parsing_info.get_cst())
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if i.context.is_parsing_context([AuxOutlines.theoremLikeStmtThm]):
            i.context.pop_context([AuxOutlines.theoremLikeStmtThm], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxOutlines.theoremLikeStmtProp]):
            i.context.pop_context([AuxOutlines.theoremLikeStmtProp], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxOutlines.theoremLikeStmtLem]):
            i.context.pop_context([AuxOutlines.theoremLikeStmtLem], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxOutlines.theoremLikeStmtCor]):
            i.context.pop_context([AuxOutlines.theoremLikeStmtCor], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxOutlines.theoremLikeStmtConj]):
            i.context.pop_context([AuxOutlines.theoremLikeStmtConj], i.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected context in ContextTheoremLikeStatement.stop " + parsing_info.get_cst())
        i.parse_list.append(parsing_info)


