from anytree import AnyNode


class AuxSTGlobal(AnyNode):

    def __init__(self, parent: AnyNode, gid: str, block: AnyNode):
        super().__init__()
        self.parent = parent
        self.reference = block
        self.gid = gid
        self.id = block.get_relative_id()
