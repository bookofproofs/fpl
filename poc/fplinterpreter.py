import poc.fplsourceanalyser
import poc.fplsourcetransformer
import poc.fplmessage
import tatsu
from anytree import AnyNode, RenderTree
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser


class FplInterpreter(object):

    def __init__(self, parser):
        self._parser = parser
        self._errors = []
        self._symbol_table_root = AnyNode(outline=AuxSymbolTable.root)
        AnyNode(outline=AuxSymbolTable.globalLookup, parent=self._symbol_table_root)
        self._is_verbose = AuxISourceAnalyser.verbose
        self._analyser = None
        self.version = "1.2.3"

    def syntax_analysis(self, theory_name: str, fpl_source: str):
        self._analyser = poc.fplsourceanalyser.FPLSourceAnalyser(self._symbol_table_root, theory_name,
                                                                 self._errors)
        if self._analyser.i.verbose:
            self._parser.parse(fpl_source, semantics=self._analyser, whitespace='')
        else:
            try:
                self._parser.parse(fpl_source, semantics=self._analyser, whitespace='')
            except tatsu.exceptions.FailedParse as ex:
                self._analyser.i.errors.append(
                    poc.fplmessage.FplParserError(ex, "in " + theory_name + ":" + str(ex)))
            except tatsu.exceptions.FailedToken as ex:
                self._analyser.i.errors.append(
                    poc.fplmessage.FplParserError(ex, "in " + theory_name + ":" + str(ex)))
            except tatsu.exceptions.FailedPattern as ex:
                self._analyser.i.errors.append(
                    poc.fplmessage.FplParserError(ex, "in " + theory_name + ":" + str(ex)))

    def syntax_transform(self, theory_name: str, fpl_source: str):
        self._analyser = poc.fplsourcetransformer.FPLSourceTransformer(theory_name, self._errors)
        if self._analyser.i.verbose:
            self._parser.parse(fpl_source, semantics=self._analyser, whitespace='')
        else:
            try:
                self._parser.parse(fpl_source, semantics=self._analyser, whitespace='')
            except tatsu.exceptions.FailedParse as ex:
                self._analyser.i.errors.append(
                    poc.fplmessage.FplParserError(ex, "in " + theory_name + ":" + str(ex)))
            except tatsu.exceptions.FailedToken as ex:
                self._analyser.i.errors.append(
                    poc.fplmessage.FplParserError(ex, "in " + theory_name + ":" + str(ex)))
            except tatsu.exceptions.FailedPattern as ex:
                self._analyser.i.errors.append(
                    poc.fplmessage.FplParserError(ex, "in " + theory_name + ":" + str(ex)))

    def print_symbol_table(self):
        print(RenderTree(self._symbol_table_root))

    def symbol_table_to_str(self):
        return str(RenderTree(self._symbol_table_root))

    def clear(self):
        self._symbol_table_root.children = tuple([])
        self._errors.clear()

    def get_symbol_table_root(self):
        return self._symbol_table_root

    def is_in_verbose_mode(self):
        return self._is_verbose

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
        return self._analyser.get_minified()

    def prettyfied(self):
        return self._analyser.get_prettified()

    def print_semantics(self):
        for item in self._analyser.parse_list:
            print(item)
        print(str(len(self._analyser.parse_list)) + " items")

    def get_semantics(self):
        return self._analyser.parse_list

    def get_ast_list(self):
        return self._analyser.ast_list
