from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTClassInstance import AuxSTClassInstance
from poc.classes.AuxBits import AuxBits


class ContextClassInstance(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.building_block = AuxSTClassInstance(i)
        self._var_type = None
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["ClassInstance"] + ["FunctionalTermHeader"]
                                      , self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "VariableType":
            self.building_block.register_child(parsing_info.var_type)  # noqa
            self._var_type = parsing_info.var_type  # remember the pointer for handling "FunctionalTermHeader"
        elif rule == "FunctionalTermHeader":
            # The syntax of FPL allows incomplete functional terms (e.g. missing images)
            # In this case, there is a parsed FunctionTermHeader that proceeds the VariableType
            # in the parse list. Semantically, this is incorrect. We correct the type_pattern of
            # the VariableType anyway in the symbol table because the semantical error will be detected when we
            # start the semantical analysis.
            # Note: At this stage, we are still in the syntax analysis process. We want to strictly separate
            # the phases of syntactical and semantical analysis (backend and frontend of the FPL interpreter).
            self._var_type.id = parsing_info.id
            self._var_type.type_pattern = self._var_type.type_pattern | AuxBits.functionalTermBit
            self._var_type.type_pattern = self._var_type.type_pattern | AuxBits.inbuiltBit
            self._var_type.zfrom = AuxISourceAnalyser.corrected_zpos_by(self._var_type.zfrom, len(self._var_type.id))
        elif rule == "Signature":
            self.building_block.register_child(parsing_info.symbol_signature)  # noqa
            self.building_block.id = parsing_info.symbol_signature.to_string()  # noqa
        elif rule == "InstanceBlock":
            self.building_block.register_child(parsing_info.variable_spec)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextClassInstance(i)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)
