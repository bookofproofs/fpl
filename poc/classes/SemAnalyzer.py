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
        used_vars = referenced_node.get_used_vars()
        self.__check_undeclared_var_usages(declared_vars, used_vars)

    def __check_undeclared_var_usages(self, declared_vars, used_vars):
        for var_node in used_vars:
            if var_node.id not in declared_vars:
                # the variable is undeclared if it was not found among the declared variables
                self.errors.append(
                    fplerror.FplUndeclaredVariable(var_node.zfrom, var_node.id, self._current_filename)
                )
            elif not declared_vars[var_node.id].has_in_scope(var_node.zfrom):
                # the variable is also undeclared if it was found among the declared variables
                # but is outside the scope of this variable declaration
                self.errors.append(
                    fplerror.FplUndeclaredVariable(var_node.zfrom, var_node.id, self._current_filename)
                )
