from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTTheory(AuxSTOutline):

    def __init__(self, parent: AuxSTOutline, file_name: str):
        super().__init__(parent, AuxSTConstants.theory)
        self.file_name = file_name
        self.namespace = AuxSTConstants.undefined
        AuxSTOutline(parent=self, outline=AuxSTConstants.uses)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_axiom_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_ir_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_def_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_thm_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_lem_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_prop_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_conj_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_cor_root)
        AuxSTOutline(parent=self, outline=AuxSTConstants.block_proof_root)
