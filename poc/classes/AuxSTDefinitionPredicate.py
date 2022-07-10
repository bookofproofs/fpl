from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate
from poc.classes.AuxSTBlock import AuxSTBlock
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxSTProperties import AuxSTProperties
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.fplerror import FplErrorManager


class AuxSTDefinitionPredicate(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_def, i)
        self.def_type = AuxSymbolTable.predicateDeclaration
        self.id = ""
        self.zfrom = i.corrected_position('PredicateHeader')
        self.zto = i.last_positions_by_rule['DefinitionPredicate'].pos_to_str()

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        # The declared variables of a functional term definition are in its signature and its
        # variable specification list only.
        signature_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.signature)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.var_spec)
        declared_vars_tuple = search.findall_by_attr(signature_node, AuxSymbolTable.var_decl,
                                                     AuxSymbolTable.outline)
        declared_vars_tuple += search.findall_by_attr(var_spec_list_node, AuxSymbolTable.var_decl,
                                                      AuxSymbolTable.outline)
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
        # The used variables of a predicate definition are, therefore, limited to its scope without the scopes of
        # of its sub nodes.
        self._used_vars = ()
        for child in self.children:
            if type(child) is not AuxSTProperties:
                self._used_vars += search.findall_by_attr(child, AuxSymbolTable.var, AuxSymbolTable.outline)
        self.filter_misused_templates(error_mgr, filename)

    def evaluate(self, sem):
        if self.constant_value() is None:
            signature = None
            for child in self.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(),
                                                      sem.eval_stack[-1].arg_type_list,
                                                      sem.eval_stack[-1].check_args)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined())
                elif isinstance(child, (AuxSTPredicate, AuxSTPredicateWithArgs, AuxSTVariable)):
                    ret = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate())
                    if ret.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                    else:
                        sem.eval_stack[-1].value = ret.returned_value
                    if len(signature.children) == 0:
                        self.set_constant_value(sem.eval_stack[-1])
                elif isinstance(child, AuxSTProperties):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined())
                else:
                    raise NotImplementedError(str(type(child)))
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
