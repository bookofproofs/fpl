from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.WildcardTheoryNamespace import WildcardTheoryNamespace
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextWildcardTheoryNamespace:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        wildcard_namespace_info = WildcardTheoryNamespace(i.parse_list, parsing_info)
        AuxSymbolTable.add_usage_to_theory(i.theory_node, wildcard_namespace_info)
        i.parse_list.append(wildcard_namespace_info)
