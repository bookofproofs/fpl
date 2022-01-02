from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.classes.AuxSTClass import AuxSTClass


class AuxSTBlockWithSignature(AuxSTBlock):
    def __init__(self, property_type: str, i):
        super().__init__(property_type, i)

    def get_declared_vars(self):
        """
        Calculates a tuple of variables declared in the scope of the node, including relevant variables in
        relevant outer scopes (like class variables).
        :return: tuple of declared variables.
        """
        # for blocks with signatures, limit the declared vars to those in the signature + variable specification
        # (i.e. do not consider the sub-scopes of properties)
        signature_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.signature)
        declared_vars = search.findall_by_attr(signature_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.var_spec)
        declared_vars += search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
        return declared_vars
