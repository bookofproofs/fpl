from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
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
            return_value = None
            for child in node.children:
                if isinstance(child, AuxSTSignature):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child))
                elif isinstance(child, AuxSTType):
                    return_value = child
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child))
                elif isinstance(child, AuxSTProperties):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(child))
                else:
                    raise NotImplementedError(str(type(child)))
            ret = sem.eval_stack.pop()
            ret.value = return_value
            sem.eval_stack.append(ret)
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(node.constant_value())
        node.set_sc_ready()

    def get_declared_type(self):
        if self._declared_type is None:
            self._initialize_declared_type()
        return self._declared_type

    @staticmethod
    def initialize_declared_type_of_functional_term(functional_term):
        for child in functional_term.children:
            if isinstance(child, AuxSTType):
                functional_term._declared_type = child
                break
