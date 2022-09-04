from poc.classes.AuxBits import AuxBits
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxParamsArgsMatcher:

    def __init__(self):
        self._pointer_args = 0
        self._pointer_params = 0
        self._param_types = list()

    def try_match(self, sem, args_of_caller: list, params_of_signature: list):
        while self._try_match(sem, args_of_caller, params_of_signature):
            pass
        # pass any argument errors through to the calling node
        sem.eval_stack[-2].argument_error = sem.eval_stack[-1].argument_error

    def _try_match(self, sem, args_of_caller: list, params_of_signature: list):
        if self._pointer_args >= len(args_of_caller):
            if self._pointer_params < len(params_of_signature):
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
            else:
                return False
        else:
            if self._pointer_params >= len(params_of_signature):
                sem.eval_stack[-1].argument_error = self._param_types
                return False
            else:
                type_arg = args_of_caller[self._pointer_args]
                type_param = params_of_signature[self._pointer_params].children[0]
                if AuxParamsArgsMatcher.are_types_compatible(type_arg, type_param):
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
                    sem.eval_stack[-1].argument_error = self._param_types
                    return False

    @staticmethod
    def are_types_compatible(type_arg, type_param):
        # handy variables for the representations of the types
        arg_repr = type_arg.get_repr()
        param_repr = type_param.get_repr()
        if isinstance(param_repr, InbuiltUndefined) or isinstance(arg_repr, InbuiltUndefined):
            # if any of the representations are undefined, return false
            return False

        # check consistency of types of the argument and the parameter it has to match
        types_consistent = False
        if AuxBits.is_predicate(type_arg.type_pattern) and AuxBits.is_predicate(type_param.type_pattern):
            types_consistent = True
        elif AuxBits.is_functional_term(type_arg.type_pattern) and AuxBits.is_functional_term(type_param.type_pattern):
            types_consistent = True
        elif AuxBits.is_object(type_arg.type_pattern) and AuxBits.is_object(type_param.type_pattern):
            types_consistent = True
        if not types_consistent:
            return False

        if type_param.id == type_arg.id:
            # if after the proceedings checks the ids are equal, we have a match
            return True
        else:
            # even though there is was no match of IDs, we have already ensured the consistency of types.
            # In this case, we still have to check if the two consistent types with different IDs are still compatible,
            # for instance due to class inheritance. The parameter has to 'accept' an argument if
            # the argument's type is a derived class of the parameter's type.
            if AuxBits.is_object(type_arg.type_pattern) and AuxBits.is_object(type_param.type_pattern):
                return arg_repr.is_of_type(param_repr)

        # in all other cases, return False (argument is not matching the parameter)
        return False
