from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTStatementIsOp import AuxSTStatementIsOp
from fplerror import FplAxiomNotSatisfiable


class AuxSTAxiom(AuxSTBuildingBlock, AuxInterfaceSTType):

    def __init__(self, i):
        super().__init__(AuxSTConstants.block_axiom, i)
        self.zfrom = i.corrected_position('AxiomHeader')
        self.zto = i.last_positions_by_rule['Axiom'].pos_to_str()
        self.keyword = ""
        # Axioms are predicates per default
        self.set_declared_type(InbuiltPredicate(self))

    def evaluate(self, sem):
        if self.constant_value() is None:
            signature = None
            new_value = InbuiltValuePredicate(self)
            sem.eval_stack[-1].value = new_value
            for child in self.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTPredicate):
                    ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
                    if ret.evaluation_error:
                        new_value.set_undetermined()
                    elif not ret.value.get_value():
                        sem.error_mgr.add_error(FplAxiomNotSatisfiable(self))
                        new_value.set_false()
                    else:
                        # since the axiom is satisfiable, we 'assume' it to be true for the theory to come
                        new_value.set_true()
                elif isinstance(child, AuxSTStatementIsOp):
                    # handle the 'is' statement
                    ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
                    if ret.evaluation_error:
                        new_value.set_undetermined()
                    else:
                        # since the axiom is satisfiable, we 'assume' it to be true for the theory to come
                        new_value.set_true()
                else:
                    raise NotImplementedError(str(type(child)))
            if len(signature.children) == 0:
                self.set_constant_value(sem.eval_stack[-1])
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
        self.set_sc_ready()
