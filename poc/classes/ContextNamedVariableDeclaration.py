from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.NamedVariableDeclaration import NamedVariableDeclaration


class ContextNamedVariableDeclaration:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.varDeclaration, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        named_var_decl = NamedVariableDeclaration(i.parse_list, parsing_info)
        is_signature = AuxContext.signature in i.context.get_context()
        if i.context.get_context().count(AuxContext.varDeclaration) == 1:
            # if there is exactly one varDeclaration in context, we have to add declared variables to the current node.
            parent = i.touch_node()
            var_nodes = AuxSymbolTable.get_child_by_outline(parent, AuxSymbolTable.variables)
            AuxSymbolTable.add_vars_to_nodes(var_nodes, named_var_decl, is_signature)
        i.parse_list.append(named_var_decl)
        i.context.pop_context([AuxContext.varDeclaration], i.get_debug_parsing_info(parsing_info))
