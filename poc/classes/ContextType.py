from poc.classes.AuxBits import AuxBits
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation


class ContextType(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.type_pattern = 0
        self.id = ""
        self._colon_read = False
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["Type"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateIdentifier" and not self._colon_read:
            # colon_read prevents mixing up PredicateIdentifiers of classes with their types
            self.type_pattern = self.type_pattern | AuxBits.isObject
            self.id = parsing_info.id
        elif rule == "ObjectHeader":
            self.type_pattern = self.type_pattern | AuxBits.isObject
            if parsing_info.id in AuxRuleDependencies.dep["TemplateHeader"]:
                self.type_pattern = self.type_pattern | AuxBits.isTemplate
            elif parsing_info.id.startswith("tpl"):
                self.type_pattern = self.type_pattern | AuxBits.isTemplate
            elif parsing_info.id.startswith("template"):
                self.type_pattern = self.type_pattern | AuxBits.isTemplate
            else:
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
        type_info = ContextType(i)
        i.parse_list.append(type_info)
