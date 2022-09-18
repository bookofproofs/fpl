from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from poc import fplerror
from poc.classes.AuxBits import AuxBits


class AuxSTClassSignature(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.signature_class, i)
        self.id = ''
        self.type = ''
        self.type_pattern = 0
        self.zfrom = i.corrected_position('PredicateIdentifier')
        self.zto = i.last_positions_by_rule['ClassSignature'].pos_to_str()

    def set_type(self, class_type):
        if AuxBits.is_functional_term(class_type.type_pattern):
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a functional term"))
        elif AuxBits.is_index(class_type.type_pattern):
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "an index"))
        elif AuxBits.is_predicate(class_type.type_pattern):
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a predicate"))
        elif AuxBits.is_generic(class_type.type_pattern):
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a generic"))
        elif AuxBits.is_extension(class_type.type_pattern):
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a user-defined syntax extension"))

        self.type_pattern = class_type.type_pattern
        self.type = class_type.id
