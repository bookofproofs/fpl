from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextSignature import ContextSignature


class ContextFunctionalTerm:
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        if i.context.is_parsing_context([AuxContext.classType]):
            # do not start a new context of a functionalTerm if it is a class type
            i.parse_list.append(parsing_info)
        else:
            if i.verbose:
                print("########### Unhandled context in ContextFunctionalTerm.start " + str(
                    i.context.get_context()) + " " + str(parsing_info))
            i.context.push_context(AuxContext.functionalTerm, i.get_debug_parsing_info(parsing_info))
            ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.pop_context([AuxContext.functionalTerm], i.get_debug_parsing_info(parsing_info))
        i.pop_node()  # clear memory for some new functional term
        i.parse_list.append(parsing_info)
