from poc.classes.AuxInterpretation import AuxInterpretation


class NamedVariableDeclaration(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.var_list = dict()
        self.var_type = None
        self.aggregate_previous_rules(parse_list,
                                      ["VariableList", "VariableType", "Colon"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        # concatenate specific proceeding rules
        if rule == "VariableList":
            self.var_list = parse_info.var_list
        elif rule == "VariableType":
            self.var_type = parse_info

    def to_signature_string(self):
        """
        Creates a recursive unique string for this named variable declaration that
        does not depend on the variables' names but their type only and on how many there are declared.
        :return: A string that can used to distinguish signature overriding in FPL.
        """
        ret = str(len(self.var_list)) + ":"
        if self.var_type.generalType.mod is not None:
            ret += self.var_type.generalType.mod
        ret += self.var_type.generalType.id
        ret += "["
        if self.var_type.paramTuple is not None:
            first_found = False
            for named_var_decl in reversed(self.var_type.paramTuple.tuple):
                if not first_found:
                    ret += named_var_decl.to_signature_string()
                    first_found = True
                else:
                    ret += "," + named_var_decl.to_signature_string()
        ret += "]"
        return ret
