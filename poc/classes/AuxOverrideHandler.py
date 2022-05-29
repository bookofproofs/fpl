from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplErrorManager
from poc.fplerror import FplAmbiguousSignature
from poc.fplerror import FplForbiddenOverride


"""
The AuxOverrideHandler class provides functionality to store building blocks with overriding signatures. 
"""


class AuxOverrideHandler:
    ALLOWED = True
    NOT_ALLOWED = False

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
                    if possible_duplicate != node and node.reference.outline != AuxSymbolTable.classDefaultConstructor:
                        self._error_mgr.add_error(FplForbiddenOverride(node, possible_duplicate))

    def get(self, identifier):
        return self._dict[identifier]

    def keys(self):
        return self._dict.keys()

    def dictionary(self):
        return self._dict
