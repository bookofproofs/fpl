from poc.classes.AuxInbuiltTypes import InbuiltVariableVariadic
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVariableVariadic(AuxST, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.variadic_var, i)
        self.zto = ""
        self.zfrom = ""
        self.id = ""
        # this node is always associated with InbuiltVariableVariadic
        self.set_declared_type(InbuiltVariableVariadic(self))

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.outline

    def clone(self):
        other = self._copy(AuxSTVariableVariadic(self._i))
        other.id = self.id
        other._declared_type = self._declared_type
        return other

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline + "." + self.id
        return self._long_id
