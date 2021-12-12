from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPredicateIdentifier(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["PredicateIdentifier"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "IdStartsWithCap":
            self.id = parse_info.get_cst()
        elif rule == "AliasedId":
            self.id = parse_info.get_cst()

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicateIdentifier(i.parse_list, parsing_info)
        i.parse_list.append(new_info)

        """ todo
        pred_identifier = PredicateIdentifier(i.parse_list, parsing_info)
      
        # PredicateIdentifier can occur in following different  contexts:
        if i.context.is_parsing_context([AuxContext.inferenceRules, AuxContext.block]):
            # as a name of an inference rule
            i.push_node(AuxSymbolTable.add_inference_rule_to_theory(i.theory_node, pred_identifier))
            ContextInference.start(i, pred_identifier)
            return
        elif i.context.is_parsing_context([AuxContext.axiom, AuxContext.signature]):
            # as a name of an axiom
            i.push_node(AuxSymbolTable.add_axiom_to_theory(i.theory_node, pred_identifier))
        elif i.context.is_parsing_context([AuxContext.classDeclaration]):
            # as a name of a class instance definition
            # we put the class instance name on the working stack because we have yet to update it with its type
            # (see ContextGeneralType.dispatch)
            i.push_node(AuxSymbolTable.add_class_to_theory(i.theory_node, pred_identifier))
            i.context.push_context(AuxContext.classType, i.get_debug_parsing_info(pred_identifier))
        elif i.context.is_parsing_context([AuxContext.mandatoryProperty]) or \
                i.context.is_parsing_context([AuxContext.optionalProperty]):
            # as the type of a class instance definition
            ContextClassInstance.start(i, pred_identifier)
            return
        elif i.context.is_parsing_context([AuxContext.theoremLikeStmtThm, AuxContext.signature]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtLem, AuxContext.signature]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtProp, AuxContext.signature]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtCor, AuxContext.signature]) or \
                i.context.is_parsing_context([AuxContext.theoremLikeStmtConj, AuxContext.signature]):
            # as a name of a theorem-like statement or conjecture
            i.push_node(
                AuxSymbolTable.add_theorem_like_stmt_or_conj(i.theory_node, pred_identifier,
                                                             i.context.get_context()[-2]))
        elif i.context.is_parsing_context(
                [AuxContext.mandatoryProperty, AuxContext.functionalTerm, AuxContext.signature]) or \
                i.context.is_parsing_context(
                    [AuxContext.optionalProperty, AuxContext.functionalTerm, AuxContext.signature]) or \
                i.context.is_parsing_context(
                    [AuxContext.mandatoryProperty, AuxContext.predicateDeclaration, AuxContext.signature]) or \
                i.context.is_parsing_context(
                    [AuxContext.optionalProperty, AuxContext.predicateDeclaration, AuxContext.signature]) or \
                i.context.is_parsing_context([AuxContext.classInstanceDeclaration, AuxContext.signature]):
            # as a name of a functional term property
            # it with its image (see ContextGeneralType.dispatch)
            property_type = i.parse_list[-1]
            parent_node = i.touch_node()
            is_mandatory = (i.context.get_context()[-3] == AuxContext.mandatoryProperty)
            i.push_node(
                AuxSymbolTable.add_property_to_node(parent_node, pred_identifier, is_mandatory, property_type))
        elif i.context.is_parsing_context([AuxContext.functionalTerm, AuxContext.signature]):
            # as a name of a functional term definition
            i.push_node(AuxSymbolTable.add_functional_term_to_theory(i.theory_node, pred_identifier))
        elif i.context.is_parsing_context([AuxContext.predicateDeclaration, AuxContext.signature]):
            # as a name of a predicate definition
            i.push_node(AuxSymbolTable.add_predicate_to_theory(i.theory_node, pred_identifier))
        elif i.context.is_parsing_context([AuxContext.classDeclaration, AuxContext.block]):
            # as the name of a Constructor
            class_node = i.touch_node()
            i.push_node(AuxSymbolTable.add_constructor_to_class(class_node, pred_identifier))
            ContextConstructor.start(i, pred_identifier)
            return
        else:
            if i.verbose:
                print(
                    "########### Unhandled context in ContextPredicateIdentifier.dispatch " + str(
                        i.context.get_context()) + " " + str(pred_identifier))
        i.parse_list.append(pred_identifier)
        """
