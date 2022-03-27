import hashlib
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplsyntaxanalyzer import FPLSyntaxAnalyzer


class AuxSTFplFile(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSymbolTable.file)
        self.file_name = ""
        self._fpl_source = ""
        self._md5_hash = hashlib.md5()
        self.checksum = ""
        self.namespace = ""
        self.is_main = False
        self._analyser = None
        self._transformer = None

    def set_file_content(self, fpl_source):
        self._fpl_source = fpl_source
        self._md5_hash.update(fpl_source.encode('utf-8'))
        self.checksum = self._md5_hash.hexdigest()

    def get_file_content(self):
        return self._fpl_source

    def set_analyser(self, root, errors: list):
        self._analyser = FPLSyntaxAnalyzer(root, self.file_name, errors)

    def get_analyser(self):
        return self._analyser
