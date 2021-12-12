from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import AnyNode


class ContextWildcardTheoryNamespace(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.used_namespace = AnyNode(info=parsing_info.get_ast_info(), modifier=None)
        self.aggregate_previous_rules(parse_list,
                                      ["Star", "Alias", "alias", "IdStartsWithCap", "NamespaceIdentifier",
                                       "NamespaceModifier", "Comma"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "NamespaceModifier":
            self.used_namespace.modifier = parse_info.get_cst()[-1]
        elif rule in ["IdStartsWithCap", "NamespaceIdentifier"]:
            self.used_namespace.id = parse_info.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextWildcardTheoryNamespace(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
