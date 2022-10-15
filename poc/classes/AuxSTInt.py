from poc.classes.AuxInbuiltTypes import InbuiltInt
from poc.classes.AuxInbuiltValues import InbuiltValueInteger
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTInt(AuxST, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.int, i)
        self.zto = ""
        self.zfrom = ""
        self.id = ""
        self.set_declared_type(InbuiltInt(self))

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.outline

    def clone(self):
        other = self._copy(AuxSTInt(self._i))
        other.id = self.id
        other._declared_type = self._declared_type
        return other

    def evaluate(self, sem):
        new_value = InbuiltValueInteger(self)
        new_value.set_value(self.id)
        sem.eval_stack[-1].value = new_value

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline + self.id
        return self._long_id
