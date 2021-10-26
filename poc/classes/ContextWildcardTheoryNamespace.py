from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.WildcardTheoryNamespace import WildcardTheoryNamespace


class ContextWildcardTheoryNamespace:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        wildcard_namespace_info = WildcardTheoryNamespace(i.parse_list, parsing_info)
        used_namespace_node = i.touch_node()
        used_namespace_node.modifier = wildcard_namespace_info.modifier
        i.parse_list.append(wildcard_namespace_info)
