from poc.classes.AuxBits import AuxBits
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation


class ContextType(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.type_pattern = 0
        self.id = ""
        self._colon_read = False
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["Type"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "TemplateHeader":
            self.type_pattern = self.type_pattern | AuxBits.isObject
            self.type_pattern = self.type_pattern | AuxBits.isGeneric
            self.id = parsing_info.id
        elif rule == "PredicateIdentifier" and not self._colon_read:
            # colon_read prevents mixing up PredicateIdentifiers of classes with their types
            self.type_pattern = self.type_pattern | AuxBits.isObject
            self.id = parsing_info.id
        elif rule == "ObjectHeader":
            self.type_pattern = self.type_pattern | AuxBits.isObject
            self.type_pattern = self.type_pattern | AuxBits.isInbuilt
            self.id = parsing_info.id
        elif rule == "FunctionalTermHeader":
            self.type_pattern = self.type_pattern | AuxBits.isFunctionalTerm
            self.type_pattern = self.type_pattern | AuxBits.isInbuilt
            self.id = parsing_info.id
        elif rule == "PredicateHeader":
            self.type_pattern = self.type_pattern | AuxBits.isPredicate
            self.type_pattern = self.type_pattern | AuxBits.isInbuilt
            self.id = parsing_info.id
        elif rule == "Colon":
            self._colon_read = True
        elif rule == "XId":
            self.type_pattern = self.type_pattern | AuxBits.isExtension
            self.id = parsing_info.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        type_info = ContextType(i.parse_list, parsing_info)
        i.parse_list.append(type_info)

        """
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
        """
