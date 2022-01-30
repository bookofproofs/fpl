from anytree import AnyNode, search
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc import fplerror
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTConstructor import AuxSTConstructor
from poc.classes.AuxSTPredicateInstance import AuxSTPredicateInstance
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate


class SemAnalyzer:

    def __init__(self, symbol_table: AnyNode, errors: list):
        self.symbol_table = symbol_table
        self.errors = errors
        self._current_filename = ""

    def check_semantics(self):
        globals = AuxSymbolTable.get_child_by_outline(self.symbol_table, AuxSymbolTable.globals)
        for node in globals.children:
            # for any subsequent error logging, remember the name of the FPL file in which the node was declared
            # (the second element in the node's reference's path is always the theory node with a "file_name" attribute)
            self._current_filename = node.reference.path[1].file_name
            self._check_variables(node)

    def _check_variables(self, node: AnyNode):
        referenced_node = node.reference
        declared_vars = referenced_node.get_declared_vars()
        self.__check_duplicate_var_declarations(declared_vars)
        used_vars = search.findall_by_attr(referenced_node, AuxSymbolTable.var, AuxSymbolTable.outline)
        self.__check_undeclared_var_usages(declared_vars, used_vars)

    def __check_duplicate_var_declarations(self, declared_vars):
        all_ids = dict()
        for var_node in declared_vars:
            if var_node.id not in all_ids:
                all_ids[var_node.id] = var_node
            else:
                self.errors.append(
                    fplerror.FplVariableAlreadyDeclared(var_node.zfrom, all_ids[var_node.id].zfrom, var_node.id,
                                                        self._current_filename))

    def __check_undeclared_var_usages(self, declared_vars, used_vars):
        all_declared_var_ids = set()
        for var_node in declared_vars:
            if var_node.id not in all_declared_var_ids:
                all_declared_var_ids.add(var_node.id)

        for var_node in used_vars:
            if var_node.id not in all_declared_var_ids:
                self.errors.append(
                    fplerror.FplUndeclaredVariable(var_node.zfrom, var_node.id, self._current_filename)
                )
