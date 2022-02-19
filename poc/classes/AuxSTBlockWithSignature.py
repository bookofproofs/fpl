from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.classes.AuxSTClass import AuxSTClass


class AuxSTBlockWithSignature(AuxSTBlock):
    def __init__(self, property_type: str, i):
        super().__init__(property_type, i)


