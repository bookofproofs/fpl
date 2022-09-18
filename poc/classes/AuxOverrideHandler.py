from poc.classes.AuxSTConstants import AuxSTConstants
from poc.fplerror import FplErrorManager
from poc.fplerror import FplAmbiguousSignature
from poc.fplerror import FplForbiddenOverride

"""
The AuxOverrideHandler class provides functionality to store building blocks with overriding signatures. 
"""


class AuxOverrideHandler:
    ALLOWED = True  # block type allows overriding signatures with the same identifier
    NOT_ALLOWED = False  # block type does not allow overriding signatures with the same identifier

    def __init__(self, mode: bool, error_mgr: FplErrorManager):
        self._mode = mode
        self._error_mgr = error_mgr
        self._dict = dict()

    def add(self, identifier, node, possible_duplicate):
        if identifier not in self._dict:
            self._dict[identifier] = list()
        self._dict[identifier].append(node)
        if possible_duplicate is not None:
            if self._mode == AuxOverrideHandler.ALLOWED:
                if possible_duplicate.reference.get_node_type_str() != node.reference.get_node_type_str():
                    # if the type of the possible_duplicate does not correspond to the type of the node,
                    # and the collection allows overrides, trigger an FplAmbiguousSignature error
                    self._error_mgr.add_error(
                        FplAmbiguousSignature(node, possible_duplicate)
                    )
                else:
                    # if the type of the possible_duplicate equals the type of the node,
                    # and the collection allows overrides, trigger an FplAmbiguousSignature error
                    if possible_duplicate != node and node.reference.outline != AuxSTConstants.classDefaultConstructor:
                        self._error_mgr.add_error(FplForbiddenOverride(node, possible_duplicate))

    def get(self, identifier):
        return self._dict[identifier]

    def keys(self):
        return self._dict.keys()

    def dictionary(self):
        return self._dict

    def identify_representative(self, identifier):
        """
        Identifies a representative based on the type of block
        :param identifier:
        :return:
        """
        if self._mode == AuxOverrideHandler.NOT_ALLOWED:
            # in case the block type does not allow overriding, it is ensured that there is only one representative
            return self._dict[identifier][0]
        elif self._mode == AuxOverrideHandler.ALLOWED:
            if len(self._dict[identifier]) == 1:
                # in case the block type allows overriding and there is only one candidate, return it
                return self._dict[identifier][0]
            else:
                raise AssertionError("More then ({0}) one representative possible".format(len(self._dict[identifier])))
        else:
            raise NotImplementedError(self._mode)
