import fplsemantics
import fplerror
import tatsu
from anytree import AnyNode, RenderTree
from classes.AuxOutlines import AuxOutlines
from classes.SymbolTable import SymbolTable


class FplInterpreter(object):
    _version = "1.1.0"
    _errors = None
    _semantics = None
    _parser = None
    _symbol_table_root = None

    def __init__(self, parser):
        self._parser = parser
        self._errors = []
        self._symbol_table_root = AnyNode(outline=AuxOutlines.root)

    def syntax_analysis(self, theory_name, fpl_source):
        try:
            self._semantics = fplsemantics.FPLSemantics(self._symbol_table_root, theory_name, self._errors)
            self._parser.parse(fpl_source, semantics=self._semantics, whitespace='')
            # self.print_semantics()
        except tatsu.exceptions.FailedParse as ex:
            self._semantics.errors.append(fplerror.FplParserError(ex, "in " + theory_name + ":" + str(ex)))

    def print_symbol_table(self):
        print(RenderTree(self._symbol_table_root))

    def symbol_table_to_str(self):
        return str(RenderTree(self._symbol_table_root))

    def symbol_table_clear(self):
        self._symbol_table_root.children = []

    def get_symbol_table_root(self):
        return self._symbol_table_root

    def get_version(self):
        return self._version

    def has_errors(self):
        return len(self._errors) > 0

    def print_errors(self):
        if len(self._errors) > 0:
            print(str(len(self._errors)), "errors found:")
            for err in self._errors:
                print(err)
        else:
            print("Congratulations! No errors found")

    def get_errors(self):
        return self._errors

    def minified(self):
        return self._semantics.get_minified()

    def prettyfied(self):
        return self._semantics.get_prettified()

    def print_semantics(self):
        for item in self._semantics.parse_list:
            print(item)
        print(str(len(self._semantics.parse_list)) + " items")

    def get_semantics(self):
        return self._semantics.parse_list

    def get_ast_list(self):
        return self._semantics.ast_list
