from anytree import AnyNode
from poc.classes.AuxSTTheory import AuxSTTheory
from poc.classes.AuxSTLocalizations import AuxSTLocalizations

"""
Implements an interface between the classes named Context<Something> and the class FPLSyntaxAnalyzer
"""


class AuxISourceAnalyser:
    verbose = True  # True <=> verbose mode

    def __init__(self, errors: list, root: AnyNode, theory_name: str):
        """
        Creates a new interface between the classes named Context<Something> and the class FPLSyntaxAnalyzer
        :param errors: a pointer to the errors of the FPL transformer
        :param root: a pointer to the root (cross-theory) node of the symbol table of the FPL transformer
        :param theory_name: the name of the current theory being interpreted
        """
        self.parse_list = []  # a stack for bottom-up aggregation of parsed FPL source code derivations
        self.errors = errors  # any errors of the FPL transformer
        self.theory_node = AuxSTTheory(root, theory_name)
        self.locals_node = AuxSTLocalizations(self.theory_node)
        self.last_positions_by_rule = dict()

    def set_pos(self, ast_info):
        self.last_positions_by_rule[ast_info.rule] = ast_info

    def corrected_position(self, rule: str):
        ast_info = self.last_positions_by_rule[rule]
        ast_info.pos = ast_info.pos - ast_info.length_cst + 1
        ast_info.col = ast_info.col - ast_info.length_cst + 1
        return ast_info.pos_to_str()

    def corrected_position_by(self, rule: str, offset: int):
        ast_info = self.last_positions_by_rule[rule]
        ast_info.pos = ast_info.pos - offset
        ast_info.col = ast_info.col - offset
        return ast_info.pos_to_str()

    def corrected_zpos_by(self, zpos: str, offset: int):
        s = zpos.split(":")
        return ":".join([s[0], str(int(s[1]) - offset), str(int(s[2]) - offset)])
