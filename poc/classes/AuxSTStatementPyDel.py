from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTStatementPyDel(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_py, i)
        self.zfrom = i.corrected_position('py')
        self.zto = i.last_positions_by_rule['PythonDelegate'].pos_to_str()

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self._statement_type + "." + self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def clone(self):
        return AuxSTStatementPyDel(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()