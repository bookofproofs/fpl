from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.NamespaceIdentifier import NamespaceIdentifier
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextNamespaceIdentifier:
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

