from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxContext import AuxContext
from poc.classes.GeneralType import GeneralType
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.ContextClassInstance import ContextClassInstance
from poc.classes.AuxBits import AuxBits
from poc.fplerror import FplInvalidInheritance


class ContextGeneralType:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        # consume all proceeding variables into a GeneralType and remove them from self.i.parse_list
        general_type = GeneralType(i.parse_list, parsing_info)

        # Handle the different contexts
        if i.context.is_parsing_context([AuxContext.optionalProperty]) or \
                i.context.is_parsing_context([AuxContext.mandatoryProperty]):
            # as the type of property definition that is not a class instance
            ContextClassInstance.start(i, general_type)
            return
        elif i.context.is_parsing_context([AuxContext.signature, AuxContext.paren, AuxContext.varDeclaration]):
            # As the type of variables in the signature
            pass
        elif i.context.is_parsing_context([AuxContext.functionalTerm, AuxContext.functionalTermImage]):
            # as the image of a functional term
            functional_term_node = i.touch_node()
            image_node = AuxSymbolTable.get_image_node(functional_term_node)
            AuxSymbolTable.add_param_to_image_node(image_node, general_type)
        elif i.context.is_parsing_context([AuxContext.block, AuxContext.varDeclaration]):
            # as the type of a variable declaration inside a block
            pass
        else:
            if i.verbose:
                print("########### Unhandled context in ContextGeneralType.dispatch " + str(
                    i.context.get_context()) + " " + str(parsing_info))
        i.parse_list.append(general_type)
