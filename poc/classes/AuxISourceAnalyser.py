from poc.classes.AuxST import AuxSTOutline
from poc.fplerror import FplErrorManager
from poc.classes.AuxSTTheory import AuxSTTheory
from poc.classes.AuxSTLocalizations import AuxSTLocalizations

"""
Implements an interface between the classes named Context<Something> and the class FPLSyntaxAnalyzer
"""


class AuxISourceAnalyser:
    verbose = True  # True <=> verbose mode and no try-catch blocks for run time errors

    def __init__(self, error_mgr: FplErrorManager, root: AuxSTOutline, theory_name: str, namespace=""):
        """
        Creates a new interface between the classes named Context<Something> and the class FPLSyntaxAnalyzer
        :param error_mgr: a pointer to the errors of the FPL transformer
        :param root: a pointer to the root (cross-theory) node of the symbol table of the FPL transformer
        :param theory_name: the name of the current theory being interpreted
        :param namespace: the name of the theory's namespace
        """
        self.parse_list = []  # a stack for bottom-up aggregation of parsed FPL source code derivations
        self.errors = error_mgr  # any errors of the FPL transformer
        self.theory_node = AuxSTTheory(root, theory_name)
        self.theory_node.namespace = namespace
        self.locals_node = AuxSTLocalizations(self.theory_node)
        self.last_positions_by_rule = dict()
        self.highlight_tags = list()
        self.all_extension_definitions = dict()
        self.ast_info = None

    def set_pos(self, ast_info):
        self.last_positions_by_rule[ast_info.rule] = ast_info

    def corrected_position(self, rule: str):
        ast_info = self.last_positions_by_rule[rule]
        ast_info.pos = ast_info.pos - ast_info.length_cst
        ast_info.col = ast_info.col - ast_info.length_cst
        return ast_info.pos_to_str()

    def corrected_position_by(self, rule: str, offset: int):
        ast_info = self.last_positions_by_rule[rule]
        ast_info.pos = ast_info.pos - offset
        ast_info.col = ast_info.col - offset
        return ast_info.pos_to_str()

    @staticmethod
    def corrected_zpos_by(zpos: str, offset: int):
        s = zpos.split(".")
        return ".".join([s[0], str(int(s[1]) - offset)])
