from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTStatement(AuxST):

    def __init__(self, statement_type: str, i):
        super().__init__(AuxSymbolTable.statement, i)
        self.type = statement_type
        if statement_type == AuxSymbolTable.statement_is:
            self.zfrom = i.corrected_position('is')
            self.zto = i.last_positions_by_rule['IsOperator'].pos_to_str()
        elif statement_type == AuxSymbolTable.statement_assert:
            self.zfrom = i.corrected_position('assert')
            self.zto = i.last_positions_by_rule['AssertionStatement'].pos_to_str()
        elif statement_type == AuxSymbolTable.statement_assign:
            self.zfrom = i.corrected_position('Assignee')
            self.zto = i.last_positions_by_rule['AssignmentStatement'].pos_to_str()
        elif statement_type == AuxSymbolTable.statement_loop:
            self.zfrom = i.corrected_position('loop')
            self.zto = i.last_positions_by_rule['LoopStatement'].pos_to_str()
        elif statement_type == AuxSymbolTable.statement_return:
            self.zfrom = i.corrected_position('ReturnHeader')
            self.zto = i.last_positions_by_rule['ReturnStatement'].pos_to_str()
        elif statement_type == AuxSymbolTable.statement_range:
            self.zfrom = i.corrected_position('range')
            self.zto = i.last_positions_by_rule['RangeStatement'].pos_to_str()
        elif statement_type == AuxSymbolTable.statement_py:
            self.zfrom = i.corrected_position('py')
            self.zto = i.last_positions_by_rule['PythonDelegate'].pos_to_str()
        elif statement_type == AuxSymbolTable.case_default:
            self.zfrom = i.corrected_position('else')
            self.zto = i.last_positions_by_rule['DefaultResult'].pos_to_str()
        elif statement_type == AuxSymbolTable.cases:
            self.zfrom = i.corrected_position('case')
            self.zto = i.last_positions_by_rule['CaseStatement'].pos_to_str()
        elif statement_type == AuxSymbolTable.case:
            self.zfrom = i.corrected_position('Predicate')
            self.zto = i.last_positions_by_rule['ConditionFollowedByResult'].pos_to_str()
        else:
            raise NotImplementedError(statement_type)

    def clone(self):
        return AuxSTStatement(self.type, self._i)
