from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate
from poc.classes.AuxInbuiltValues import InbuiltValueNamedUndefined, InbuiltValueUndefined, \
    InbuiltValueAtRuntime, InbuiltValuePredicate, AuxInbuiltValue
from poc.classes.AuxSelfContainment import AuxReferenceType
from poc.classes.AuxParamsArgsMatcher import AuxParamsArgsMatcher
from poc.classes.AuxST import AuxST
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from fplerror import FplIdentifierNotDeclared, FplWrongArguments, FplPredicateRecursion, FplVariableNotInitialized


class AuxSTPredicateWithArgs(AuxST, AuxInterfaceSTType):

    def __init__(self, i):
        AuxInterfaceSTType.__init__(self)
        AuxST.__init__(self, AuxSTConstants.predicate_with_arguments, i)
        self.reference = None
        self._is_bound = False

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateWithArgs(self._i))
        new_predicate.id = self.id
        new_predicate.outline = self.outline
        new_predicate.reference = self.reference
        return new_predicate

    def evaluate(self, sem):
        """
        Checks if
        a) the referenced Pascal case identifier exists
        b) there is an override accepting the submitted arguments including their types in their respective order
        c) the type of the override corresponds to the type in the context of which self is used
        If all three are true, then the matched override will be 'called' with the current (contexts-specific)
        values of the arguments of self.
        :param sem:
        :return:
        """
        arg_list = self._calculate_arguments(sem)
        propagated_expected_type = sem.eval_stack[-1].expected_type
        if self.reference is None:
            # if the reference of this AuxSTPredicateWithArgs was never determined,
            # we first try to determine it.
            qualified_identifier = self._get_qualified_id(sem)
            if qualified_identifier[0].isupper() or "." in qualified_identifier:
                if qualified_identifier not in sem.overridden_qualified_ids.dictionary():
                    # if the qualified_identifier is not found, re-check the current scope
                    # (addressing properties directly and without "@self."
                    # inside the definition where there are declared)
                    scope = self.get_scope()
                    s = scope.id.split("[")
                    another_qualified_identifier = s[0] + "." + qualified_identifier
                    if another_qualified_identifier not in sem.overridden_qualified_ids.dictionary():
                        # the reference of the predicate_with_args is nowhere in the FPL sourcecode declared
                        sem.error_mgr.add_error(
                            FplIdentifierNotDeclared(qualified_identifier, self.path[1].file_name, self.zfrom))
                        self.reference = InbuiltValueNamedUndefined(self, qualified_identifier)
                    else:
                        ret = self.__get_possible_override(sem, another_qualified_identifier, propagated_expected_type,
                                                           arg_list)
                else:
                    ret = self.__get_possible_override(sem, qualified_identifier, propagated_expected_type, arg_list)
                if isinstance(self.reference, (InbuiltValueUndefined, InbuiltValueNamedUndefined)):
                    sem.eval_stack[-1].value = self.reference
                else:
                    # at this stage, if self.reference is not InbuiltUndefined, it is instead
                    # a matched override of the Pascal Case identifier somewhere in the FPL source code.
                    # In this case, ret contains an evaluated value of this override
                    # and we replace the stack by this evaluation
                    sem.eval_stack.pop()
                    sem.eval_stack.append(ret)
            elif qualified_identifier in ["pred", "predicate"]:
                declared_type = self.get_declared_type()
                if len(declared_type.children) > 0:
                    # if the predicate type has 'parameters', we also check if the arguments match them
                    param_list = AuxSymbolTable.get_child_by_outline(declared_type, AuxSTConstants.arg_list)
                    matcher = AuxParamsArgsMatcher()
                    matcher.try_match(sem, arg_list, list(param_list.children))
                    if sem.eval_stack[-1].argument_error is not None:
                        mismatched_overrides = list()
                        mismatched_overrides.append(str(sem.eval_stack[-1].argument_error))
                        self._issue_FplWrongArguments(sem, arg_list, mismatched_overrides)
                self.reference = InbuiltValuePredicate(self)
                sem.eval_stack[-1].value = self.reference
            else:
                raise NotImplementedError()
            if not self.get_scope().is_sc_ready():
                if propagated_expected_type.is_predicate():
                    sem.sc.add_reference(self.reference, self.get_scope(), AuxReferenceType.logical)
                else:
                    sem.sc.add_reference(self.reference, self.get_scope(), AuxReferenceType.semantical)
            # set the declared type of self to the declared type of its reference
            self.set_declared_type(self.reference.get_declared_type())
        else:
            # avoid re-evaluation of inbuilt values
            if not isinstance(self.reference, AuxInbuiltValue):
                ret = EvaluateParams.evaluate_recursion(sem, self.reference,
                                                        expected_type=propagated_expected_type,
                                                        arg_type_list=arg_list,
                                                        check_args=True,
                                                        building_block=self.reference,
                                                        instance_guid=self.reference.clone_main_instance().id)
                sem.eval_stack.pop()
            else:
                ret = sem.eval_stack.pop()
                # the value of this predicate with args is a wrapper object with the type of its reference
                ret.value = InbuiltValueAtRuntime(self, self.reference.get_declared_type())
            sem.eval_stack.append(ret)

    def __get_possible_override(self, sem, qualified_identifier, propagated_expected_type, arg_list):
        ret = sem.eval_stack[-1]
        possible_overrides = sem.overridden_qualified_ids.get(qualified_identifier)
        # at this stage, we have a list of possible overrides,
        # we now try to "call" them with the given arguments
        mismatched_overrides = list()
        for override in possible_overrides:
            if self._check_illegal_recursion(sem, override):
                sem.error_mgr.add_error(FplPredicateRecursion(override.reference, self))
                self.reference = InbuiltValueUndefined(self)
                break
            ret = EvaluateParams.evaluate_recursion(sem, override.reference,
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
            self._issue_FplWrongArguments(sem, ret.arg_type_list, mismatched_overrides)
            self.reference = InbuiltValueUndefined(self)

        return ret

    def _issue_FplWrongArguments(self, sem, arg_type_list, mismatched_overrides):
        arg_types = list()
        for type_node in arg_type_list:
            if isinstance(type_node, InbuiltUndefined):
                arg_types.append(type_node.to_string2() + "/" + type_node.id)
            else:
                arg_types.append(type_node.to_string2())
        sem.error_mgr.add_error(FplWrongArguments(arg_types, mismatched_overrides, self))

    def _get_qualified_id(self, sem):
        if self.id[0].isupper():
            base_identifier = self.get_qualified_id()
        else:
            base_identifier = self.get_declared_type().get_qualified_id()
        # check if the predecessor was an AuxSTQualified node
        if isinstance(sem.eval_stack[-2].node, AuxSTQualified):
            # if so, correct the qualified identifier by its identifier
            qualified_identifier = sem.eval_stack[-2].node.get_qualified_id() + "." + base_identifier
        else:
            qualified_identifier = base_identifier
        return qualified_identifier

    def _calculate_arguments(self, sem):
        # create a list of argument types to be matched with any of the available overrides
        args = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.arg_list)
        arg_type_list = list()
        for argument_node in args.children:
            if isinstance(argument_node, AuxSTPredicateWithArgs):
                # recursive call of for a new argument being itself a predicate with arguments
                argument_node.evaluate(sem)
                arg_type_list.append(argument_node.get_declared_type())
            elif isinstance(argument_node, AuxSTVariable):
                if not argument_node.is_bound_or_initialized():
                    sem.error_mgr.add_error(FplVariableNotInitialized(argument_node))
                arg_type_list.append(argument_node.get_declared_type())
            elif isinstance(argument_node, AuxSTSelf):
                arg_type_list.append(argument_node.get_declared_type())
            elif isinstance(argument_node, AuxSTStatement):
                arg_type_list.append(argument_node.get_declared_type())
            else:
                arg_type_list.append(argument_node.get_declared_type())
        return arg_type_list

    def _check_illegal_recursion(self, sem, override):
        if not isinstance(sem.eval_stack[-1].expected_type, InbuiltPredicate):
            return False
        else:
            for register in sem.eval_stack:
                if register.node == override.reference and override.reference is not None:
                    return True
            return False

    def set_is_bound(self):
        self._is_bound = True

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id
