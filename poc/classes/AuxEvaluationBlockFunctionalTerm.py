from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxSTProperties import AuxSTProperties
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList

"""
This class saves code that we would otherwise need to repeat in AuxSTDefinitionFunctionalTerm and 
AuxSTFunctionalTermInstance
"""


class AuxEvaluationBlockFunctionalTerm:

    @staticmethod
    def evaluate(node, sem):
        if node.constant_value() is None:
            type_pointer = None
            for child in node.children:
                if isinstance(child, (AuxSTSignature, AuxSTVarSpecList, AuxSTProperties)):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTType):
                    type_pointer = child
                else:
                    raise NotImplementedError(str(type(child)))
            sem.eval_stack[-1].value = InbuiltValueAtRuntime(node, type_pointer)
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(node.constant_value())
        node.set_sc_ready()

    @staticmethod
    def initialize_declared_type_of_functional_term(functional_term):
        for child in functional_term.children:
            if isinstance(child, AuxSTType):
                functional_term._declared_type = child
                break
