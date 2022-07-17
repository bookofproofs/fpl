from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxParamsArgsMatcher import AuxParamsArgsMatcher


class AuxSTSignature(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.signature, i)
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
                AuxSymbolTable.add_vars_to_node(self._i, self, named_var_declaration)

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
        matcher = AuxParamsArgsMatcher()
        args_of_caller = sem.eval_stack[-1].arg_type_list
        if sem.eval_stack[-1].check_args:
            params_of_signature = list(self.children)
            matcher.try_match(sem, args_of_caller, params_of_signature)
        sem.eval_stack[-1].value = InbuiltUndefined()
