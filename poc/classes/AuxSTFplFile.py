import hashlib
from poc.fplerror import FplErrorManager
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.fplsyntaxanalyzer import FPLSyntaxAnalyzer


class AuxSTFplFile(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.file)
        self.file_name = ""
        self._fpl_source = ""
        self._md5_hash = hashlib.md5()
        self.checksum = ""
        self.namespace = ""
        self._analyser = None
        self._transformer = None

    def set_file_content(self, fpl_source):
        self._fpl_source = fpl_source.strip()
        self._md5_hash.update(self._fpl_source.encode('utf-8'))
        self.checksum = self._md5_hash.hexdigest()

    def get_file_content(self):
        return self._fpl_source

    def set_analyser(self, root, error_mgr: FplErrorManager, all_extensions: dict):
        self._analyser = FPLSyntaxAnalyzer(root, self.file_name, error_mgr, self.namespace)
        self._analyser.i.all_extension_definitions.update(all_extensions)

    def get_analyser(self):
        return self._analyser

    def get_source(self):
        return self._fpl_source
