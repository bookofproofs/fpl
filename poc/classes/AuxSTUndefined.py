from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxInbuiltValues import InbuiltValueUndefined
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTUndefined(AuxST, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.undefined, i)
        self.zto = i.last_positions_by_rule['UndefinedHeader'].pos_to_str()
        self.zfrom = i.corrected_position('UndefinedHeader')
        self.set_declared_type(InbuiltUndefined(self))

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.outline

    def clone(self):
        other = self._copy(AuxSTUndefined(self._i))
        other._declared_type = self._declared_type
        return other

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltValueUndefined(self)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline
        return self._long_id
