from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTTheory(AuxSTOutline):

    def __init__(self, parent: AuxSTOutline, file_name: str):
        super().__init__(parent, AuxSymbolTable.theory)
        self.file_name = file_name
        AuxSTOutline(parent=self, outline=AuxSymbolTable.uses)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_axiom_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_ir_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_def_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_thm_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_lem_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_prop_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_conj_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_cor_root)
        AuxSTOutline(parent=self, outline=AuxSymbolTable.block_proof_root)
