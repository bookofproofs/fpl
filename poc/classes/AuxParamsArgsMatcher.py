class AuxParamsArgsMatcher:

    def __init__(self):
        self._pointer_args = 0
        self._pointer_params = 0
        self._param_types = list()
        self._error_occurred = False

    def try_match(self, args_of_caller: list, params_of_signature: list):
        while self._try_match(args_of_caller, params_of_signature):
            pass
        return not self._error_occurred

    def _try_match(self, args_of_caller: list, params_of_signature: list):
        if self._pointer_args >= len(args_of_caller):
            if self._pointer_params < len(params_of_signature):
                type_param = params_of_signature[self._pointer_params].children[0]
                self._param_types.append(type_param.to_string2())
                self._pointer_params += 1
                if type_param.type_mod not in ["+", "*"]:
                    # flag an argument error unless the params are variadic
                    self._error_occurred = True
                elif type_param.type_mod == "+" and len(args_of_caller) == 0:
                    # the params are expect at least one parameter
                    self._error_occurred = True
                return True
            else:
                return False
        else:
            if self._pointer_params >= len(params_of_signature):
                self._error_occurred = True
                return False
            else:
                type_arg = args_of_caller[self._pointer_args].value.get_declared_type()
                type_param = params_of_signature[self._pointer_params].children[0]
                if type_param.accepts(type_arg):
                    if type_param.type_mod in ["+", "*"]:
                        self._pointer_args += 1
                    elif type_arg.type_mod in ["+", "*"]:
                        self._pointer_params += 1
                        self._param_types.append(type_param.to_string2())
                    else:
                        self._pointer_args += 1
                        self._pointer_params += 1
                        self._param_types.append(type_param.to_string2())
                    return True
                else:
                    self._pointer_args += 1
                    self._pointer_params += 1
                    self._param_types.append(type_param.to_string2())
                    self._error_occurred = True
                    return False
