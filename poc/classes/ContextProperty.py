from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines


class ContextProperty:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if parsing_info.get_cst() == 'opt' or parsing_info.get_cst() == 'optional':
            i.context.push_context(AuxOutlines.optionalProperty, i.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'mand' or parsing_info.get_cst() == 'mandatory':
            i.context.push_context(AuxOutlines.mandatoryProperty, i.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected keyword in ContextProperty.start " + parsing_info.get_cst())
        i.parse_list.append(parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if i.context.is_parsing_context([AuxOutlines.optionalProperty]):
            i.context.pop_context([AuxOutlines.optionalProperty], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxOutlines.mandatoryProperty]):
            i.context.pop_context([AuxOutlines.mandatoryProperty], i.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected context in ContextProperty.stop " + str(parsing_info.get_cst()))
        i.parse_list.append(parsing_info)

