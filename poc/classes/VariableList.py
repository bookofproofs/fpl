from classes.AuxInterpretation import AuxInterpretation
import fplerror

# The list has the following meaning:
#   As long as the proceeding rules of VariableList is one of the list elements,
#   they will be removed from the parse_list and the interpretation of the VariableList will be
#   replaced by the object VariableList
aggr_rules_VariableList = {'Variable', 'Comma', 'IW', 'Entity', 'Assignee'}


class VariableList(AuxInterpretation):
    __set = None

    def __init__(self, parse_list: list, inter: AuxInterpretation):
        self.clone(inter)
        self.__set = set()

        can_be_ignored = parse_list[-1].rule_name() in aggr_rules_VariableList
        while can_be_ignored:
            if parse_list[-1].rule_name() == "Variable":
                self.add(parse_list[-1].get_interpretation())
            # remove ignored rule
            parse_list.pop()
            if len(parse_list) > 0:
                can_be_ignored = parse_list[-1].rule_name() in aggr_rules_VariableList
            else:
                can_be_ignored = False
        self.set_interpretation(self.__set)

    def add(self, var_name):
        if var_name in self.__set:
            self.all_errors().append(fplerror.FplVariableDuplicateInVariableList(self, var_name))
        else:
            self.__set.add(var_name)

    def get_value(self):
        return self.__set
