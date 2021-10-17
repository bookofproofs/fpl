from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.NamedVariableDeclaration import NamedVariableDeclaration


class ContextNamedVariableDeclaration:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxOutlines.varDeclaration, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        parent_node = i.working_stack[-1]
        named_var_decl = NamedVariableDeclaration(i.parse_list, parsing_info)
        is_signature = i.context.is_parsing_context(
            [AuxOutlines.signature, AuxOutlines.paren, AuxOutlines.varDeclaration])
        AuxSymbolTable.add_variables_to_node(parent_node, named_var_decl.var_type, named_var_decl.var_list,
                                             is_signature)
        i.context.pop_context([AuxOutlines.varDeclaration], i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(named_var_decl)
