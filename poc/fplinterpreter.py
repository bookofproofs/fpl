import fplsemantics
import fplerror
import tatsu


class FplInterpreter(object):
    _version = "1.0.2"
    _semantics = None
    _theory_name = None

    def __init__(self, theory_name, fpl_source, parser):
        self._theory_name = theory_name
        self._semantics = fplsemantics.FPLSemantics()
        try:
            self._theory_name = theory_name
            self._semantics = fplsemantics.FPLSemantics()
            parser.parse(fpl_source, semantics=self._semantics, whitespace='')
        except tatsu.exceptions.FailedParse as ex:
            self._semantics.errors.append(fplerror.FplParserError(ex, "in " + theory_name + ":" + str(ex)))
        # self.validate_statements()

    def get_version(self):
        return self._version

    def has_errors(self):
        return len(self._semantics.errors) > 0

    def get_name(self):
        return self._theory_name

    def print_errors(self):
        if len(self._semantics.errors) > 0:
            print(str(len(self._semantics.errors)), "errors found:")
            for err in self._semantics.errors:
                print(err)
        else:
            print("Congratulations! No errors found")

    def get_errors(self):
        return self._semantics.errors

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
