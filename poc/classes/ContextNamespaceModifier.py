from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.NamespaceModifier import NamespaceModifier


class ContextNamespaceModifier:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        namespace_modifier_info = NamespaceModifier(i.parse_list, parsing_info)
        used_namespace_node = i.working_stack.pop()
        used_namespace_node.modifier = namespace_modifier_info.modifier
        i.parse_list.append(namespace_modifier_info)
