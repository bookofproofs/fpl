import poc.fplsourceanalyser
import poc.fplsourcetransformer
import poc.fplerror
import tatsu
from anytree import AnyNode, RenderTree
from poc.classes.AuxOutlines import AuxOutlines


class FplInterpreter(object):

    def __init__(self, parser):
        self._parser = parser
        self._errors = []
        self._symbol_table_root = AnyNode(outline=AuxOutlines.root)
        self._source_analysis = None
        self.version = "1.1.2"

    def syntax_analysis(self, theory_name: str, fpl_source: str):
        try:
            self._source_analysis = poc.fplsourceanalyser.FPLSourceAnalyser(self._symbol_table_root, theory_name,
                                                                            self._errors)
            self._parser.parse(fpl_source, semantics=self._source_analysis, whitespace='')
        except tatsu.exceptions.FailedParse as ex:
            self._source_analysis.errors.append(poc.fplerror.FplParserError(ex, "in " + theory_name + ":" + str(ex)))

    def syntax_transform(self, theory_name: str, fpl_source: str):
        try:
            self._syntax_transform = poc.fplsourcetransformer.FPLSourceTransformer(theory_name, self._errors)
            self._parser.parse(fpl_source, semantics=self._syntax_transform, whitespace='')
        except tatsu.exceptions.FailedParse as ex:
            self._source_analysis.errors.append(poc.fplerror.FplParserError(ex, "in " + theory_name + ":" + str(ex)))

    def print_symbol_table(self):
        print(RenderTree(self._symbol_table_root))

    def symbol_table_to_str(self):
        return str(RenderTree(self._symbol_table_root))

    def clear(self):
        self._symbol_table_root.children = tuple([])
        self._errors.clear()

    def get_symbol_table_root(self):
        return self._symbol_table_root

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
        return self._syntax_transform.get_minified()

    def prettyfied(self):
        return self._syntax_transform.get_prettified()

    def print_semantics(self):
        for item in self._source_analysis.parse_list:
            print(item)
        print(str(len(self._source_analysis.parse_list)) + " items")

    def get_semantics(self):
        return self._source_analysis.parse_list

    def get_ast_list(self):
        return self._source_analysis.ast_list
