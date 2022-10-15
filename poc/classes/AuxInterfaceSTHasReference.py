from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate
from poc.classes.AuxInbuiltValues import InbuiltValueNamedUndefined, InbuiltValueUndefined, InbuiltValuePredicate
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxParamsArgsMatcher import AuxParamsArgsMatcher
from poc.classes.AuxSelfContainment import AuxReferenceType
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from fplerror import FplWrongArguments, FplPredicateRecursion, FplVariableNotInitialized, FplIdentifierNotDeclared


class AuxInterfaceSTHasReference:

    def __init__(self):
        self.reference = None
        self._sem = None

    def set_sem(self, sem):
        self._sem = sem

    def calculate_arguments(self):
        # create a list of argument types to be matched with any of the available overrides
        args = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.arg_list)
        arg_type_list = list()
        for argument_node in args.children:
            if isinstance(argument_node, AuxInterfaceSTType):
                if argument_node.outline == AuxSTConstants.predicate_with_arguments:
                    # recursive call of for a new argument being itself a predicate with arguments
                    argument_node.evaluate(self._sem)
                elif argument_node.outline == AuxSTConstants.var:
                    if not argument_node.is_bound_or_initialized():
                        self._sem.error_mgr.add_error(FplVariableNotInitialized(argument_node))
                arg_type_list.append(argument_node.get_declared_type())
            else:
                raise NotImplementedError(str(type(argument_node)))
        return arg_type_list

    def establish_reference(self, arg_list, propagated_expected_type):
        # if the reference of this AuxSTPredicateWithArgs was never determined,
        # we first try to determine it.
        qualified_identifier = self._get_qualified_id_helper()
        if qualified_identifier[0].isupper() or "." in qualified_identifier:
            if qualified_identifier not in self._sem.overridden_qualified_ids.dictionary():
                # if the qualified_identifier is not found, re-check the current scope
                # (addressing properties directly and without "@self."
                # inside the definition where there are declared)
                scope = self.get_scope()
                s = scope.id.split("[")
                another_qualified_identifier = s[0] + "." + qualified_identifier
                if another_qualified_identifier not in self._sem.overridden_qualified_ids.dictionary():
                    # the reference of the predicate_with_args is nowhere in the FPL sourcecode declared
                    self._sem.error_mgr.add_error(
                        FplIdentifierNotDeclared(qualified_identifier, self.path[1].file_name, self.zfrom))
                    self.reference = InbuiltValueNamedUndefined(self, qualified_identifier)
                else:
                    ret = self._get_possible_override(another_qualified_identifier, propagated_expected_type,
                                                      arg_list)
            else:
                ret = self._get_possible_override(qualified_identifier, propagated_expected_type, arg_list)
            if isinstance(self.reference, (InbuiltValueUndefined, InbuiltValueNamedUndefined)):
                self._sem.eval_stack[-1].value = self.reference
            else:
                # at this stage, if self.reference is not InbuiltUndefined, it is instead
                # a matched override of the Pascal Case identifier somewhere in the FPL source code.
                # In this case, ret contains an evaluated value of this override
                # and we replace the stack by this evaluation
                self._sem.eval_stack.pop()
                self._sem.eval_stack.append(ret)
        elif qualified_identifier in ["pred", "predicate"]:
            declared_type = self.get_declared_type()
            if len(declared_type.children) > 0:
                # if the predicate type has 'parameters', we also check if the arguments match them
                param_list = AuxSymbolTable.get_child_by_outline(declared_type, AuxSTConstants.arg_list)
                matcher = AuxParamsArgsMatcher()
                matcher.try_match(self._sem, arg_list, list(param_list.children))
                if self._sem.eval_stack[-1].argument_error is not None:
                    mismatched_overrides = list()
                    mismatched_overrides.append(str(self._sem.eval_stack[-1].argument_error))
                    self._issue_wrong_arguments(arg_list, mismatched_overrides)
            self.reference = InbuiltValuePredicate(self)
            self._sem.eval_stack[-1].value = self.reference
        else:
            raise NotImplementedError()
        if not self.get_scope().is_sc_ready():
            if propagated_expected_type.is_predicate():
                self._sem.sc.add_reference(self.reference, self.get_scope(), AuxReferenceType.logical)
            else:
                self._sem.sc.add_reference(self.reference, self.get_scope(), AuxReferenceType.semantical)
        # set the declared type of self to the declared type of its reference
        self.set_declared_type(self.reference.get_declared_type())

    def _check_illegal_recursion(self, override):
        if not isinstance(self._sem.eval_stack[-1].expected_type, InbuiltPredicate):
            return False
        else:
            for register in self._sem.eval_stack:
                if register.node == override.reference and override.reference is not None:
                    return True
            return False

    def _issue_wrong_arguments(self, arg_type_list, mismatched_overrides):
        arg_types = list()
        for type_node in arg_type_list:
            if isinstance(type_node, InbuiltUndefined):
                arg_types.append(type_node.to_string2() + "/" + type_node.id)
            else:
                arg_types.append(type_node.to_string2())
        self._sem.error_mgr.add_error(FplWrongArguments(arg_types, mismatched_overrides, self))

    def _get_qualified_id_helper(self):
        if self.id[0].isupper():
            base_identifier = self.get_qualified_id()
        else:
            base_identifier = self.get_declared_type().get_qualified_id()
        # check if the predecessor was an AuxSTQualified node
        if isinstance(self._sem.eval_stack[-2].node, AuxSTQualified):
            # if so, correct the qualified identifier by its identifier
            qualified_identifier = self._sem.eval_stack[-2].node.get_qualified_id() + "." + base_identifier
        else:
            qualified_identifier = base_identifier
        return qualified_identifier

    def _get_possible_override(self, qualified_identifier, propagated_expected_type, arg_list):
        ret = self._sem.eval_stack[-1]
        possible_overrides = self._sem.overridden_qualified_ids.get(qualified_identifier)
        # at this stage, we have a list of possible overrides,
        # we now try to "call" them with the given arguments
        mismatched_overrides = list()
        for override in possible_overrides:
            if self._check_illegal_recursion(override):
                self._sem.error_mgr.add_error(FplPredicateRecursion(override.reference, self))
                self.reference = InbuiltValueUndefined(self)
                break
            ret = EvaluateParams.evaluate_recursion(self._sem, override.reference,
                                                    expected_type=propagated_expected_type,
                                                    arg_type_list=arg_list,
                                                    check_args=True,
                                                    building_block=override.reference,
                                                    instance_guid=override.reference.clone_main_instance().id)
            if ret.argument_error is not None:
                mismatched_overrides.append(str(ret.argument_error))
                override.reference.remove_instance(ret.instance_guid)
            else:
                # break searching for matching overrides, if one was found
                self.reference = override.reference
                break

        if len(mismatched_overrides) >= len(possible_overrides):
            self._issue_wrong_arguments(ret.arg_type_list, mismatched_overrides)
            self.reference = InbuiltValueUndefined(self)

        return ret




