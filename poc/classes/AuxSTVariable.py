from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTVariable(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.var, i)
        self.id = ""
        self.zto = i.last_positions_by_rule['Variable'].pos_to_str()
        self.zfrom = i.corrected_position('IdStartsWithSmallCase')
        self._declared_type = None  # a pointer to the type in the symbol table with which this variable was declared
        self._is_bound = False
        self._is_initialized = False

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.id

    def clone(self):
        other = self._copy(AuxSTVariable(self._i))
        other.id = self.id
        other._is_bound = self._is_bound
        other._is_initialized = self._is_initialized
        return other

    def is_bound_or_initialized(self):
        return self._is_bound or self._is_initialized

    def set_is_bound(self):
        self._is_bound = True

    def evaluate(self, sem):
        sem.eval_stack[-1].value = self.get_declared_type().get_repr()


