from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxPrettifier import AuxPrettifier
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from anytree import AnyNode


class FPLSourceTransformer(object):

    def __init__(self, theory_name: str, errors: list):
        self._prettifier = AuxPrettifier()
        root = AnyNode()
        self.i = AuxISourceAnalyser(errors, root, theory_name)

    def get_minified(self):
        return self._prettifier.get_minified()

    def get_prettified(self):
        return self._prettifier.get_prettified()

    def _default(self, ast):
        """
        If there’s no method matching the rule’s name, TatSu will invoke this method.
        :param ast: ast
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
        :param ast: ast
        :return: ast
        """

        ast_info = AuxAstInfo(context, self.i.theory_node.theory_name)
        # minify
        self._minify(ast_info)
        return ast













