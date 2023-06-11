from poc.classes.AuxPrettifier import AuxPrettifier
from poc.util.fplutil import Utils
from poc.classes.AuxAstInfo import AuxAstInfo
import os


class FPLSourceTransformer:

    def __init__(self, fpl_parser):
        self._prettifier = AuxPrettifier()
        self._parser = fpl_parser
        self._theory_name = ""

    def syntax_transform(self, path_to_theory: str):
        fpl_source = Utils.get_file_content(path_to_theory)
        self._theory_name = os.path.basename(path_to_theory)
        self.syntax_transform_from_source(fpl_source)

    def syntax_transform_from_source(self, fpl_source: str):
        self._parser.parse(fpl_source, semantics=self, whitespace='')

    def get_minified(self):
        return self._prettifier.get_minified()

    def get_prettified(self):
        return self._prettifier.get_prettified()

    def clear(self):
        del self._prettifier
        self._prettifier = AuxPrettifier()

    def _default(self, ast):  # noqa
        """
        If there’s no method matching the rule’s name, TatSu will invoke this method.
        :param ast: Abstract symbol tree of the parser
        :return: ast
        """
        return ast

    def _minify(self, ast_info: AuxAstInfo):
        """
        Builds up a minified representation of the parsed fpl file during the parsing process
        :param ast_info: info about the parsed item
        :return: None
        """
        self._prettifier.minify(ast_info)

    def _postproc(self, context, ast):
        """
        This TatSu method will be called after each rule is processed.
        In contrast to _default, this method receives the current parsing context as a parameter that contains
        valuable parsing information like the position and the cst.
        :param context: parsing context
        :param ast: Abstract symbol tree of the parser
        :return: ast
        """

        ast_info = AuxAstInfo(context, self._theory_name)
        # minify
        self._minify(ast_info)
        return ast


