from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.PredicateIdentifier import PredicateIdentifier
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.ContextInference import ContextInference
from poc.classes.ContextClassInstance import ContextClassInstance
from poc.classes.ContextConstructor import ContextConstructor


class ContextPredicateIdentifier:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        pred_identifier = PredicateIdentifier(i.parse_list, parsing_info)
        # PredicateIdentifier can occur in following different  contexts:
        if i.context.is_parsing_context([AuxOutlines.inferenceRules, AuxOutlines.block]):
            # as a name of an inference rule
            i.working_stack.append(
                AuxSymbolTable.add_inference_rule_to_theory(i.theory_node, pred_identifier))
            ContextInference.start(i, pred_identifier)
            return
        elif i.context.is_parsing_context([AuxOutlines.axiom, AuxOutlines.signature]):
            # as a name of an axiom that is global
            i.working_stack.append(AuxSymbolTable.add_axiom_to_theory(i.theory_node, pred_identifier))
        elif i.context.is_parsing_context([AuxOutlines.classDeclaration]):
            # as a name of a class instance definition
            # we put the class instance name on the working stack because we have yet to update it with its type
            # (see ContextGeneralType.dispatch)
            i.working_stack.append(AuxSymbolTable.add_class_to_theory(i.theory_node, pred_identifier))
            i.context.push_context(AuxOutlines.classType, i.get_debug_parsing_info(pred_identifier))
        elif i.context.is_parsing_context([AuxOutlines.classType]):
            # as a name of a class type, do nothing since ContextGeneralType.dispatch handles this
            pass
        elif i.context.is_parsing_context([AuxOutlines.varDeclaration]):
            # as a name of type, do nothing since named_variable_declaration_stop handles this
            pass
        elif i.context.is_parsing_context([AuxOutlines.mandatoryProperty]) or \
                i.context.is_parsing_context([AuxOutlines.optionalProperty]):
            # as the type of a class instance definition
            # we put the type name on the working stack so we can get it back
            # when the name of the class instance definition will be parsed next in the context
            # [AuxOutlines.mandatoryProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            # [AuxOutlines.optionalProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            i.working_stack.append(pred_identifier.id)
            ContextClassInstance.start(i, pred_identifier)
            return
        elif i.context.is_parsing_context([AuxOutlines.theoremLikeStmtThm, AuxOutlines.signature]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtLem, AuxOutlines.signature]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtProp, AuxOutlines.signature]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtCor, AuxOutlines.signature]) or \
                i.context.is_parsing_context([AuxOutlines.theoremLikeStmtConj, AuxOutlines.signature]):
            # as a name of a predicate definition that is global
            i.working_stack.append(
                AuxSymbolTable.add_theorem_like_stmt(i.theory_node, pred_identifier,
                                                     i.context.get_context()[-2]))
        elif i.context.is_parsing_context([AuxOutlines.predicateDeclaration, AuxOutlines.signature]):
            # as a name of a predicate definition that is global
            i.working_stack.append(AuxSymbolTable.add_predicate_to_theory(i.theory_node, pred_identifier))
        elif i.context.is_parsing_context(
                [AuxOutlines.mandatoryProperty, AuxOutlines.functionalTerm, AuxOutlines.signature]) or \
                i.context.is_parsing_context(
                    [AuxOutlines.optionalProperty, AuxOutlines.functionalTerm, AuxOutlines.signature]):
            # as a name of a functional term property
            # we put the functional term name on the working stack because we have yet to update
            # it with its image (see ContextGeneralType.dispatch)
            parent_node = i.working_stack[-1]
            is_mandatory = (i.context.get_context()[-3] == AuxOutlines.mandatoryProperty)
            i.working_stack.append(
                AuxSymbolTable.add_property_to_node(parent_node, pred_identifier, is_mandatory,
                                                    i.context.get_context()[-2]))
        elif i.context.is_parsing_context(
                [AuxOutlines.mandatoryProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature]) or \
                i.context.is_parsing_context(
                    [AuxOutlines.optionalProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature]):
            # as a name of a class instance property
            # we put the class instance name on the working stack because we have yet to update
            # it with its image (see ContextGeneralType.dispatch)
            property_type = i.working_stack.pop()
            parent_node = i.working_stack[-1]
            is_mandatory = (i.context.get_context()[-3] == AuxOutlines.mandatoryProperty)
            i.working_stack.append(
                AuxSymbolTable.add_property_to_node(parent_node, pred_identifier, is_mandatory, property_type))
        elif i.context.is_parsing_context([AuxOutlines.functionalTerm, AuxOutlines.signature]):
            # as a name of a functional term definition that is global
            # we put the functional term name on the working stack because we have yet to update
            # it with its image (see ContextGeneralType.dispatch)
            i.working_stack.append(
                AuxSymbolTable.add_functional_term_to_theory(i.theory_node, pred_identifier))
        elif i.context.is_parsing_context([AuxOutlines.classDeclaration, AuxOutlines.block]):
            # as the name of a Constructor
            class_node = i.working_stack[-1]
            i.working_stack.append(AuxSymbolTable.add_constructor_to_class(class_node, pred_identifier))
            ContextConstructor.start(i, pred_identifier)
            return
        else:
            if i.debug:
                print(
                    "########### Unhandled context in ContextPredicateIdentifier.dispatch " + str(
                        i.context.get_context()) + " " + str(pred_identifier))
        i.parse_list.append(pred_identifier)
