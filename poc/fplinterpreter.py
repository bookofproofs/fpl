import fplsemantics
import fplerror
import tatsu
import sys


class FplInterpreter(object):
    _semantics = None
    _theory_name = None
    _verbose = None

    def __init__(self, theory_name, fpl_source, parser, verbose=False):
        self._theory_name = theory_name
        self._semantics = fplsemantics.FPLSemantics()
        self._verbose = verbose
        parser.parse(fpl_source, semantics=self._semantics, whitespace='')
        try:
            self._theory_name = theory_name
            self._semantics = fplsemantics.FPLSemantics()
            self._verbose = verbose
            parser.parse(fpl_source, semantics=self._semantics, whitespace='')
        except tatsu.exceptions.FailedParse as ex:
            self._semantics.errors.append(fplerror.FPLCompilerError(0, ex, 0, "in " + theory_name + ":" + str(ex)))
        except tatsu.exceptions.FailedParse as ex:
            self._semantics.errors.append(fplerror.FPLCompilerError(-1, ex, 0, "in " + theory_name + ":" + str(ex)))
        except:
            self._semantics.errors.append(fplerror.FPLCompilerError(-2, sys.exc_info()[1], 0, sys.exc_info()[1]))
        # self.validate_statements()

    def has_errors(self):
        return len(self._semantics.errors) > 0

    def print_errors(self):
        if len(self._semantics.errors) > 0:
            print(str(len(self._semantics.errors)), "errors found:")
            for err in self._semantics.errors:
                print(err)
            if self._verbose:
                max_len = len(self._semantics.parse_list)
                min_len = 10
                if max_len < min_len:
                    min_len = min_len
                print(*(self._semantics.parse_list[max_len - min_len:]), sep="\n")

        else:
            print("Congratulations! No errors found")

    def minified(self):
        return self._semantics.get_minified()

    def print_semantics(self):
        for item in self._semantics.parse_list:
            print(item)
