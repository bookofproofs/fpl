from anytree import AnyNode, RenderTree
from poc.classes.AuxInbuiltTypes import InbuiltIndex

"""
The AuxETNode class defines a single node of the Evaluation Tree.
The idea of the Evaluation Tree is to provide a by-design tree structure to storage what is in the 
current (as of version 1.10.18) implementation being stored in the lineare stack data structure  

We want to use the new data structure to refactor and redesign the FPL evaluation process currently based on 
many ugly classes like in particular AuxSTBuildingBlockInstanceHandler, AuxeEvaluation, AuxEvaluationRegister, etc. 
"""

""" 
Basic structure of an outline node of the Evaluation Tree 
"""


class AuxETOutlineNode(AnyNode):
    def __init__(self, parent: AnyNode):
        self.parent = parent

    @staticmethod
    def to_string(root_node):
        return str(RenderTree(root_node)).strip()


class AuxETOutlineVars(AuxETOutlineNode):
    def __init__(self, parent: AnyNode):
        super().__init__(parent)


class AuxETOutlineVerifiedExpressions(AuxETOutlineNode):
    def __init__(self, parent: AnyNode):
        super().__init__(parent)


class AuxETOutlineDefinitions(AuxETOutlineNode):
    def __init__(self, parent: AnyNode):
        super().__init__(parent)


class AuxETOutlineVerifiedPredicates(AuxETOutlineNode):
    def __init__(self, parent: AnyNode):
        super().__init__(parent)


class AuxETOutlineConjecturedPredicates(AuxETOutlineNode):
    def __init__(self, parent: AnyNode):
        super().__init__(parent)


class AuxETOutlineRoot(AuxETOutlineNode):
    def __init__(self):
        super().__init__(None)  # the root has no parent
        AuxETOutlineVerifiedPredicates(self)
        AuxETOutlineConjecturedPredicates(self)
        AuxETOutlineDefinitions(self)


"""
Basic structure of a node containing some additional meta information in the Evaluation Tree
"""


class AuxETNode(AuxETOutlineNode):
    def __init__(self, parent: AnyNode, symbol_table_node: AnyNode):
        AuxETOutlineNode.__init__(self, parent)
        self._st_node = symbol_table_node
        self.a_id = symbol_table_node.gid if hasattr(symbol_table_node, "gid") else symbol_table_node.get_long_id()

    def get_st_node_object(self):
        return self._st_node


"""
AuxETNodeVarVariadic is a basic subtype of AuxETNode containing evaluation information specific for variadic variables
"""


class AuxETNodeVarVariadic(AuxETNode):

    def __init__(self, parent: AnyNode, symbol_table_node: AnyNode,
                 at_least_one: bool):
        AuxETNode.__init__(self, parent, symbol_table_node)
        self.length = 0
        self.min_length = int(at_least_one)
        # AuxETNodeVarVariadic have no subnodes, might become some during the evaluation process.
        # In this case, it will be a list of variables of the same type belonging to the variadic variable


"""
AuxETValue is a subclass wrapping around values with different actual types  
"""


class AuxETValue(AuxETOutlineNode):
    def __init__(self, parent: AnyNode, actual_type):
        AuxETOutlineNode.__init__(self, parent)
        self._actual_type = actual_type
        self.actual_type = self._actual_type.get_long_id()

    def get_actual_type_object(self):
        return self._actual_type

    def get_value(self):
        """ Subclasses have to implement this method """
        raise NotImplementedError()


class AuxETIndexValue(AuxETValue):
    def __init__(self, parent, actual_type):
        AuxETValue.__init__(parent, actual_type)
        self.value = None

    def get_value(self):
        """ The value of an FPL index is just the value attribute of the class """
        return self.value


"""
AuxETNodeVarIndex is a basic subtype of AuxETNode containing evaluation information specific for index variables
"""


class AuxETNodeVarIndex(AuxETNode):
    def __init__(self, parent: AnyNode, symbol_table_node: AnyNode,
                 index_value: int):
        AuxETNode.__init__(self, parent, symbol_table_node)
        # AuxETNodeVarIndex has a single subnode wrapping around its integer valur
        child = AuxETIndexValue(self, InbuiltIndex(symbol_table_node))
        child.value = index_value



"""
AuxETFplTyped is a basic subclass of AuxETNode containing evaluation information specific for nodes 
for which a specific Fpl Type is expected and that might return an evaluation error when some another type 
than the expected one is established.

The AuxETFplTyped nodes contain information necessary for the evaluation of:
* variables other than variadic and index variables
* building blocks of FPL (i.e. definitions, theorem-like statements, proofs, axioms, and conjectures) 
"""


class AuxETFplTyped(AuxETNode):
    def __init__(self, parent: AnyNode, symbol_table_node: AnyNode,
                 expected_type: AnyNode):
        AuxETNode.__init__(self, parent, symbol_table_node)
        self._expected_type = expected_type
        self.b_expected_type = expected_type.get_long_id()
        self.c_evaluation_error = ""  # empty string no error
        # FplTyped nodes have always these three outline subnodes
        AuxETOutlineVerifiedPredicates(self)
        AuxETOutlineConjecturedPredicates(self)
        AuxETOutlineVars(self)
        AuxETOutlineVerifiedExpressions(self)

    def get_expected_type_object(self):
        return self._expected_type
