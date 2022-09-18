from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltPredicate, InbuiltUndefined, EvaluatedPredicate
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTTheoremLikeStatementOrConjecture(AuxSTBuildingBlock):

    def __init__(self, block_type, i, zfrom, zto):
        super().__init__(block_type, i)
        self.zfrom = zfrom
        self.zto = zto
        # TheoremLikeStatementsOrConjectures are predicates per default
        self.set_declared_type(InbuiltPredicate(self))

    def evaluate(self, sem):
        sem.current_building_block = self
        if self.constant_value() is None:
            signature = None
            pre = None
            con = None
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
                    if child.outline == AuxSTConstants.pre:
                        pre = ret.returned_value
                    elif child.outline == AuxSTConstants.con:
                        con = ret.returned_value
                elif isinstance(child, AuxSTOutline):
                    if child.outline in [AuxSTConstants.block_cor_root, AuxSTConstants.block_proof_root]:
                        for sub_child in child.children:
                            EvaluateParams.evaluate_recursion(sem, sub_child, InbuiltUndefined(child))
                        sem.eval_stack[-1].value = InbuiltUndefined(child)
                else:
                    raise NotImplementedError(str(type(child)))

            if pre is None or con is None:
                sem.eval_stack[-1].value = InbuiltUndefined(self)
                return
            # per default, we assume the truth of theorem-like statements
            # unless the evaluation of some of its sub-nodes was not successful
            sem.eval_stack[-1].value = EvaluatedPredicate(self, True)

            if len(signature.children) == 0:
                self.set_constant_value(sem.eval_stack[-1])
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
        self.set_sc_ready()