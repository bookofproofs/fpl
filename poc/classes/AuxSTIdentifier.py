from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime, AuxInbuiltValue
from poc.classes.AuxInterfaceSTHasReference import AuxInterfaceSTHasReference
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTIdentifier(AuxST, AuxInterfaceSTType, AuxInterfaceSTHasReference):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.ids, i)
        AuxInterfaceSTHasReference.__init__(self)
        self.zto = ""
        self.zfrom = ""
        self.id = ""

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.outline

    def clone(self):
        other = self._copy(AuxSTIdentifier(self._i))
        other.id = self.id
        other._declared_type = self._declared_type
        other.reference = self.reference
        return other

    def evaluate(self, sem):
        self.initialize_has_reference_calculations(sem)
        if self.has_arguments():
            propagated_expected_type = sem.eval_stack[-1].expected_type
            if self.reference is None:
                self.establish_reference(self.get_arg_list(), propagated_expected_type)
            else:
                if isinstance(self.reference, AuxInbuiltValue):
                    # avoid re-evaluation of inbuilt values
                    ret = sem.eval_stack.pop()
                    # the value of this predicate with args is a wrapper object with the type of its reference
                    ret.value = InbuiltValueAtRuntime(self, self.reference.get_declared_type())
                else:
                    ret = EvaluateParams.evaluate_recursion(sem, self.reference,
                                                            expected_type=propagated_expected_type,
                                                            arg_type_list=self.get_arg_list(),
                                                            check_args=True,
                                                            building_block=self.reference,
                                                            instance_guid=self.reference.clone_main_instance().id)
                    sem.eval_stack.pop()
                sem.eval_stack.append(ret)
        else:
            if self.reference is None:
                if self._try_to_determine_reference(sem):
                    self.set_declared_type(self.reference.get_declared_type())
                else:
                    self.set_declared_type(InbuiltUndefined(self))
            sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def _try_to_determine_reference(self, sem):
        qualified_identifier = self.get_qualified_id()
        if qualified_identifier in sem.overridden_qualified_ids.dictionary():
            possible_overrides = sem.overridden_qualified_ids.get(qualified_identifier)
            self.reference = possible_overrides[0]
            return True
        return False
