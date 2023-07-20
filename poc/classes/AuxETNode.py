from anytree import AnyNode
from enum import Enum, auto

"""
The AuxETNode class defines a single node of the Evaluation Tree.
The idea of the Evaluation Tree is to provide a by-design tree structure to storage what is in the 
current (as of version 1.10.18) implementation being stored in the lineare stack data structure  

We want to use the new data structure to refactor and redesign the FPL evaluation process currently based on 
many ugly classes like in particular AuxSTBuildingBlockInstanceHandler, AuxeEvaluation, AuxEvaluationRegister, etc. 
"""


class AuxETOutlineNodeType(Enum):
    """ Possible types of AuxETOutlineNode """
    ROOT = auto()
    VERIFIED_EXPRESSIONS = auto()
    VARS = auto()
    DEFINITIONS = auto()
    VERIFIED_PREDICATES = auto()
    CONJECTURED_PREDICATES = auto()


class AuxETRegisterNodeType(Enum):
    """ Possible types of AuxETNode """
    EXPRESSION = auto()
    VAR_VARIADIC = auto()
    VAR = auto()
    VAR_INDEX = auto()
    INSTANCE = auto()


""" 
Basic structure of an outline node of the Evaluation Tree 
"""


class AuxETOutlineNode(AnyNode):
    def __init__(self, node_type: AuxETOutlineNodeType, parent: AnyNode):
        self.parent = parent
        self.type = node_type


"""
Basic structure of a node containing some additional meta information in the Evaluation Tree
"""


class AuxETNode(AuxETOutlineNode):
    def __init__(self, node_type: AuxETRegisterNodeType, parent: AnyNode, symbol_table_node: AnyNode):
        AuxETOutlineNode.__init__(self, node_type, parent)
        self.st_node = symbol_table_node


"""
AuxETNodeVarVariadic is a basic subtype of AuxETNode containing evaluation information specific for variadic variables
"""


class AuxETNodeVarVariadic(AuxETNode):

    def __init__(self, node_type: AuxETRegisterNodeType, parent: AnyNode, symbol_table_node: AnyNode,
                 at_least_one: bool):
        AuxETNode.__init__(self, node_type, parent, symbol_table_node)
        self.length = 0
        self.min_length = int(at_least_one)
        # AuxETNodeVarVariadic have no subnodes, might become some during the evaluation process.
        # In this case, it will be a list of variables of the same type belonging to the variadic variable


"""
AuxETNodeVarIndex is a basic subtype of AuxETNode containing evaluation information specific for index variables
"""


class AuxETNodeVarIndex(AuxETNode):
    def __init__(self, node_type: AuxETRegisterNodeType, parent: AnyNode, symbol_table_node: AnyNode,
                 index_value: int):
        AuxETNode.__init__(self, node_type, parent, symbol_table_node)
        self.index_value = index_value
        # AuxETNodeVarIndex have no subnodes


"""
AuxETFplTyped is a basic subtype of AuxETNode containing evaluation information specific for nodes 
for which a specific Fpl Type is expected and that might return an evaluation error when some another type 
than the expected one is established.

The AuxETFplTyped nodes contain information necessary for the evaluation of:
* variables other than variadic and index variables
* building blocks of FPL (i.e. definitions, theorem-like statements, proofs, axioms, and conjectures) 
"""


class AuxETFplTyped(AuxETNode):
    def __init__(self, node_type: AuxETRegisterNodeType, parent: AnyNode, symbol_table_node: AnyNode,
                 expected_type: AnyNode):
        AuxETNode.__init__(self, node_type, parent, symbol_table_node)
        self.expected_type = expected_type
        self.evaluation_error = ""  # empty string no error
        # FplTyped nodes have always these three outline subnodes
        AuxETOutlineNode(AuxETOutlineNodeType.VERIFIED_PREDICATES, self)
        AuxETOutlineNode(AuxETOutlineNodeType.CONJECTURED_PREDICATES, self)
        AuxETOutlineNode(AuxETOutlineNodeType.VARS, self)
        AuxETOutlineNode(AuxETOutlineNodeType.VERIFIED_EXPRESSIONS, self)


class AuxETFplRoot(AuxETOutlineNode):

    def __init__(self):
        AuxETOutlineNode.__init__(self, AuxETOutlineNodeType.ROOT, None)  # the root has no parent
        # the AuxETFplRoot has always these three outline subnodes
        AuxETOutlineNode(AuxETOutlineNodeType.VERIFIED_PREDICATES, self)
        AuxETOutlineNode(AuxETOutlineNodeType.CONJECTURED_PREDICATES, self)
        AuxETOutlineNode(AuxETOutlineNodeType.DEFINITIONS, self)
