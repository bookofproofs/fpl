import re
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTWithId(AuxST):
    """
    A class for outline elements of the symbol table that have an ast_info and errors
    """

    def __init__(self, outline: str, i):
        super().__init__(outline=outline, i=i)
        self.id = ""

    def get_qualified_id(self):
        if self._qualified_id is None:
            self._qualified_id = re.sub(AuxSTConstants.qualified_re, "", self.id)
        return self._qualified_id
