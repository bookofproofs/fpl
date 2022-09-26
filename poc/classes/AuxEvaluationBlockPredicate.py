from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxSTProperties import AuxSTProperties
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList

"""
This class saves code that we would otherwise need to repeat in AuxSTDefinitionPredicate and AuxSTPredicateInstance
"""


class AuxEvaluationBlockPredicate:

    @staticmethod
    def evaluate(node, sem):
        if node.constant_value() is None:
            signature = None
            for child in node.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child),
                                                      sem.eval_stack[-1].arg_type_list,
                                                      sem.eval_stack[-1].check_args)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child))
                elif isinstance(child, (AuxSTPredicate, AuxSTPredicateWithArgs, AuxSTVariable)):
                    ret = EvaluateParams.evaluate_recursion(sem, child, InbuiltPredicate(child))
                    if ret.evaluation_error:
                        sem.eval_stack[-1].value = InbuiltUndefined(node)
                    else:
                        sem.eval_stack[-1].value = ret.value
                    if len(signature.children) == 0:
                        node.set_constant_value(sem.eval_stack[-1])
                elif isinstance(child, AuxSTProperties):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child))
                else:
                    raise NotImplementedError(str(type(child)))
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append( node.constant_value())
        node.set_sc_ready()

    @staticmethod
    def initialize_declared_type_of_predicate(predicate):
        # the predicate's block's type is the inbuilt predicate
        predicate.set_declared_type(InbuiltPredicate(predicate))
