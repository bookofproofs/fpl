from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextNamedVariableDeclaration(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.var_list = None
        self.var_type = None
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["NamedVariableDeclaration"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "VariableList":
            self.var_list = parsing_info.var_list  # noqa
        elif rule == "VariableType":
            self.var_type = parsing_info

    def to_string(self):
        """
        Creates a recursive unique string for this named variable declaration that
        does not depend on the variables' names but their type only and on how many of them there are declared.
        :return: A string that can be used to distinguish signature overriding in FPL.
        """
        ret = str(len(self.var_list)) + ":"
        if self.var_type.generalType.type_mod is not None:
            ret += self.var_type.generalType.type_mod
        ret += self.var_type.generalType.to_string()
        if self.var_type.paramTuple is not None:
            ret += "["
            first_found = False
            for named_var_declaration in self.var_type.paramTuple.tuple:
                if not first_found:
                    ret += named_var_declaration.to_string()
                    first_found = True
                else:
                    ret += "," + named_var_declaration.to_string()
            ret += "]"
        return ret

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextNamedVariableDeclaration(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
