from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxInterfaceSTHasReference import AuxInterfaceSTHasReference
from poc.classes.AuxSTCoords import AuxSTCoords
from poc.classes.AuxSTRange import AuxSTRange
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVariable(AuxST, AuxInterfaceSTType, AuxInterfaceSTHasReference):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.var, i)
        AuxInterfaceSTHasReference.__init__(self)
        self.id = ""
        self.zto = i.last_positions_by_rule['Variable'].pos_to_str()
        self.zfrom = i.corrected_position('IdStartsWithSmallCase')
        self._is_bound = False
        self._is_initialized = False

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.id

    def clone(self):
        other = self._copy(AuxSTVariable(self._i))
        other.id = self.id
        other._is_bound = self._is_bound
        other._is_initialized = self._is_initialized
        return other

    def is_bound_or_initialized(self):
        return self._is_bound or self._is_initialized

    def set_is_bound(self):
        self._is_bound = True

    def evaluate(self, sem):
        self.initialize_has_reference_calculations(sem)
        if len(self.children) > 0:
            for child in self.children:
                if isinstance(child, AuxSTCoords):
                    raise NotImplementedError()
                elif isinstance(child, AuxSTRange):
                    raise NotImplementedError()
                elif isinstance(child, AuxSTQualified):
                    # due to the structure of symbol table, there can be only one child of self that is AuxSTQualified
                    propagated_expected_type = sem.eval_stack[-1].expected_type
                    check = EvaluateParams.evaluate_recursion(sem, child, expected_type=propagated_expected_type)
                    # set the value of self's evaluation to the value of the qualified identifier
                    sem.eval_stack[-1].value = check.value
                else:
                    raise NotImplementedError(type(child))
        else:
            instance = sem.eval_stack[-1].instance
            register = sem.eval_stack[-1]
            register_id = self.get_long_id()
            if not instance.has_register(register_id):
                # if the instance of the building block does not yet have a register for this variable
                register.value = InbuiltValueAtRuntime(self, self.get_declared_type())
                instance.set_register(register_id, register)
            # return the value of the variable to be the value of the register
            sem.eval_stack.pop()
            sem.eval_stack.append(instance.get_register(register_id))

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id
