from poc.classes.AuxEvaluationRegister import AuxEvaluationRegister
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTableHelpers import AuxSymbolTableHelpers
from poc.classes.AuxParamsArgsMatcher import AuxParamsArgsMatcher


class AuxSTSignature(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.signature, i)
        self._list_named_declarations = None
        self._id = None
        self._i = i
        if 'Signature' in i.last_positions_by_rule:
            self.zfrom = i.corrected_position('PredicateIdentifier')
            self.zto = i.last_positions_by_rule['Signature'].pos_to_str()
        else:
            # in case of a default constructor there is no Signature parsed previously
            self.zfrom = ''
            self.zto = ''
        self._pointer_args = 0
        self._pointer_params = 0
        self._param_types = list()

    def set_id(self, identifier):
        self._id = identifier

    def set_params(self, list_named_declarations):
        self._list_named_declarations = list_named_declarations

    def make(self):
        if self._list_named_declarations is not None:
            for named_var_declaration in self._list_named_declarations:
                named_var_declaration.var_list.reverse()
                AuxSymbolTableHelpers.add_vars_to_node(self._i, self, named_var_declaration)

    def to_string(self):
        ret = self._id + "["
        first_found = False
        if self._list_named_declarations is not None:
            for named_var_declaration in self._list_named_declarations:
                if not first_found:
                    ret += named_var_declaration.to_string()
                    first_found = True
                else:
                    ret += "," + named_var_declaration.to_string()
        ret += "]"
        return ret

    def clone(self):
        new_signature = self._copy(AuxSTSignature(self._i))
        new_signature.set_id(self._id)
        new_signature.set_params(self._list_named_declarations)
        return new_signature

    def evaluate(self, sem):
        # if evaluate method of the signature get called, the corresponding FPL building block's
        # _next_input_arguments are already set
        register = sem.eval_stack[-1]
        current_building_block = register.building_block
        current_instance = current_building_block.get_instance(register.instance_guid)
        if current_instance.id != current_building_block.get_main_instance().id:
            # if this is not the main instance, i.e. it was called, we have input arguments.
            input_arguments = current_building_block.get_input_arguments()
        else:
            input_arguments = self._create_dummy_input_arguments(current_building_block, current_instance)
        for reg in input_arguments:
            current_instance.set_register(reg.node.get_long_id(), reg)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = "AuxSTSignature"
        return self._long_id

    def _create_dummy_input_arguments(self, building_block, instance):
        input_arguments = list()
        for child in self.children:
            register = AuxEvaluationRegister(child, None)
            register.building_block = building_block
            register.instance = instance
            register.instance_guid = instance.id
            register.value = InbuiltValueAtRuntime(child, child.children[0])
            input_arguments.append(register)
        return input_arguments
