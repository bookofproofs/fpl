from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


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
        args_of_caller = sem.eval_stack[-1].arg_type_list
        if sem.eval_stack[-1].check_args:
            params_of_signature = list(self.children)
            self._pointer_args = 0
            self._pointer_params = 0
            self._param_types.clear()
            while self._try_match(sem, args_of_caller, params_of_signature):
                pass
            # pass any argument errors through to the calling node
            sem.eval_stack[-2].argument_error = sem.eval_stack[-1].argument_error
        sem.eval_stack[-1].value = InbuiltUndefined()

    def _try_match(self, sem, args_of_caller: list, params_of_signature: list):
        if self._pointer_args >= len(args_of_caller) and self._pointer_params < len(params_of_signature):
            type_param = params_of_signature[self._pointer_params].children[0]
            self._param_types.append(type_param.to_string2())
            self._pointer_params += 1
            if type_param.type_mod not in ["+", "*"]:
                # flag an argument error unless the params are variadic
                sem.eval_stack[-1].argument_error = self._param_types
            elif type_param.type_mod == "+" and len(args_of_caller) == 0:
                # the params are expect at least one parameter
                sem.eval_stack[-1].argument_error = self._param_types
            return True
        elif self._pointer_args < len(args_of_caller) and self._pointer_params >= len(params_of_signature):
            self._pointer_args += 1
            return True
        elif self._pointer_args >= len(args_of_caller) and self._pointer_params >= len(params_of_signature):
            return False
        else:
            type_arg = args_of_caller[self._pointer_args]
            type_param = params_of_signature[self._pointer_params].children[0]
            if type_param.id == type_arg.id:
                if type_param.type_mod in ["+", "*"]:
                    self._pointer_args += 1
                elif type_arg.type_mod in ["+", "*"]:
                    self._pointer_params += 1
                    self._param_types.append(type_param.to_string2())
                else:
                    self._pointer_args += 1
                    self._pointer_params += 1
                    self._param_types.append(type_param.to_string2())
            else:
                self._pointer_args += 1
                self._pointer_params += 1
                self._param_types.append(type_param.to_string2())
                sem.eval_stack[-1].argument_error = self._param_types
        return True
