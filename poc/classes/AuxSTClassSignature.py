from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from poc import fplerror


class AuxSTClassSignature(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.signature_class, i)
        self.id = ''
        self.type = ''
        self.type_pattern = 0
        self.zfrom = i.corrected_position('PredicateIdentifier')
        self.zto = i.last_positions_by_rule['ClassSignature'].pos_to_str()

    def set_type(self, class_type):
        if class_type.is_functional_term():
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a functional term"))
        elif class_type.is_variadic():
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "an index"))
        elif class_type.is_predicate():
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a predicate"))
        elif class_type.is_generic():
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id, "a generic"))
        elif class_type.is_extension():
            self.get_error_mgr().add_error(
                fplerror.FplInvalidInheritance(class_type.get_ast_info(), class_type.id,
                                               "a user-defined syntax extension"))

        self.type_pattern = class_type.type_pattern
        self.type = class_type.id
