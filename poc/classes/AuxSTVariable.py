from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTVariable(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.var, i)
        self.id = ""
        self.zto = i.last_positions_by_rule['Variable'].pos_to_str()
        self.zfrom = i.corrected_position('IdStartsWithSmallCase')

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.id
