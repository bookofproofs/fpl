from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate


class AuxSTStatement(AuxST):

    def __init__(self, statement_type: str, i):
        super().__init__(AuxSymbolTable.statement, i)
        self.type = statement_type
        if statement_type == AuxSymbolTable.statement_is:
            self.zfrom = i.corrected_position('is')
            self.zto = i.last_positions_by_rule['IsOperator'].pos_to_str()
            # the is operator is a predicate
            self.set_declared_type(InbuiltPredicate(self))
        elif statement_type == AuxSymbolTable.statement_assert:
            self.zfrom = i.corrected_position('assert')
            self.zto = i.last_positions_by_rule['AssertionStatement'].pos_to_str()
            # the assert statement is a predicate
            self.set_declared_type(InbuiltPredicate(self))
        elif statement_type == AuxSymbolTable.statement_assign:
            self.zfrom = i.corrected_position('Assignee')
            self.zto = i.last_positions_by_rule['AssignmentStatement'].pos_to_str()
            # the assert statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.statement_loop:
            self.zfrom = i.corrected_position('loop')
            self.zto = i.last_positions_by_rule['LoopStatement'].pos_to_str()
            # the loop statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.statement_return:
            self.zfrom = i.corrected_position('ReturnHeader')
            self.zto = i.last_positions_by_rule['ReturnStatement'].pos_to_str()
            # the return statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.statement_range:
            self.zfrom = i.corrected_position('range')
            self.zto = i.last_positions_by_rule['RangeStatement'].pos_to_str()
            # the range statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.statement_py:
            self.zfrom = i.corrected_position('py')
            self.zto = i.last_positions_by_rule['PythonDelegate'].pos_to_str()
            # the py statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.case_default:
            self.zfrom = i.corrected_position('else')
            self.zto = i.last_positions_by_rule['DefaultResult'].pos_to_str()
            # the case default statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.cases:
            self.zfrom = i.corrected_position('case')
            self.zto = i.last_positions_by_rule['CaseStatement'].pos_to_str()
            # the cases statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        elif statement_type == AuxSymbolTable.case:
            self.zfrom = i.corrected_position('Predicate')
            self.zto = i.last_positions_by_rule['ConditionFollowedByResult'].pos_to_str()
            # the case statement is a undefined
            self.set_declared_type(InbuiltUndefined(self))
        else:
            raise NotImplementedError(statement_type)

    def clone(self):
        return AuxSTStatement(self.type, self._i)

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined(self)
