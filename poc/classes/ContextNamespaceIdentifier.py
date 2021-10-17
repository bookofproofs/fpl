from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.NamespaceIdentifier import NamespaceIdentifier
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextNamespaceIdentifier:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        namespace_info = NamespaceIdentifier(i.parse_list, parsing_info)
        # NamespaceIdentifer can occur in the following contexts:
        if i.context.is_parsing_context([AuxOutlines.root]):
            # tag the namespace to the theory node
            i.theory_node.namespace = namespace_info.id
        elif i.context.is_parsing_context([AuxOutlines.root, AuxOutlines.block, AuxOutlines.uses]):
            # as a name of namespaces used in the current namespace
            # In this case, remember the node of the used namespace added to the symbol table
            # because we will need it again when handling the NamespaceModifier rule (see last_element_of_list_or_tuple)
            i.working_stack.append(
                AuxSymbolTable.add_usage_to_theory(i.theory_node, namespace_info))

        else:
            if i.debug:
                print(
                    "########### Unhandled context in ContextNamespaceIdentifier.dispatch " + str(
                        i.context.get_context()) + " " + str(namespace_info))
        i.parse_list.append(namespace_info)

