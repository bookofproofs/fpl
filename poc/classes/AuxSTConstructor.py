from poc.classes.AuxInbuiltTypes import InbuiltClassInstance, InbuiltUndefined
from poc.classes.AuxSTBlock import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.fplerror import FplErrorManager


class AuxSTConstructor(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.classConstructor, i)
        self.id = ""

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        # Note: Default constructors are omitted since they do not declare any variables
        # but still are called in the loop (otherwise we would cause double-listing of the same errors).
        if self.outline != AuxSymbolTable.classDefaultConstructor:
            # include the variables declared in the class (outer scope)
            classes_var_spec_list = AuxSymbolTable.get_child_by_outline(self.parent.parent, AuxSymbolTable.var_spec)
            class_var_declarations = search.findall_by_attr(classes_var_spec_list, AuxSymbolTable.var_decl,
                                                            AuxSymbolTable.outline)
            for class_var_declaration in class_var_declarations:
                if class_var_declaration.id not in self._declared_vars:
                    # set the scope of the class variable to the end of the class
                    class_var_declaration.initialize_scope(self.parent.parent.zto)
                    # add the class variable declaration into a dictionary of the constructor for fast searching
                    self._declared_vars[class_var_declaration.id] = class_var_declaration
                else:
                    # we have a potential duplicate variable declaration
                    self.append_variable_already_declared(class_var_declaration, error_mgr, filename)

            # include constructor's own variables (i.e. both, its signature and body)
            own_var_declarations = search.findall_by_attr(self, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
            for var_declaration in own_var_declarations:
                if var_declaration.id not in self._declared_vars:
                    # set the scope of the class variable to the end of the class
                    var_declaration.initialize_scope(self.parent.parent.zto)
                    # add the class variable declaration into a dictionary of the constructor for fast searching
                    self._declared_vars[var_declaration.id] = var_declaration
                else:
                    # we have a potential duplicate variable declaration
                    self.append_variable_already_declared(var_declaration, error_mgr, filename)

            # the used variables are only in the body
            self._used_vars += search.findall_by_attr(self, AuxSymbolTable.var, AuxSymbolTable.outline)
            self.filter_misused_templates(error_mgr, filename)

    def evaluate(self, sem):
        if self.outline == AuxSymbolTable.classDefaultConstructor:
            sem.eval_stack[-1].value = InbuiltClassInstance(self)
        else:
            sem.eval_stack[-1].value = InbuiltUndefined()
