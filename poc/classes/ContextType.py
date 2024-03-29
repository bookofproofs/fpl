from poc.classes.AuxInterfaceSTTypePattern import AuxInterfaceSTTypePattern
from poc.classes.AuxBits import AuxBits
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxHighlightTag import AuxHighlightTag


class ContextType(AuxInterpretation, AuxInterfaceSTTypePattern):

    def __init__(self, i: AuxISourceAnalyser):
        AuxInterpretation.__init__(self, i.ast_info, i.errors)
        AuxInterfaceSTTypePattern.__init__(self)
        self.id = ""
        self.type_pattern = 0
        self._colon_read = False
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["Type"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateIdentifier" and not self._colon_read:
            # colon_read prevents mixing up PredicateIdentifiers of classes with their types
            self.type_pattern = self.type_pattern | AuxBits.objectBit
            self.id = parsing_info.id
        elif rule == "ObjectHeader":
            self.type_pattern = self.type_pattern | AuxBits.objectBit
            if parsing_info.id in AuxRuleDependencies.dep["TemplateHeader"]:
                self.type_pattern = self.type_pattern | AuxBits.templateBit
            elif parsing_info.id.startswith("tpl"):
                self.type_pattern = self.type_pattern | AuxBits.templateBit
            elif parsing_info.id.startswith("template"):
                self.type_pattern = self.type_pattern | AuxBits.templateBit
            else:
                self.type_pattern = self.type_pattern | AuxBits.inbuiltBit
            self.id = parsing_info.id
        elif rule == "FunctionalTermHeader":
            self.type_pattern = self.type_pattern | AuxBits.functionalTermBit
            self.type_pattern = self.type_pattern | AuxBits.inbuiltBit
            self.id = parsing_info.get_cst()
        elif rule == "PredicateHeader":
            self.type_pattern = self.type_pattern | AuxBits.predicateBit
            self.type_pattern = self.type_pattern | AuxBits.inbuiltBit
            self.id = parsing_info.get_cst()
        elif rule == "Colon":
            self._colon_read = True
        elif rule == "XId":
            self.type_pattern = self.type_pattern | AuxBits.extensionBit
            self.id = parsing_info.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        type_info = ContextType(i)
        type_info.zto = i.last_positions_by_rule['Type'].pos_to_str()
        type_info.zfrom = AuxISourceAnalyser.corrected_zpos_by(type_info.zto, len(type_info.id))
        if type_info.is_inbuilt():
            i.highlight_tags.append(AuxHighlightTag("inbuilttype", type_info.zfrom, type_info.zto))
        else:
            i.highlight_tags.append(AuxHighlightTag("type", type_info.zfrom, type_info.zto))
        i.parse_list.append(type_info)
