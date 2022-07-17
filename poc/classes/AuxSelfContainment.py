from anytree import AnyNode


class AuxReferenceType:
    logical = 0
    semantical = 1


class AuxReference:
    def __init__(self, predecessor: AnyNode, successor: AnyNode, reference_type: AuxReferenceType):
        self.predecessor = predecessor
        self.successor = successor
        self.type = reference_type
        self.source_fpl_file = "not found"

    def __eq__(self, other):
        return self.predecessor == other.predecessor and self.successor == other.successor

    def __str__(self):
        if self.type == 1:
            # semantical inference
            self.predecessor.id + "-s>" + self.successor.id
        else:
            # logical inference
            self.predecessor.id + "-l>" + self.successor.id

    def __hash__(self):
        return id(self)


class AuxSelfContainment:
    def __init__(self):
        self._refs = set()  # set of all references
        self._predecessors = dict()  # lists all predecessors where the values are sets of all successors of each
        self._successors = dict()  # lists all successors where the values are sets of all predecessors of each

    def add_reference(self, predecessor: AnyNode, successor: AnyNode, reference_type: AuxReferenceType):
        new = AuxReference(predecessor, successor, reference_type)
        if new in self._refs:
            AssertionError("The reference " + str(new) + "already exists.")
        else:
            if predecessor not in self._predecessors:
                self._predecessors[predecessor] = set()
                self._predecessors[predecessor].add(successor)
            elif successor not in self._predecessors[predecessor]:
                self._predecessors[predecessor].add(successor)
            if successor not in self._successors:
                self._successors[successor] = set()
                self._successors[successor].add(predecessor)
            elif predecessor not in self._successors[successor]:
                self._successors[successor].add(predecessor)

    def collect_roots(self):
        return self._predecessors - self._successors

    def collect_leaves(self):
        return self._successors - self._predecessors

    def get_predecessors(self, node):
        ret = set()
        if node in self._successors:
            ret += self._successors[node]
        return ret

    def get_successors(self, node):
        ret = set()
        if node in self._predecessors:
            ret += self._predecessors[node]
        return ret

    def get_refs(self):
        return self._refs
