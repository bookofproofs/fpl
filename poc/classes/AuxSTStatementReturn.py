from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTTypeInterface import AuxSTTypeInterface
from poc.fplerror import FplInvalidUseReturnStmt


class AuxSTStatementReturn(AuxSTStatement, AuxSTTypeInterface):
    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_return, i)
        self.zfrom = i.corrected_position('ReturnHeader')
        self.zto = i.last_positions_by_rule['ReturnStatement'].pos_to_str()

    def clone(self):
        return AuxSTStatementReturn(self._i)

    def get_declared_type(self):
        if self._declared_type is None:
            # the declared type of the return statement is the type of the functional term it is part of
            minor_scope = self.get_minor_scope()
            if hasattr(minor_scope, "def_type") and minor_scope.def_type in [AuxSTConstants.functionalTerm,
                                                                             AuxSTConstants.functionalTermInstance]:
                self.set_declared_type(minor_scope.get_declared_type())
                return
            else:
                # in all other cases, a return statement is invalid
                self._i.errors.add_error(FplInvalidUseReturnStmt(self))
                # and the declared type is undefined
                self.set_declared_type(InbuiltUndefined(self))
        return self._declared_type

    def evaluate(self, sem):
        raise NotImplementedError()
