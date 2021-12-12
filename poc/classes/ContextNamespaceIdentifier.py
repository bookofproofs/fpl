from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextNamespaceIdentifier(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["NamespaceIdentifier"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "IdStartsWithCap":
            self.id = parsing_info.get_cst() + self.id
        elif rule == "Dot":
            self.id = parsing_info.get_cst() + self.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextNamespaceIdentifier(i.parse_list, parsing_info)
        i.parse_list.append(new_info)

    """
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        namespace_info = NamespaceIdentifier(i.parse_list, parsing_info)
        # NamespaceIdentifier can occur in the following contexts:
        if i.context.is_parsing_context([AuxContext.root]):
            # tag the namespace to the theory node
            i.theory_node.namespace = namespace_info.id
        else:
            if i.verbose:
                print(
                    "########### Unhandled context in ContextNamespaceIdentifier.dispatch " + str(
                        i.context.get_context()) + " " + str(namespace_info))
        i.parse_list.append(namespace_info)
    """
