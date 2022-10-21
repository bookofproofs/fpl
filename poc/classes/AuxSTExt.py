from poc.classes.AuxST import AuxST


class AuxSTExt(AuxST):
    def __init__(self, extension_id, i):
        super().__init__(extension_id, i)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline + "." + self.id
        return self._long_id

    def evaluate(self, sem):
        raise NotImplementedError()


