from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.NamespaceIdentifier import NamespaceIdentifier
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextNamespaceIdentifier:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        namespace_info = NamespaceIdentifier(i.parse_list, parsing_info)
        # NamespaceIdentifer can occur in the following contexts:
        if i.context.is_parsing_context([AuxContext.root]):
            # tag the namespace to the theory node
            i.theory_node.namespace = namespace_info.id
        elif i.context.is_parsing_context([AuxContext.root, AuxContext.block, AuxContext.uses]):
            # as a name of namespaces used in the current namespace
            # Remember the used namespace because we will need it in case ContextWildcardTheoryNamespace is called
            i.push_node(AuxSymbolTable.add_usage_to_theory(i.theory_node, namespace_info))
        else:
            if i.verbose:
                print(
                    "########### Unhandled context in ContextNamespaceIdentifier.dispatch " + str(
                        i.context.get_context()) + " " + str(namespace_info))
        i.parse_list.append(namespace_info)

