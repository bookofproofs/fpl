from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxSTProperties import AuxSTProperties
from poc.classes.AuxSTConstants import AuxSTConstants
from anytree import search
from poc.fplerror import FplErrorManager


class AuxSTAnonymousBlock(AuxSTBuildingBlock):

    def __init__(self, i, node):
        super().__init__(AuxSTConstants.block_def, i)
        self.def_type = AuxSTConstants.predicateDeclaration
        self.id = "anonymous_" + node.id
        self.zfrom = node.get_declared_type().zfrom
        self.zto = node.get_declared_type().zto
        self._anonymous_of_node = node
        self._declared_type = node.get_declared_type()
        signature_node = AuxSTSignature(i)
        signature_node.parent = self
        if len(node.get_declared_type().children) > 0:
            for child in node.get_declared_type().children[0].children:
                child_clone = child.clone()
                child_clone.parent = signature_node
        self.initialize_vars(node.ancestors[1].file_name, i.errors)

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        # The declared variables of a functional term definition are in its signature and its
        # variable specification list only.
        declared_vars_tuple = search.findall_by_attr(self._anonymous_of_node, AuxSTConstants.var_decl,
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
        new_value = InbuiltValuePredicate(self._anonymous_of_node)
        sem.eval_stack[-1].value = new_value
