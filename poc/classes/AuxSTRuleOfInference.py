from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltPredicate, InbuiltUndefined, EvaluatedPredicate
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTRuleOfInference(AuxSTBuildingBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_ir, i)
        self.zfrom = i.last_positions_by_rule['PredicateIdentifier'].pos_to_str()
        self.zto = i.last_positions_by_rule['RuleOfInference'].pos_to_str()
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
                    if child.outline == AuxSymbolTable.pre:
                        pre = ret.returned_value
                    elif child.outline == AuxSymbolTable.con:
                        con = ret.returned_value
                else:
                    raise NotImplementedError(str(type(child)))

            if pre is None or con is None:
                sem.eval_stack[-1].value = InbuiltUndefined(self)
                return
            # per default, we assume the truth of inference rules
            # unless the evaluation of some of its sub-nodes was not successful
            sem.eval_stack[-1].value = EvaluatedPredicate(self, True)

            if len(signature.children) == 0:
                self.set_constant_value(sem.eval_stack[-1])
        else:
            # replace the stack by the immutable value
            sem.eval_stack.pop()
            sem.eval_stack.append(self.constant_value())
        self.set_sc_ready()
