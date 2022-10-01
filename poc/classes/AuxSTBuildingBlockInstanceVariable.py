"""
The class AuxSTBuildingBlockInstanceVariable stores the type and a list of occurrences of the variable inside a block.
"""


class AuxSTBuildingBlockInstanceVariable:
    def __init__(self, occurrences: list, type_node):
        self.type_node = type_node.clone()
        self.occurrences = occurrences
