from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.All import All
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextAll:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxSymbolTable.predicate_all, i.get_debug_parsing_info(parsing_info))
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxSymbolTable.predicate_all], i.get_debug_parsing_info(parsing_info))
        new_info = All(i.parse_list, parsing_info)
        new_info.predicate.bound_vars = []
        # check if the bound variables are all declared
        bound_vars = new_info.predicate.get_bound_vars()
        for var in bound_vars:
            declared_vars = AuxSymbolTable.get_variable_in_current_scope(i.touch_node(), bound_vars[var])
            new_info.predicate.bound_vars.append(declared_vars)
        i.parse_list.append(new_info)
