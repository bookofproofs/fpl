from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTSignature import AuxSTSignature
from fplerror import FplAxiomNotSatisfiable


class AuxSTAxiom(AuxSTBlockWithSignature):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_axiom, i)
        self.zfrom = i.corrected_position('AxiomHeader')
        self.zto = i.last_positions_by_rule['Axiom'].pos_to_str()
        self.keyword = ""

    def evaluate(self, sem):
        if self.constant_value() is None:
            signature = None
            for child in self.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child, None)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child, None)
                elif isinstance(child, AuxSTPredicate):
                    ret = EvaluateParams.evaluate_recursion(sem, child, AuxSymbolTable.predicate)
                    if ret.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                    elif not ret.returned_value:
                        sem.analyzer.error_mgr.add_error(FplAxiomNotSatisfiable(self))
                        sem.eval_stack[-1].value = InbuiltUndefined()
                    else:
                        # since the axiom is satisfiable, we 'assume' it to be true for the theory to come
                        sem.eval_stack[-1].value = True
                else:
                    raise NotImplementedError(str(type(child)))
            if len(signature.children) == 0:
                self.set_constant_value(sem.eval_stack[-1])
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
