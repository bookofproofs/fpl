from poc.classes.AuxST import AuxST


class AuxSTStatement(AuxST):

    def __init__(self, statement_type: str, i):
        super().__init__(statement_type, i)
        self._statement_type = statement_type

    def evaluate(self, sem):
        raise NotImplementedError(str(type(self)))

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self._statement_type
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id
