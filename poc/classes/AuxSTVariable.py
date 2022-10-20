from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTNodeWithReference import AuxSTNodeWithReference
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVariable(AuxSTNodeWithReference):

    def __init__(self, i):
        AuxSTNodeWithReference.__init__(self, AuxSTConstants.var, i)
        self.zto = i.last_positions_by_rule['Variable'].pos_to_str()
        self.zfrom = i.corrected_position('IdStartsWithSmallCase')
        self._is_bound = False
        self._is_initialized = False

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.id

    def clone(self):
        other = self._copy(AuxSTVariable(self._i))
        other.id = self.id
        other._is_bound = self._is_bound
        other._is_initialized = self._is_initialized
        return other

    def is_bound_or_initialized(self):
        return self._is_bound or self._is_initialized

    def set_is_bound(self):
        self._is_bound = True

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def get_declared_type(self):
        if self._declared_type is None:
            minor_scope = self.get_minor_scope()
            declared_vars = minor_scope.get_declared_vars()
            if self.id in declared_vars:
                self._declared_type = declared_vars[self.id].children[0]
            else:
                self._declared_type = InbuiltUndefined(self)
        return self._declared_type
