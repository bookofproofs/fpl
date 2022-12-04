from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltPredicate, InbuiltUndefined
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate, InbuiltValueUndefined
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
        if self.constant_value() is None:
            new_value = InbuiltValuePredicate(self)
            sem.eval_stack[-1].value = new_value
            signature = None
            pre = None
            con = None
            for child in self.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTPredicate):
                    ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
                    if child.outline == AuxSTConstants.pre:
                        pre = ret
                    elif child.outline == AuxSTConstants.con:
                        con = ret
                elif isinstance(child, AuxSTOutline):
                    if child.outline in [AuxSTConstants.block_cor_root, AuxSTConstants.block_proof_root]:
                        for sub_child in child.children:
                            EvaluateParams.evaluate_recursion(sem, sub_child)
                else:
                    raise NotImplementedError(str(type(child)))

            if pre.evaluation_error:
                new_value.set_undetermined()
            elif con.evaluation_error:
                new_value.set_undetermined()
            else:
                new_value.set_true()
                new_value.set_expression(True)

            if len(signature.children) == 0:
                self.set_constant_value(new_value)
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
        self.set_sc_ready()
