"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class IndexValue(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.info = parsing_info
        self.firstArg = None
        self.secondArg = None
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["IndexValue"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Variable":
            if self.firstArg is None:
                self.firstArg = parsing_info
            else:
                self.secondArg = parsing_info
        elif rule == "Dollar":
            self.secondArg = int(str(parsing_info.get_cst()))
        elif rule == "Digit":
            pass

