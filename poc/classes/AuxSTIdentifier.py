from poc.classes.AuxSTNodeWithReference import AuxSTNodeWithReference
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTIdentifier(AuxSTNodeWithReference):

    def __init__(self, i):
        AuxSTNodeWithReference.__init__(self, AuxSTConstants.ids, i)
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
        other.reference = self.reference
        return other

