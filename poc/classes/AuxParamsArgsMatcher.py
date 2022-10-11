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
                if not hasattr(type_arg, "type_pattern"):
                    type_arg = type_arg.get_declared_type()
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
        if isinstance(type_arg, InbuiltUndefined) or isinstance(type_param, InbuiltUndefined):
            # if any of the representations are undefined, return false
            return False

        # check consistency of types of the argument and the parameter it has to match
        if type_arg.is_predicate() and type_param.is_predicate():
            return True
        elif type_arg.is_functional_term() and type_param.is_functional_term():
            return True
        elif type_arg.is_generic() and type_param.is_generic():
            if type_param.get_scope().id == type_arg.get_scope().id:
                return type_param.id == type_arg.id
            else:
                # return true even if the names of the generic types are not the same if the
                # scope they are declared in are not the same
                return True
        elif type_arg.is_generic() and type_param.is_object():
            return True
        elif type_arg.is_object() and type_param.is_generic():
            return True
        elif type_arg.is_object() and type_param.is_object():
            if type_param.id == type_arg.id:
                # if after the proceedings checks the ids are equal, we have a match
                return True
            else:
                # even though there is was no match of IDs, we have already ensured the consistency of types.
                # In this case, we still have to check if the two consistent types
                # with different IDs are still compatible, for instance due to class inheritance.
                # The parameter has to 'accept' an argument if
                # the argument's type is a derived class of the parameter's type.
                if type_arg.is_object() and type_param.is_object():
                    if type_param.is_inbuilt_object():
                        # every object is derived from the inbuilt object
                        return True
                    elif type_arg.is_inbuilt_object():
                        # the inbuilt object is never a derived object
                        return False
                    else:
                        raise NotImplementedError()

        # in all other cases, return False (argument is not matching the parameter)
        return False
