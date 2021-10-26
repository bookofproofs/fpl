from poc.classes.AuxContext import AuxContext
from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInterpretation import AuxInterpretation

"""
Implements an interface between the classes named Context<Something> and the class FPLSourceAnalyser
"""


class AuxISourceAnalyser:
    verbose = False  # True <=> verbose mode

    def __init__(self, errors: list, root: AnyNode, theory_name: str):
        """
        Creates a new interface between the classes named Context<Something> and the class FPLSourceAnalyser
        :param errors: a pointer to the errors of the FPL interpreter
        :param root: a pointer to the root (cross-theory) node of the symbol table of the FPL interpreter
        :param theory_name: the name of the current theory being interpreted
        """
        self.context = AuxContext()  # the current context of the source analysis
        self.parse_list = []  # a stack for bottom-up aggregation of parsed FPL source code productions
        self.errors = errors  # any errors of the FPL interpreter
        self.theory_node = AuxSymbolTable.add_or_get_theory(root, theory_name)  # root node of the current theory
        # A stack for AnyTree nodes of the symbol table being built in the specific context.
        # contains, typically the running AnyNodes for definitions, theorems, classes, constructors, or even variables.
        self._node_stack = []

    def get_debug_parsing_info(self, parsing_info: AuxInterpretation):
        if self.verbose:
            return str(parsing_info)
        else:
            return None

    def touch_node(self):
        if len(self._node_stack) == 0:
            # this error indicates an asynchronous logic in using the node
            raise AssertionError("Cannot retrieve value of node, stack empty.")
        if self.verbose:
            print("node stack (touch): " + self._str_node_stack())
        return self._node_stack[-1]

    def pop_node(self):
        if len(self._node_stack) == 0:
            # this error indicates an asynchronous logic in using the node
            raise AssertionError("Cannot pop node, stack empty.")
        if self.verbose:
            print("node stack (pop): " + self._str_node_stack())
        return self._node_stack.pop()

    def push_node(self, node: AnyNode):
        self._node_stack.append(node)
        if self.verbose:
            print("node stack (push): " + self._str_node_stack())

    def _str_node_stack(self):
        ret = []
        for node in reversed(self._node_stack):
            d = dict()
            if node is not None:
                d["id"] = node.id
                d["outline"] = node.outline
                d["l"] = node.info.line
                d["c"] = node.info.col
                ret.append(d)
            else:
                # None nodes can occur during the syntax analysis process, for instance,
                # if we could not create a constructor of a class, because it was misspelled by the user.
                # in this case, we avoid errors when attempting to access non-existing object attributes
                pass
        return str(ret)
