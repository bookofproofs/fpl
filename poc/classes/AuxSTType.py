import re
from poc.classes.AuxInterfaceSTTypePattern import AuxInterfaceSTTypePattern
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTableHelpers import AuxSymbolTableHelpers
from poc.classes.AuxSTArgs import AuxSTArgs
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTType(AuxST, AuxInterfaceSTTypePattern):

    def __init__(self, i):
        AuxST.__init__(self, AuxSTConstants.type, i)
        AuxInterfaceSTTypePattern.__init__(self)
        self.id = ""
        self.type_pattern = 0
        self.type_mod = ""
        self._parsing_info = None
        self._qualified_id = None
        self._base_classes = set()

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

    def evaluate(self, sem):
        # a separate evaluation of type nodes is not required since they are already fully represented by themselves
        # in the symbol table. We add this method anyway as an interface for the recursive evaluation of the nodes
        # in the symbol table
        pass

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.to_string()
        return self._long_id

    def accepts(self, other_type):
        """
        True, if the other_type is consistent with self.
        The method is asymmetric, for instance, base class types accept the types of their
        derived classes but not vice versa.
        :return: Boolean value
        """
        ret = self._accepts_any_undefined(other_type)
        if ret is not None:
            return ret

        ret = self._accepts_any_predicates(other_type)
        if ret is not None:
            return ret

        ret = self._accepts_any_functional_terms(other_type)
        if ret is not None:
            return ret

        ret = self._accepts_any_template(other_type)
        if ret is not None:
            return ret

        ret = self._accepts_any_class(other_type)
        if ret is not None:
            return ret

        ret = self._accepts_any_object(other_type)
        if ret is not None:
            return ret

        ret = self._accepts_any_index(other_type)
        if ret is not None:
            return ret

        # if the match method does not yet recognize a use case, raise a NotImplementedError
        raise NotImplementedError()

    def _accepts_any_undefined(self, other_type):
        if self.is_inbuilt() and self.id == AuxSTConstants.undefined:
            # the inbuilt type does not match anything
            return False
        if other_type.is_inbuilt() and other_type.id == AuxSTConstants.undefined:
            # the inbuilt type does not match anything
            return False
        return None

    def _accepts_any_predicates(self, other_type):
        if self.is_predicate() and other_type.is_predicate():
            # two predicates always match
            return True
        if self.is_predicate() and not other_type.is_predicate():
            return False
        if other_type.is_predicate() and not self.is_predicate():
            return False
        return None

    def _accepts_any_functional_terms(self, other_type):
        if self.is_functional_term() and other_type.is_functional_term():
            if self.is_inbuilt():
                # the inbuilt type accepts any other functional term
                return True
            else:
                # otherwise, it accepts only, if the functional terms have the same id
                return self.id == other_type.id
        if self.is_functional_term() and not other_type.is_functional_term():
            # a functional term might match some non functional-terms
            raise NotImplementedError()
        if other_type.is_functional_term() and not self.is_functional_term():
            # a functional term might match some non functional-terms
            raise NotImplementedError()
        return None

    def _accepts_any_object(self, other_type):
        if self.is_object() and other_type.is_object():
            if self.is_inbuilt():
                # the inbuilt object accepts any other object
                return True
            else:
                # we have a user-defined class (self)
                if self.id == other_type.id:
                    # if this is the same class, return True
                    return True
                else:
                    # if the other_type is derived from self either via inheritance
                    # or via the assertion of the is operand
                    return other_type.is_derived_from(self)
        if self.is_object() and not other_type.is_object():
            # an object might match some non objects, except
            if other_type.is_index():
                return False
            else:
                raise NotImplementedError()
        if other_type.is_object() and not self.is_object():
            # an object might match some non objects
            raise NotImplementedError()
        return None

    def _accepts_any_template(self, other_type):
        if self.is_generic() and other_type.is_generic():
            if self.get_scope().id == other_type.get_scope().id:
                # two generic types are the same if they have the same scope and id
                return self.id == other_type.id
            else:
                # return true even if the names of the generic types are not the same if the
                # scope they are declared in are not the same
                return True
        elif self.is_generic() and not other_type.is_generic():
            # a generic type accepts anything else
            return True
        elif not self.is_generic() and other_type.is_generic():
            # a generic type accepts anything else
            return True
        return None

    def _accepts_any_class(self, other_type):
        if self.is_class() and other_type.is_class():
            # self accepts the other type if the latter is derived from self
            return other_type.is_derived_from(self)
        elif self.is_class() and not other_type.is_class():
            # case of deriving classes from other types
            return True
        elif not self.is_object() and other_type.is_class():
            raise NotImplementedError()
        return None

    def _accepts_any_index(self, other_type):
        if self.is_index() and other_type.is_index():
            # two index types always match
            return True
        # in all other cases return False
        return False

    def is_derived_from(self, other_type):
        if other_type == self:
            return True
        else:
            other_type.is_class() and other_type.id in self._base_classes

    def register_base_class(self, class_id: str):
        if class_id not in self._base_classes:
            self._base_classes.add(class_id)
