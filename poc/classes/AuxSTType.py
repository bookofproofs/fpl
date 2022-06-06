import re
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTArgs import AuxSTArgs
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInbuiltTypes import InbuiltObject, InbuiltGeneric, InbuiltIndex, InbuiltPredicate, InbuiltUndefined, \
    InbuiltFunctionalTerm, InbuiltExtension
from poc.fplerror import FplTypeNotAllowed
from poc.fplerror import FplIdentifierNotDeclared
from poc.classes.AuxBits import AuxBits


class AuxSTType(AuxST):

    def __init__(self, i):
        super().__init__("type", i)
        self.id = ""
        self.type_pattern = -1
        self.type_mod = ""
        self._parsing_info = None
        self._type_node = None
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
            type_node = type_node.clone()
            type_node.parent = self
            for next_var_declaration in self._parsing_info.paramTuple.tuple:
                AuxSymbolTable.add_vars_to_node(self._i, type_node, next_var_declaration)

    def to_string(self):
        ret = self.id
        if len(self.children) > 0:
            for child in self.children:
                ret += child.to_string()
        return ret

    def clone(self):
        other = self._copy(AuxSTType(self._i))
        other._type_node = self._type_node
        other._qualified_id = self._qualified_id
        if self.type_pattern == -1:
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

    def set_type_node(self, sem_identifiers, file_name):
        qualified_identifier = self.get_qualified_id()
        if self.id[0].isupper():  # if the identifier starts with a Capital, we have a user-defined type
            if qualified_identifier in sem_identifiers.classes.dictionary():
                self._type_node = sem_identifiers.classes.get(qualified_identifier)[0]
            elif qualified_identifier in sem_identifiers.predicates.dictionary():
                self._type_node = sem_identifiers.predicates.get(qualified_identifier)[0]
            elif qualified_identifier in sem_identifiers.functional_terms.dictionary():
                self._type_node = sem_identifiers.functional_terms.get(qualified_identifier)[0]
            elif qualified_identifier in sem_identifiers.overridden_qualified_ids.dictionary():
                # any other found declared block is semantically not an allowed type,
                # we trigger the
                sem_identifiers.analyzer.error_mgr.add_error(
                    FplTypeNotAllowed(sem_identifiers.overridden_qualified_ids.get(qualified_identifier)[0], self.zfrom,
                                      file_name)
                )
                # and set the type to undefined
                self._type_node = InbuiltUndefined()
            else:
                # otherwise we trigger the FplIdentifierNotDeclared error
                sem_identifiers.analyzer.error_mgr.add_error(
                    FplIdentifierNotDeclared(qualified_identifier, file_name, self.zfrom))
                # and set the type to undefined
                self._type_node = InbuiltUndefined()
        elif AuxBits.is_index(self.type_pattern):
            self._type_node = InbuiltIndex()
        elif AuxBits.is_predicate(self.type_pattern):
            self._type_node = InbuiltPredicate()
        elif AuxBits.is_functional_term(self.type_pattern):
            self._type_node = InbuiltFunctionalTerm()
        elif AuxBits.is_generic(self.type_pattern):
            self._type_node = InbuiltGeneric(self.id)
        elif AuxBits.is_inbuilt_object(self.type_pattern):
            self._type_node = InbuiltObject()
        elif AuxBits.is_extension(self.type_pattern):
            self._type_node = InbuiltExtension(self.id)
        else:
            raise NotImplementedError("type_pattern " + str(self.type_pattern))

    def get_type_node(self):
        return self._type_node

    def get_qualified_id(self):
        if self._qualified_id is None:
            self._qualified_id = re.sub(AuxSTConstants.qualified_re, "", self.id)
        return self._qualified_id

    def get_type_signature(self):
        return self._type_node.id
