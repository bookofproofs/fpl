from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search


class AuxSTConstructor(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.classConstructor, i)
        self.id = ""

    def get_declared_vars(self):
        # Class Constructor variables consist of:
        # class variables:
        declared_vars = ()
        # Note: Default constructors are omitted since they do not declare any variables
        # but still are called in the loop (otherwise we would cause double-listing of the same errors).
        if self.outline != AuxSymbolTable.classDefaultConstructor:
            var_spec_list_node = AuxSymbolTable.get_child_by_outline(self.parent.parent,
                                                                     AuxSymbolTable.var_spec)
            declared_vars += search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
            # constructor's variables (i.e. both, its signature and body)
            declared_vars += search.findall_by_attr(self, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
        return declared_vars
