from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.VariableList import VariableList
from poc.classes.ContextNamedVariableDeclaration import ContextNamedVariableDeclaration


class ContextVariableList:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        # consume all proceeding variables into a VariableList and remove them from self.i.parse_list
        variable_list = VariableList(i.parse_list, parsing_info)
        if i.context.is_parsing_context([AuxOutlines.signature, AuxOutlines.paren]) or \
                i.context.is_parsing_context([AuxOutlines.classDeclaration, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.axiom, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.inferenceRule, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.predicateDeclaration, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtThm, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtLem, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtConj, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtCor, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtProp, AuxOutlines.block]) or \
                i.context.is_parsing_context([AuxOutlines.classConstructor, AuxOutlines.block]):
            ContextNamedVariableDeclaration.start(i, variable_list)
            return
        else:
            if i.debug:
                print(
                    "########### Unhandled context in ContextVariableList.dispatch " + str(
                        i.context.get_context()) + " " + str(variable_list))
        i.parse_list.append(variable_list)
