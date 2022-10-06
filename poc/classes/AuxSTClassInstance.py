from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTClassInstance(AuxSTInstance):

    def __init__(self, i):
        super().__init__(i)
        self.def_type = AuxSTConstants.classInstance
        self.zfrom = i.corrected_position('VariableType')
        self.zto = i.last_positions_by_rule['ClassInstance'].pos_to_str()

    def clone(self):
        new_class_instance = self._copy(AuxSTClassInstance(self._i))
        new_class_instance.id = self.id
        new_class_instance.def_type = self.def_type
        new_class_instance.zfrom = self.zfrom
        new_class_instance.to = self.zto
        new_class_instance.mandatory = self.mandatory
        new_class_instance._is_inherited = True
        return new_class_instance

    def evaluate(self, sem):
        type_node = None
        for child in self.children:
            if isinstance(child, AuxSTSignature):
                EvaluateParams.evaluate_recursion(sem, child)
            elif isinstance(child, AuxSTType):
                type_node = child
            elif isinstance(child, AuxSTVarSpecList):
                EvaluateParams.evaluate_recursion(sem, child)
            else:
                raise NotImplementedError(str(type(child)))
        # the value of the constructor is a wrapper object with the type of its class
        sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, type_node)
        self.set_sc_ready()

    def get_declared_type(self):
        if self._declared_type is None:
            # determine the class instance's type from the symbol table
            for child in self.children:
                if isinstance(child, AuxSTType):
                    self._declared_type = child
                    break
        return self._declared_type
