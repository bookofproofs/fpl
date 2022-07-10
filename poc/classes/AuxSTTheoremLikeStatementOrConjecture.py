from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltPredicate, InbuiltUndefined, EvaluatedPredicate
from poc.classes.AuxSTBlock import AuxSTBlock
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList


class AuxSTTheoremLikeStatementOrConjecture(AuxSTBlock):

    def __init__(self, block_type, i, zfrom, zto):
        super().__init__(block_type, i)
        self.zfrom = zfrom
        self.zto = zto

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
                elif isinstance(child, AuxSTPredicate):
                    ret = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate())
                    if ret.returned_value is None:
                        sem.eval_stack[-1].value = InbuiltUndefined()
                        return
                else:
                    raise NotImplementedError(str(type(child)))
            # per default, we assume the truth of theorem-like statements
            # unless the evaluation of some of its sub-nodes was not successful
            sem.eval_stack[-1].value = EvaluatedPredicate(True)

            if len(signature.children) == 0:
                self.set_constant_value(sem.eval_stack[-1])
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
