from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSTConstructor import AuxSTConstructor
from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTTheory import AuxSTTheory


class AuxSTQualified(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.qualified, i)
        # the resolved_parent is the node in the symbol table that can possibly be identified
        # during the semantic analysis
        self._resolved_parent = None

    def to_string(self):
        ret = "dot["
        for child in self.children:
            ret += child.to_string()
        ret += "]"
        return ret

    def clone(self):
        my_copy = self._copy(AuxSTQualified(self._i))
        my_copy._resolved_parent = self._resolved_parent
        return my_copy

    def resolve_parent(self):
        if self._resolved_parent is None:
            # since this method is called the first time, we have first to initiate the _resolved_parent
            # using different approaches dependent on the type of self.parent
            if isinstance(self.parent, AuxSTSelf):
                # in case self.parent is an AuxSTSelf instance, we count the ats (e.g. two when @@self)
                # while trying to identify the right node in the symbol table referenced by that
                test_node = self
                maximum_reached = False
                at = 0
                while at <= self.parent.number_ats and not maximum_reached:
                    test_node = test_node.parent
                    if isinstance(test_node, (AuxSTInstance, AuxSTConstructor, AuxSTBlockWithSignature, AuxSTClass)):
                        at += 1
                    if isinstance(test_node.parent, AuxSTTheory):
                        maximum_reached = True
                if at > self.parent.number_ats and not maximum_reached:
                    # the test_node points to the intended node referenced by 'self'
                    self._resolved_parent = test_node
            elif isinstance(self.parent, AuxSTVariable):
                self._resolved_parent = self.parent.get_declared_type()
            elif isinstance(self.parent, AuxSTPredicateWithArgs):
                pass  # todo
            else:
                raise NotImplementedError(str(type(self.parent)))
        return self._resolved_parent
