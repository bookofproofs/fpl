from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTSignature(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.signature, parsing_info)
        self._list_named_declarations = None
        self._id = None

    def set_id(self, identifier):
        self._id = identifier

    def set_params(self, list_named_declarations):
        self._list_named_declarations = list_named_declarations

    def make(self):
        for named_var_declaration in self._list_named_declarations:
            AuxSymbolTable.add_vars_to_node(self, named_var_declaration)

    def to_string(self):
        ret = self._id + "["
        first_found = False
        if self._list_named_declarations is not None:
            for named_var_declaration in self._list_named_declarations:
                if not first_found:
                    ret += named_var_declaration.to_string()
                    first_found = True
                else:
                    ret += "," + named_var_declaration.to_string()
        ret += "]"
        return ret
