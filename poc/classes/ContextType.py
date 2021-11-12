from poc.classes.AuxBits import AuxBits
from poc.classes.AuxContext import AuxContext
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.Type import Type
from fplerror import FplInvalidInheritance


class ContextType:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        type_info = Type(i.parse_list, parsing_info)
        i.parse_list.append(type_info)
        if i.context.is_parsing_context([AuxContext.classType]):
            # in the context of a class declaration, we have to update the type of the class
            class_node = i.touch_node()
            if AuxBits.is_functional_term(type_info.pattern_int):
                parsing_info.all_errors().append(
                    FplInvalidInheritance(parsing_info.get_ast_info(), type_info.id, "a functional term type"))
            elif AuxBits.is_predicate(type_info.pattern_int):
                parsing_info.all_errors().append(
                    FplInvalidInheritance(parsing_info.get_ast_info(), type_info.id, "a predicate type"))
            elif AuxBits.is_generic(type_info.pattern_int):
                parsing_info.all_errors().append(
                    FplInvalidInheritance(parsing_info.get_ast_info(), type_info.id, "a generic type"))
            elif AuxBits.is_index(type_info.pattern_int):
                parsing_info.all_errors().append(
                    FplInvalidInheritance(parsing_info.get_ast_info(), type_info.id, "an index type"))
            elif AuxBits.is_extension(type_info.pattern_int):
                parsing_info.all_errors().append(
                    FplInvalidInheritance(parsing_info.get_ast_info(), type_info.id,
                                          "a user-defined syntax extension"))
            else:
                # register the type of the class
                class_node.type = type_info.id
                class_node.type_pattern = type_info.pattern_int
            # we clear the context of classType
            i.context.pop_context([AuxContext.classType], i.get_debug_parsing_info(parsing_info))
        else:
            if i.verbose:
                print("########### Unhandled context in ContextType.dispatch " + str(
                    i.context.get_context()) + " " + str(parsing_info))