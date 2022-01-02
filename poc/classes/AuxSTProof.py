from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search


class AuxSTProof(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_proof, i)
        self.zfrom = i.corrected_position('ProofHeader')
        self.zto = i.last_positions_by_rule['Proof'].pos_to_str()

    def get_declared_vars(self):
        """
        Calculates a tuple of variables declared in the scope of the node.
        :return: tuple of declared variables.
        """
        # Class variables only (i.e. do not consider the sub-scopes of constructors and properties)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.var_spec)
        return search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
