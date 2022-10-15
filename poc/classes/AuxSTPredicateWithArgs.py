from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime, AuxInbuiltValue
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxInterfaceSTHasReference import AuxInterfaceSTHasReference
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTPredicateWithArgs(AuxST, AuxInterfaceSTType, AuxInterfaceSTHasReference):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.predicate_with_arguments, i)
        AuxInterfaceSTHasReference.__init__(self)
        self._is_bound = False

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateWithArgs(self._i))
        new_predicate.id = self.id
        new_predicate.outline = self.outline
        new_predicate.reference = self.reference
        return new_predicate

    def evaluate(self, sem):
        self.set_sem(sem)
        arg_list = self.calculate_arguments()
        propagated_expected_type = sem.eval_stack[-1].expected_type
        if self.reference is None:
            self.establish_reference(arg_list, propagated_expected_type)
        else:
            if isinstance(self.reference, AuxInbuiltValue):
                # avoid re-evaluation of inbuilt values
                ret = sem.eval_stack.pop()
                # the value of this predicate with args is a wrapper object with the type of its reference
                ret.value = InbuiltValueAtRuntime(self, self.reference.get_declared_type())
            else:
                ret = EvaluateParams.evaluate_recursion(sem, self.reference,
                                                        expected_type=propagated_expected_type,
                                                        arg_type_list=arg_list,
                                                        check_args=True,
                                                        building_block=self.reference,
                                                        instance_guid=self.reference.clone_main_instance().id)
                sem.eval_stack.pop()
            sem.eval_stack.append(ret)

    def set_is_bound(self):
        self._is_bound = True

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id
