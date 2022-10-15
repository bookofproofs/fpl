from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
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
            new_value = InbuiltValuePredicate(node)
            sem.eval_stack[-1].value = new_value
            for child in node.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, (AuxSTPredicate, AuxSTPredicateWithArgs, AuxSTVariable)):
                    ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
                    if ret.evaluation_error:
                        new_value.set_undetermined()
                    else:
                        new_value.set_to(ret.value.get_value())
                    if len(signature.children) == 0:
                        node.set_constant_value(sem.eval_stack[-1])
                elif isinstance(child, AuxSTProperties):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxInterfaceSTType):
                    ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
                    if ret.evaluation_error:
                        new_value.set_undetermined()
                    else:
                        new_value.set_to(ret.value.get_value())
                else:
                    EvaluateParams.evaluate_recursion(sem, child)
                    new_value.set_undetermined()
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append( node.constant_value())
        node.set_sc_ready()

    @staticmethod
    def initialize_declared_type_of_predicate(predicate):
        # the predicate's block's type is the inbuilt predicate
        predicate.set_declared_type(InbuiltPredicate(predicate))
