from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate, EvaluatedPredicate
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTStatement import AuxSTStatement
from fplerror import FplAxiomNotSatisfiable


class AuxSTAxiom(AuxSTBuildingBlock):

    def __init__(self, i):
        super().__init__(AuxSTConstants.block_axiom, i)
        self.zfrom = i.corrected_position('AxiomHeader')
        self.zto = i.last_positions_by_rule['Axiom'].pos_to_str()
        self.keyword = ""
        # Axioms are predicates per default
        self.set_declared_type(InbuiltPredicate(self))

    def evaluate(self, sem):
        sem.current_building_block = self
        if self.constant_value() is None:
            signature = None
            for child in self.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child),
                                                      sem.eval_stack[-1].arg_type_list,
                                                      sem.eval_stack[-1].check_args)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child))
                elif isinstance(child, AuxSTPredicate):
                    ret = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate(child))
                    if ret.evaluation_error:
                        sem.eval_stack[-1].value = InbuiltUndefined(self)
                    elif not ret.value.get_repr():
                        sem.error_mgr.add_error(FplAxiomNotSatisfiable(self))
                        sem.eval_stack[-1].value = InbuiltUndefined(self)
                    else:
                        # since the axiom is satisfiable, we 'assume' it to be true for the theory to come
                        sem.eval_stack[-1].value = EvaluatedPredicate(self, True)
                elif isinstance(child, AuxSTStatement):
                    # handle the 'is' statement
                    ret = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate(child))
                    if ret.evaluation_error:
                        sem.eval_stack[-1].value = InbuiltUndefined(self)
                    else:
                        # since the axiom is satisfiable, we 'assume' it to be true for the theory to come
                        sem.eval_stack[-1].value = EvaluatedPredicate(self, True)
                else:
                    raise NotImplementedError(str(type(child)))
            if len(signature.children) == 0:
                self.set_constant_value(sem.eval_stack[-1])
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
        self.set_sc_ready()
