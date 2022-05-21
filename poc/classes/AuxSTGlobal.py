from anytree import AnyNode
import re


class AuxSTGlobal(AnyNode):

    def __init__(self, parent: AnyNode, gid: str, block: AnyNode, theory_node: AnyNode):
        super().__init__()
        self.parent = parent
        self.reference = block
        self.gid = gid
        self.id = block.get_relative_id()
        self.theory = theory_node
        self._qualified_id = None

    def get_qualified_id(self):
        if self._qualified_id is None:
            self._qualified_id = re.sub(r"\[([0-9,\+\*\[\]:a-zA-Z_\$]*)\]", "", self.id)
        return self._qualified_id
