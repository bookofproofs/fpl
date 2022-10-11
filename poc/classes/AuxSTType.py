import re
from poc.classes.AuxInterfaceSTTypePattern import AuxInterfaceSTTypePattern
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTableHelpers import AuxSymbolTableHelpers
from poc.classes.AuxSTArgs import AuxSTArgs
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTType(AuxST, AuxInterfaceSTTypePattern):

    def __init__(self, i):
        super().__init__(AuxSTConstants.type, i)
        self.id = ""
        self.type_pattern = 0
        self.type_mod = ""
        self._parsing_info = None
        self._qualified_id = None

    def set_type(self, var_type):
        if var_type.generalType is not None:
            self.id = var_type.generalType.id
            self.type_mod = var_type.generalType.type_mod
            self.type_pattern = var_type.generalType.type_pattern
            self.zfrom = var_type.generalType.zfrom
            self.zto = var_type.generalType.zto
        self._parsing_info = var_type

    def make(self):
        if self._parsing_info.paramTuple is not None:
            type_node = AuxSTType(self._i)
            type_node = type_node.clone(with_params=True)
            type_node.parent = self
            for next_var_declaration in self._parsing_info.paramTuple.tuple:
                AuxSymbolTableHelpers.add_vars_to_node(self._i, type_node, next_var_declaration)

    def to_string(self):
        ret = self.id
        if len(self.children) > 0:
            for child in self.children:
                ret += child.to_string()
        return ret

    def to_string2(self):
        if self.type_mod is not None:
            ret = self.type_mod
        else:
            ret = ""
        return ret + self.to_string()

    def clone(self, with_params=False):
        other = self._copy(AuxSTType(self._i))
        other._qualified_id = self._qualified_id
        if with_params:
            # prevent cloning type when, in fact the type has params.
            # In this case replace the node by an AuxSTArgs node
            args = AuxSTArgs(self._i)
            # but make sure it has the same children as the cloned type
            args.children = other.children
            return args
        else:
            other.id = self.id
            other.type_mod = self.type_mod
            other.type_pattern = self.type_pattern
            other._parsing_info = self._parsing_info
            return other

    def get_qualified_id(self):
        if self._qualified_id is None:
            self._qualified_id = re.sub(AuxSTConstants.qualified_re, "", self.id)
        return self._qualified_id

    def get_relative_id(self):
        return self.id

    def evaluate(self, sem):
        # a separate evaluation of type nodes is not required since they are already fully represented by themselves
        # in the symbol table. We add this method anyway as an interface for the recursive evaluation of the nodes
        # in the symbol table
        pass

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.to_string()
        return self._long_id
