from poc.classes.AuxContext import AuxContext
from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInterpretation import AuxInterpretation

"""
Implements an interface between the classes named Context<Something> and the class FPLSourceAnalyser
"""


class AuxISourceAnalyser:

    def __init__(self, errors: list, root: AnyNode, theory_name: str):
        """
        Creates a new interface between the classes named Context<Something> and the class FPLSourceAnalyser
        :param errors: a pointer to the errors of the FPL interpreter
        :param root: a pointer to the root (cross-theory) node of the symbol table of the FPL interpreter
        :param theory_name: the name of the current theory being interpreted
        """
        self.debug = False  # True <=> verbose mode
        self.context = AuxContext()  # the current context of the source analysis
        self.working_stack = []  # a stack for remembering the symbol tree node(s) being relevant in the current context
        self.parse_list = []  # a stack for bottom-up aggregation of parsed FPL source code productions
        self.errors = errors  # any errors of the FPL interpreter
        self.theory_node = AuxSymbolTable.add_or_get_theory(root, theory_name)  # root node of the current theory

    def get_debug_parsing_info(self, parsing_info: AuxInterpretation):
        if self.debug:
            return str(parsing_info)
        else:
            return None
