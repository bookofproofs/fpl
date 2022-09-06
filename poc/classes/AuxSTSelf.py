from poc.classes.AuxST import AuxST
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTTheory import AuxSTTheory
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTSelf(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.selfInstance, i)
        self.reference = None
        self.number_ats = 0
        self.id = AuxSymbolTable.selfInstance

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

    def get_declared_type(self):
        if self._declared_type is None:
            test_node = self
            maximum_reached = False
            at = 0
            while at <= self.number_ats and not maximum_reached:
                test_node = test_node.parent
                if isinstance(test_node, AuxSTBuildingBlock):
                    at += 1
                if isinstance(test_node.parent, AuxSTTheory):
                    maximum_reached = True
            declared_type = None
            if at > self.number_ats and not maximum_reached:
                # the test_node points to the intended node referenced by 'self'
                # also remember the node in the this qualified identifier
                declared_type = test_node

            if declared_type is None:
                declared_type = InbuiltUndefined()
            self._declared_type = declared_type
        return self._declared_type
