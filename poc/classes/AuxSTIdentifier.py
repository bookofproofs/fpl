from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTIdentifier(AuxST, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.ids, i)
        self.reference = None
        self.zto = ""
        self.zfrom = ""
        self.id = ""

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.outline

    def clone(self):
        other = self._copy(AuxSTIdentifier(self._i))
        other.id = self.id
        other._declared_type = self._declared_type
        return other

    def evaluate(self, sem):
        if self.reference is None:
            if self._try_to_determine_reference(sem):
                self.set_declared_type(self.reference.get_declared_type())
            else:
                self.set_declared_type(InbuiltUndefined(self))
        sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline
        return self._long_id

    def _try_to_determine_reference(self, sem):
        qualified_identifier = self.get_qualified_id()
        if qualified_identifier in sem.overridden_qualified_ids.dictionary():
            possible_overrides = sem.overridden_qualified_ids.get(qualified_identifier)
            self.reference = possible_overrides[0]
            return True
        return False
