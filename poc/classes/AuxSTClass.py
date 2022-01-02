from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search


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

    def get_declared_vars(self):
        """
        Calculates a tuple of variables declared in the scope of the node.
        :return: tuple of declared variables.
        """
        # Class variables only (i.e. do not consider the sub-scopes of constructors and properties)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.var_spec)
        return search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl, AuxSymbolTable.outline)
