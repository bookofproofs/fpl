from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxPredicate(AnyNode):

    def __init__(self, p_type: str):
        super().__init__()
        self.type = p_type
        self._bound_vars = dict()
        self._is_asserted = False
        self._is_revoked = False
        self._exist_number = -1

    def assert_predicate(self):
        self._is_asserted = True

    def revoke_predicate(self):
        self._is_asserted = False
        self._is_revoked = True

    def register_reference(self, reference: AnyNode):
        self.reference = reference  # noqa

    def register_referenced_type(self, referenced_type: AnyNode):
        self.referenced_type = referenced_type  # noqa

    def get_reference(self):
        return self._reference

    def get_referenced_type(self):
        return self._referenced_type

    def register_child(self, predicate: AnyNode):
        if type(predicate) is not AuxPredicate and type(predicate) is not AnyNode:
            raise TypeError("Argument type was {0}, must be AuxPredicate or AnyNode".format(str(type(predicate))))
        predicate.parent = self

    def set_exists_number(self, number: int):
        self._exist_number = number

    def get_exists_number(self):
        return self._exist_number

    def bind_var(self, variable_node: AnyNode):
        self._bound_vars[variable_node.id] = variable_node

    def get_bound_vars(self):
        return self._bound_vars

    def get_predicate_value(self):
        if self._is_asserted:
            return True
        elif self._is_revoked:
            return False
        else:
            if self.type == AuxSymbolTable.predicate_true:
                return True
            elif self.type == AuxSymbolTable.predicate_false:
                return False
            elif self.type == AuxSymbolTable.predicate_negation:
                return not self.children[0].get_predicate_value()
            elif self.type == AuxSymbolTable.predicate_conjunction:
                ret = True
                for child in self.children:
                    ret = ret and child.get_predicate_value()
                    if not ret:
                        break
                return ret
            elif self.type == AuxSymbolTable.predicate_disjunction:
                ret = False
                for child in self.children:
                    ret = ret or child.get_predicate_value()
                    if ret:
                        break
                return ret
            elif self.type == AuxSymbolTable.predicate_equivalence:
                p = self.children[0].get_predicate_value()
                q = self.children[1].get_predicate_value()
                return p == q
            elif self.type == AuxSymbolTable.predicate_exclusiveOr:
                p = self.children[0].get_predicate_value()
                q = self.children[1].get_predicate_value()
                return (p and not q) or (q and not p)
            elif self.type == AuxSymbolTable.predicate_implication:
                p = self.children[0].get_predicate_value()
                q = self.children[1].get_predicate_value()
                return not p or q
            else:
                raise NotImplementedError(self.type)
