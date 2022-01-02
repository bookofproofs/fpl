from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.classes.AuxSTClass import AuxSTClass


class AuxSTInstance(AuxSTBlock):
    def __init__(self, i):
        super().__init__(AuxSymbolTable.property, i)
        self.mandatory = False

    def get_declared_vars(self):
        """
        Calculates a tuple of variables declared in the scope of the node, including relevant variables in
        relevant outer scopes (like class variables).
        :return: tuple of declared variables.
        """
        declared_vars = ()
        if type(self.parent.parent) is AuxSTClass:
            # Predicate property variables of classes consist of:
            # class variables:
            var_spec_list_node = AuxSymbolTable.get_child_by_outline(self.parent.parent,
                                                                     AuxSymbolTable.var_spec)
            declared_vars += search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
            # and the own predicate instance variables (i.e. both, its signature and body)
            declared_vars += search.findall_by_attr(self, AuxSymbolTable.var_decl, AuxSymbolTable.outline)

        else:
            # Predicate property variables of non-classes (i.e. of predicates or of functional terms) consist of:
            # the parent's signature variables:
            signature_node = AuxSymbolTable.get_child_by_outline(self.parent.parent,
                                                                 AuxSymbolTable.signature)
            declared_vars += search.findall_by_attr(signature_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
            # the parent's variable specifications:
            var_spec_list_node = AuxSymbolTable.get_child_by_outline(self.parent.parent,
                                                                     AuxSymbolTable.var_spec)
            declared_vars += search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
            # and the own predicate instance variables (i.e. both, its signature and body)
            declared_vars += search.findall_by_attr(self, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
        return declared_vars