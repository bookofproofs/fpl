from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.ContextDefinitionPredicate import ContextDefinitionPredicate


class ContextPredicateHeader:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        # a predicate header can occur in the following contexts:
        if i.context.is_parsing_context([AuxContext.theory, AuxContext.block]):
            # inside a theory as a global predicate definition
            ContextDefinitionPredicate.start(i, parsing_info)
            return
        elif i.context.is_parsing_context([AuxContext.optionalProperty]) or \
                i.context.is_parsing_context([AuxContext.mandatoryProperty]):
            # inside a class, or functional term as a predicate property
            ContextDefinitionPredicate.start(i, parsing_info)
            return
        else:
            if i.verbose:
                print("########### Unhandled context in ContextPredicateHeader.dispatch" + str(
                    i.context.get_context()) + " " + str(parsing_info))
        i.parse_list.append(parsing_info)
