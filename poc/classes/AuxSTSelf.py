from poc.classes.AuxInbuiltValues import InbuiltValueUndefined
from poc.classes.AuxSTNodeWithReference import AuxSTNodeWithReference
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTSelf(AuxSTNodeWithReference):

    def __init__(self, i):
        AuxSTNodeWithReference.__init__(self, AuxSTConstants.selfInstance, i)
        self.number_ats = 0
        self.id = AuxSTConstants.selfInstance

    def to_string(self):
        ret = "@" * self.number_ats + "self"
        for child in self.children:
            ret += child.to_string()
        return ret

    def clone(self):
        other = self._copy(AuxSTSelf(self._i))
        other.number_ats = self.number_ats
        other.id = self.id
        return other

    def get_qualified_id(self):
        if self._qualified_id is None:
            self._establish_reference()
            self._qualified_id = self.reference.get_qualified_id()
        return self._qualified_id

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def _establish_reference(self):
        if self.reference is None:
            if self.number_ats == 0:
                self.reference = self.get_minor_scope()
            elif self.number_ats == 1:
                self.reference = self.get_scope()
            else:
                # the FPL syntax does not allow nesting more than one building block
                # in each other. The number of @ can, therefore, be only <=1
                self.reference = InbuiltValueUndefined(self)
                # todo: add a new Fpl Error type
                raise NotImplementedError()

    def get_declared_type(self):
        if self._declared_type is None:
            self._establish_reference()
            self._declared_type = self.reference.get_declared_type()
        return self._declared_type
