from poc.classes.AuxEvaluationBlockFunctionalTerm import AuxEvaluationBlockFunctionalTerm
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTProperties import AuxSTProperties
from anytree import search
from poc.fplerror import FplErrorManager


class AuxSTDefinitionFunctionalTerm(AuxSTBuildingBlock):

    def __init__(self, i):
        AuxSTBuildingBlock.__init__(self, AuxSTConstants.block_def, i)
        self.def_type = AuxSTConstants.functionalTerm
        self.zfrom = i.corrected_position('FunctionalTermHeader')
        self.zto = i.last_positions_by_rule['DefinitionFunctionalTerm'].pos_to_str()

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        # The declared variables of a functional term definition are in its signature, its image, and its
        # variable specification list only.
        signature_node = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.signature)
        image_node = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.type)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.var_spec)
        declared_vars_tuple = search.findall_by_attr(signature_node, AuxSTConstants.var_decl,
                                                     AuxSTConstants.outline)
        declared_vars_tuple += search.findall_by_attr(image_node, AuxSTConstants.var_decl,
                                                      AuxSTConstants.outline)
        declared_vars_tuple += search.findall_by_attr(var_spec_list_node, AuxSTConstants.var_decl,
                                                      AuxSTConstants.outline)
        for var_declaration in declared_vars_tuple:
            if var_declaration.id not in self._declared_vars:
                # set the scope of the variable
                var_declaration.initialize_scope(self.zto)
                # add the variable declaration into a dictionary for fast searching
                self._declared_vars[var_declaration.id] = var_declaration
            else:
                # we have a potential duplicate variable declaration
                self.append_variable_already_declared(var_declaration, error_mgr, filename)

        # The used variables might be spread across the scope of the predicate definition, including its properties.
        # However, we omit those scopes because they have their own _used_vars tuples. Thus, we have to limit
        # The used variables of a predicate definition are, therefore, limited to its scope without the scopes
        # of its sub nodes.
        self._used_vars = ()
        for child in self.children:
            if type(child) is not AuxSTProperties:
                self._used_vars += search.findall_by_attr(child, AuxSTConstants.var, AuxSTConstants.outline)
        self.filter_misused_templates(error_mgr, filename)

    def evaluate(self, sem):
        AuxEvaluationBlockFunctionalTerm.evaluate(self, sem)

    def get_declared_type(self):
        if self._declared_type is None:
            AuxEvaluationBlockFunctionalTerm.initialize_declared_type_of_functional_term(self)
        return self._declared_type
