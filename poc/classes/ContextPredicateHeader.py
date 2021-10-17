from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.ContextPredicateDeclaration import ContextPredicateDeclaration


class ContextPredicateHeader:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        # a predicate header can occur in the following contexts:
        if i.context.is_parsing_context([AuxOutlines.theory, AuxOutlines.block]):
            # inside a theory as a global predicate definition
            ContextPredicateDeclaration.start(i,parsing_info)
            return
        elif i.context.is_parsing_context([AuxOutlines.optionalProperty]) or \
                i.context.is_parsing_context([AuxOutlines.mandatoryProperty]):
            # inside a class, or functional term, a predicate instance
            ContextPredicateDeclaration.start(i,parsing_info)
            return
        else:
            if i.debug:
                print("########### Unhandled context in ContextPredicateHeader.dispatch" + str(
                    i.context.get_context()) + " " + str(parsing_info))
        i.parse_list.append(parsing_info)
