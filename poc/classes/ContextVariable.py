"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxContext import AuxContext
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextVariable:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.parse_list.append(parsing_info)
        if i.context.is_parsing_context([AuxContext.bound]):
            # In this context, variable may be used only if they have been previously properly declared.
            # Try to find out if the variable in the scope.
            var = AuxSymbolTable.get_variable_type_in_current_scope(i.touch_node(), parsing_info)


