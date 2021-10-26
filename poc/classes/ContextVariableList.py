from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.VariableList import VariableList
from poc.classes.ContextNamedVariableDeclaration import ContextNamedVariableDeclaration


class ContextVariableList:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        # consume all proceeding variables into a VariableList and remove them from self.i.parse_list
        variable_list = VariableList(i.parse_list, parsing_info)
        if i.context.is_parsing_context([AuxContext.signature, AuxContext.paren]) or \
                i.context.is_parsing_context([AuxContext.classDeclaration, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.axiom, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.inferenceRule, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.predicateDeclaration, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtThm, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtLem, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtConj, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtCor, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtProp, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.classConstructor, AuxContext.block]) or \
                i.context.is_parsing_context([AuxContext.varDeclaration, AuxContext.paren]) or \
                i.context.is_parsing_context([AuxContext.functionalTermImage, AuxContext.paren]):
            ContextNamedVariableDeclaration.start(i, variable_list)
            return
        else:
            if i.verbose:
                print(
                    "########### Unhandled context in ContextVariableList.dispatch " + str(
                        i.context.get_context()) + " " + str(variable_list))
        i.parse_list.append(variable_list)
