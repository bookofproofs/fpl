from poc.classes.AuxInterpretation import AuxInterpretation


class Signature(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.listNamedDeclarations = []
        self.aggregate_previous_rules(parse_list,
                                      ["ParamTuple"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "ParamTuple":
            self.listNamedDeclarations = parsing_info.tuple

    def to_signature_string(self):
        ret = "["
        first_found = False
        for named_var_decl in reversed(self.listNamedDeclarations):
            if not first_found:
                ret += named_var_decl.to_signature_string()
                first_found = True
            else:
                ret += "," + named_var_decl.to_signature_string()
        ret += "]"
        return ret
