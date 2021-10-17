from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.GeneralType import GeneralType
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.ContextClassInstance import ContextClassInstance


class ContextGeneralType:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        # consume all proceeding variables into a GeneralType and remove them from self.i.parse_list
        general_type = GeneralType(i.parse_list, parsing_info)
        # remove from parse list rules proceeding Alias (if any)
        if i.context.is_parsing_context([AuxOutlines.classType]):
            # in the context of a class declaration, we have to update the type of the class
            class_node = i.working_stack[-1]
            class_node.type = general_type.id
            # add type to used types
            AuxSymbolTable.register_used_type_of_node(class_node, general_type)
            # we clear the context of classType
            i.context.pop_context([AuxOutlines.classType], i.get_debug_parsing_info(parsing_info))
        elif i.context.is_parsing_context([AuxOutlines.optionalProperty]) or \
                i.context.is_parsing_context([AuxOutlines.mandatoryProperty]):
            # as the type of property definition
            # we put the type name on the working stack so we can get it back
            # when the name of the class instance definition will be parsed next in the context
            # [AuxOutlines.mandatoryProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            # [AuxOutlines.optionalProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            i.working_stack.append(general_type.id)
            ContextClassInstance.start(i, general_type)
            return
        elif i.context.is_parsing_context([AuxOutlines.functionalTerm, AuxOutlines.functionalTermImage]):
            # as the image of a functional term
            functional_term_node = i.working_stack[-1]
            image_node = AuxSymbolTable.get_image_node(functional_term_node)
            AuxSymbolTable.add_param_to_image_node(image_node, general_type)
        elif i.context.is_parsing_context([AuxOutlines.block, AuxOutlines.varDeclaration]):
            # as the type of a variable declaration inside a block
            pass
        else:
            if i.debug:
                print("########### Unhandled context in ContextGeneralType.dispatch " + str(
                    i.context.get_context()) + " " + str(parsing_info))
        i.parse_list.append(general_type)
