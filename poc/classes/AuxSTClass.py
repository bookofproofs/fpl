from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc import fplerror


class AuxSTClass(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_def, i)
        self.class_types = []
        self.def_type = AuxSymbolTable.classDeclaration
        self.id = ""
        self._content = None
        self.zfrom = i.corrected_position('ClassHeader')
        self.zto = i.last_positions_by_rule['DefinitionClass'].pos_to_str()
        self.keyword = ""

    def add_type(self, class_type: str):
        if class_type in AuxRuleDependencies.dep["ObjectHeader"]:
            if "obj" not in self.class_types:
                self.class_types.append("obj")
        else:
            self.class_types.append(class_type)

    def initialize_vars(self, filename, errors):
        # The declared variables of a class are in its variable specification list only.
        # (i.e. do not consider the sub-scopes of constructors and properties)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.var_spec)

        declared_vars_tuple = search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl,
                                                      AuxSymbolTable.outline)
        for var_declaration in declared_vars_tuple:
            if var_declaration.id not in self._declared_vars:
                # set the scope of the variable
                var_declaration.initialize_scope(self.zto)
                # add the variable declaration into a dictionary for fast searching
                self._declared_vars[var_declaration.id] = var_declaration
            else:
                # we have a duplicate variable declaration
                errors.append(
                    fplerror.FplVariableAlreadyDeclared(var_declaration.zfrom,
                                                        self._declared_vars[var_declaration.id].zfrom,
                                                        var_declaration.id,
                                                        filename))

        # The used variables might be spread across the scope of the class, including its constructors and properties.
        # However, we omit those scopes because they have their own _used_vars tuples. Thus, we have to limit
        # The used variables of a class are, therefore, limited to the scope of the class without the scopes of
        # of its sub nodes.
        self._used_vars = search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var, AuxSymbolTable.outline)
