from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.fplerror import FplErrorManager
from poc.classes.AuxInbuiltTypes import InbuiltPredicate


class AuxSTProof(AuxSTBuildingBlock):

    def __init__(self, i):
        super().__init__(AuxSTConstants.block_proof, i)
        self.zfrom = i.corrected_position('ProofHeader')
        self.zto = i.last_positions_by_rule['Proof'].pos_to_str()
        self._referenced_theorem_like_stmt = None
        # Proofs are predicates per default
        self.set_declared_type(InbuiltPredicate(self))

    def set_referenced_theorem_like_stmt(self, node):
        self._referenced_theorem_like_stmt = node

    def get_referenced_theorem_like_stmt(self):
        return self._referenced_theorem_like_stmt

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        """
         Initializes the declared variables of the proof
         :return: None
         """
        if self._referenced_theorem_like_stmt is not None:
            # initialize the declared vars of the proof with all vars declared in its theorem-like statement
            self._declared_vars = self._referenced_theorem_like_stmt.get_declared_vars()

        # call the standard initialize_vars method
        super().initialize_vars(filename, error_mgr)

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined(self)
        self.set_sc_ready()
