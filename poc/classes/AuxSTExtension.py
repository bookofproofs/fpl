import re
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from fplerror import FplExtensionExists, FplExtensionMalformed, FplExtensionUnknown


class AuxSTExtensionHandler:
    def __init__(self):
        # name
        self.extension_name = ""
        # regex
        self.extension_regex = ""
        # identified user-defined FPL constructor for this extension
        self.constructor = None
        # the name of the FPL file containing the definition of the extension
        self.file_name_with_definition = ""
        # nodes in the symbol table matching this extension
        self.matching_nodes = list()


class AuxSTExtension(AuxST):
    def __init__(self, i):
        super().__init__(AuxSTConstants.extension, i)
        self._i = i
        self.zfrom = i.last_positions_by_rule['ExtensionHeader'].pos_to_str()
        self._extension_handler = AuxSTExtensionHandler()
        self._extension_handler.file_name_with_definition = i.theory_node.file_name

    def get_handler(self):
        return self._extension_handler

    def set_extension_content(self, extension_name: str, extension_regex: str):
        self._extension_handler.extension_name = extension_name
        if extension_name in self._i.all_extension_definitions:
            # FPLError: extension already exists
            self._i.errors.add_error(
                FplExtensionExists(self, self._i.theory_node.file_name,
                                   self._i.all_extension_definitions[extension_name].file_name_with_definition))
        else:
            self._i.all_extension_definitions[extension_name] = self._extension_handler
            try:
                re.compile(extension_regex)
                self._extension_handler.extension_regex = extension_regex
            except re.error:
                self._i.errors.add_error(
                    FplExtensionMalformed(self, self._i.theory_node.file_name))
        if extension_name not in AuxSTConstants.known_extensions:
            self._i.errors.add_error(FplExtensionUnknown(self, extension_name, self._i.theory_node.file_name,
                                                         AuxSTConstants.known_extensions))
