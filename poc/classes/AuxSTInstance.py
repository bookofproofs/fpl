from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.fplerror import FplErrorManager


class AuxSTInstance(AuxSTBuildingBlock):
    def __init__(self, i):
        super().__init__(AuxSTConstants.property, i)
        self.mandatory = False
        self._i = i
        self._is_inherited = False

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        if self.parent.parent.def_type == AuxSTConstants.classDeclaration:
            # Case #1: We have a property of a class
            # collect class variable declarations (outer scope)
            classes_var_spec_list = AuxSymbolTable.get_child_by_outline(self.parent.parent, AuxSTConstants.var_spec)
            class_var_declarations = search.findall_by_attr(classes_var_spec_list, AuxSTConstants.var_decl,
                                                            AuxSTConstants.outline)
            for class_var_declaration in class_var_declarations:
                if class_var_declaration.id not in self._declared_vars:
                    # set the scope of the class variable to the end of the class
                    class_var_declaration.initialize_scope(self.parent.parent.zto)
                    # add the class variable declaration into a dictionary of the constructor for fast searching
                    self._declared_vars[class_var_declaration.id] = class_var_declaration
                else:
                    # we have a potential duplicate variable declaration
                    self.append_variable_already_declared(class_var_declaration, error_mgr, filename)
        else:
            # Case#2: We have a property of a functional term definition or a predicate definition
            # collect parent's variable declarations (outer scope)
            parent_var_spec_list = AuxSymbolTable.get_child_by_outline(self.parent.parent, AuxSTConstants.var_spec)
            parent_var_declarations = search.findall_by_attr(parent_var_spec_list, AuxSTConstants.var_decl,
                                                             AuxSTConstants.outline)

            signature_node = AuxSymbolTable.get_child_by_outline(self.parent.parent,
                                                                 AuxSTConstants.signature)
            parent_var_declarations += search.findall_by_attr(signature_node, AuxSTConstants.var_decl,
                                                              AuxSTConstants.outline)

            for parent_var_declaration in parent_var_declarations:
                if parent_var_declaration.id not in self._declared_vars:
                    # set the scope of the class variable to the end of the class
                    parent_var_declaration.initialize_scope(self.parent.parent.zto)
                    # add the class variable declaration into a dictionary of the constructor for fast searching
                    self._declared_vars[parent_var_declaration.id] = parent_var_declaration
                else:
                    # we have a potential duplicate variable declaration
                    self.append_variable_already_declared(parent_var_declaration, error_mgr, filename)

        # include own variable declarations (i.e. both, its signature and body)
        own_var_declarations = search.findall_by_attr(self, AuxSTConstants.var_decl, AuxSTConstants.outline)
        for var_declaration in own_var_declarations:
            if var_declaration.id not in self._declared_vars:
                # set the scope of the class variable to the end of the class
                var_declaration.initialize_scope(self.zto)
                # add the class variable declaration into a dictionary of the constructor for fast searching
                self._declared_vars[var_declaration.id] = var_declaration
            else:
                # we have a potential duplicate variable declaration
                self.append_variable_already_declared(var_declaration, error_mgr, filename)

        # the used variables are only in the body
        self._used_vars = search.findall_by_attr(self, AuxSTConstants.var, AuxSTConstants.outline)
        self.filter_misused_templates(error_mgr, filename)

    def isa(self):
        # getter for the source analyser
        return self._i

    def is_inherited(self):
        return self._is_inherited
