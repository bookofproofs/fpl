from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxPos import AuxPos
from poc.fplerror import FplErrorManager

"""
The class AuxInterpretation is the base class of all semantical interpretations that are possible in FPL
"""


class AuxInterpretation:

    def __init__(self, ast_info: AuxAstInfo, error_mgr: FplErrorManager):
        self._ast_info = ast_info
        # any errors from the caller. Classes inheriting from AuxInterpretation can add to to this list own errors.
        self._error_mgr = error_mgr  # a pointer to all the error manager of the semantics
        # internal semantical representation of the rule
        self.id = ""
        self.zto = AuxPos()
        self.zfrom = AuxPos()
        self.zto.col = self.zfrom.col = ast_info.col + 1
        self.zto.line = self.zfrom.line = ast_info.line
        self.zto.pos = self.zfrom.pos = ast_info.pos + 1
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

    def set_rule(self, rule: str):
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

    def get_error_mgr(self):
        return self._error_mgr

    def get_ast_info(self):
        return self._ast_info

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
        :param parse_list: current parse list of the transformer
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
        if type(self.get_cst()) is not str:
            self.clear_cst()

    def rule_aggregator(self, rule: str, parsing_info):
        # this method must be implemented by classes derived from AuxInterpretation
        raise NotImplementedError

    @staticmethod
    def dispatch(i, parsing_info):
        # this method must be implemented by classes derived from AuxInterpretation
        raise NotImplementedError
