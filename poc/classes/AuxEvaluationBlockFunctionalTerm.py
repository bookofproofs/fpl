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
        sem.analyzer.current_building_block = node
        if node.constant_value() is None:
            signature = None
            for child in node.children:
                if isinstance(child, AuxSTSignature):
                    signature = child
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined(),
                                                      sem.eval_stack[-1].arg_type_list,
                                                      sem.eval_stack[-1].check_args)
                elif isinstance(child, AuxSTType):
                    # remember the expected functional term return type
                    sem.analyzer.current_func_term_return_type = child
                    # set the node's declared type to the return type of the functional term
                    node.set_declared_type(child)
                elif isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined())
                    # forget the expected functional term return type
                    sem.analyzer.current_func_term_return_type = None
                elif isinstance(child, AuxSTProperties):
                    EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined())
                else:
                    raise NotImplementedError(str(type(child)))
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(node.constant_value())
        node.set_sc_ready()
