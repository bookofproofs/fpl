from poc.classes.AuxAstInfo import AuxAstInfo

"""
The class AuxInterpretation is the base class of all semantical interpretations that are possible in FPL
"""


class AuxInterpretation:

    def __init__(self, ast_info: AuxAstInfo, errors: list):
        self._ast_info = ast_info
        # any errors from the caller. Classes inheriting from AuxInterpretation can add to to this list own errors.
        self._errors = errors  # a pointer to all the errors of the semantics, so we can add new errors to this list
        # internal semantical representation of the rule
        self.id = ""
        # some rules require stopping the aggregation of sub rules from the parse list after a certain
        # sub rule was aggregated. This flag will be set to true in the specific rule_aggregator implementation
        # of the class inheriting from AuxInterpretation
        self.stop_aggregation = False

    def rule_name(self):
        """ name of the corresponding grammar rule """
        return self._ast_info.rule

    def rule_pos(self):
        """ Current parsing position of the parsed  file (in characters) """
        return self._ast_info.pos

    def rule_col(self):
        """ Current parsing column in the parsed file """
        return self._ast_info.col

    def set_rule(self, rule:str):
        self._ast_info.rule = rule

    def rule_line(self):
        """ Current parsing line in the parsed file """
        return self._ast_info.line

    def clear_cst(self):
        """
        Once the interpretation has been determined, sets the field to None to save memory.
        """
        self._ast_info.cst = None

    def get_cst(self):
        """
        If the interpretation is not determined yet, the TatSu parsing context of the rule.
        Otherwise None.
        """
        return self._ast_info.cst

    def get_errors(self):
        return self._errors

    def get_ast_info(self):
        return self._ast_info

    def all_errors(self):
        return self._errors

    def __str__(self):
        return self._ast_info.rule + ":" + str(self._ast_info.pos) + ":(" + str(self._ast_info.line) + ":" + \
               str(self._ast_info.col) + "):" + str(self.id).replace("\n", "\\n")

    def __repr__(self):
        return self.__str__()

    def to_tuple(self):
        return str(type(self).__name__), str(self.id).replace("\n", "\\n"), self._ast_info.line, self._ast_info.col

    def aggregate_previous_rules(self, parse_list: list, aggr_rules: list, rule_aggregator):
        """
        Implements a generic aggregation method based on the current parse list
        :param parse_list: current parse list of the interpreter
        :param aggr_rules: rules that are expected in the parse_list that can be aggregated to the rue
        :param rule_aggregator: a function implemented in the class derived from AuxInterpretation that performs
        the actual aggregation
        :return: None
        """
        if len(parse_list) > 0:
            rule = parse_list[-1].rule_name()
            can_be_aggregated = rule in aggr_rules
            while can_be_aggregated and not self.stop_aggregation:
                rule_aggregator(rule, parse_list[-1])

                # remove the rule from the parse list after it was
                # handled by the rule_aggregator implemented in the subclass
                parse_list.pop()
                if len(parse_list) > 0:
                    rule = parse_list[-1].rule_name()
                    can_be_aggregated = rule in aggr_rules
                else:
                    can_be_aggregated = False
        # after the aggregation, we can clear the cst to free memory
        self.clear_cst()

    def rule_aggregator(self, rule: str, parsing_info):
        # this method must be implemented by classes derived from AuxInterpretation
        raise NotImplementedError

    @staticmethod
    def dispatch(i, parsing_info):
        # this method must be implemented by classes derived from AuxInterpretation
        raise NotImplementedError
