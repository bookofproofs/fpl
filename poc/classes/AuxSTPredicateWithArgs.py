from poc.classes.AuxBits import AuxBits
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate, EvaluatedPredicate, InbuiltFunctionalTerm, \
    NamedUndefined, AuxInbuiltType
from poc.classes.AuxSelfContainment import AuxReferenceType
from poc.classes.AuxSTBuildingBlock import AuxST
from poc.classes.AuxParamsArgsMatcher import AuxParamsArgsMatcher
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSymbolTable import AuxSymbolTable
from fplerror import FplIdentifierNotDeclared, FplWrongArguments, FplPredicateRecursion, FplVariableNotInitialized


class AuxSTPredicateWithArgs(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
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
                    # the reference of the predicate_with_args is nowhere in the FPL sourcecode declared
                    sem.error_mgr.add_error(
                        FplIdentifierNotDeclared(qualified_identifier, self.path[1].file_name, self.zfrom))
                    self.reference = NamedUndefined(self, qualified_identifier)
                else:
                    possible_overrides = sem.overridden_qualified_ids.get(qualified_identifier)
                    # at this stage, we have a list of possible overrides,
                    # we now try to "call" them with the given arguments
                    mismatched_overrides = list()
                    for override in possible_overrides:
                        if self._check_illegal_recursion(sem, override):
                            sem.error_mgr.add_error(FplPredicateRecursion(override.reference, self))
                            self.reference = InbuiltUndefined(self)
                            break
                        ret = EvaluateParams.evaluate_recursion(sem, override.reference, propagated_expected_type,
                                                                arg_list, True)
                        if ret.argument_error is not None:
                            mismatched_overrides.append(str(ret.argument_error))
                        else:
                            # break searching for matching overrides, if one was found
                            self.reference = override.reference
                            break

                    if len(mismatched_overrides) >= len(possible_overrides):
                        self._issue_FplWrongArguments(sem, ret.arg_type_list, mismatched_overrides)
                        self.reference = InbuiltUndefined(self)
                if not isinstance(self.reference, (InbuiltUndefined, NamedUndefined)):
                    # at this stage, only if self.reference is not InbuiltUndefined, it is instead
                    # a matched override of the Pascal Case identifier somewhere in the FPL source code.
                    # In this case, ret contains an evaluated return value of this override
                    # and we replace the stack by this evaluation
                    sem.eval_stack.pop()
                    sem.eval_stack.append(ret)
                else:
                    sem.eval_stack[-1].value = self.reference
            elif qualified_identifier in ["pred", "predicate"]:
                declared_type = self.get_declared_type()
                if len(declared_type.children) > 0:
                    # if the predicate type has 'parameters', we also check if the arguments match them
                    param_list = AuxSymbolTable.get_child_by_outline(declared_type, AuxSymbolTable.arg_list)
                    matcher = AuxParamsArgsMatcher()
                    matcher.try_match(sem, arg_list, list(param_list.children))
                    if sem.eval_stack[-1].argument_error is not None:
                        mismatched_overrides = list()
                        mismatched_overrides.append(str(sem.eval_stack[-1].argument_error))
                        self._issue_FplWrongArguments(sem, arg_list, mismatched_overrides)
                self.reference = InbuiltPredicate(self)
                sem.eval_stack[-1].value = self.reference
            else:
                raise NotImplementedError()
            if not sem.current_building_block.is_sc_ready():
                if AuxBits.is_predicate(propagated_expected_type.type_pattern):
                    sem.sc.add_reference(self.reference, sem.current_building_block, AuxReferenceType.logical)
                else:
                    sem.sc.add_reference(self.reference, sem.current_building_block, AuxReferenceType.semantical)
            # set the declared type of self to the declared type of its reference, unless it is inbuilt
            if isinstance(self.reference, AuxInbuiltType):
                # prevent infinite recursion, since the inbuilt types have no declared types on their own
                self.set_declared_type(self.reference)
            else:
                self.set_declared_type(self.reference.get_declared_type())
        else:
            # avoid re-evaluation of inbuilt types
            if not isinstance(self.reference, AuxInbuiltType):
                ret = EvaluateParams.evaluate_recursion(sem, self.reference, propagated_expected_type,
                                                        arg_list, True)
                sem.eval_stack.pop()
                sem.eval_stack.append(ret)

    def _issue_FplWrongArguments(self, sem, arg_type_list, mismatched_overrides):
        arg_types = list()
        for type_node in arg_type_list:
            if isinstance(type_node.get_repr(), InbuiltUndefined):
                arg_types.append(type_node.to_string2() + "/" + type_node.get_repr().id)
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
        args = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.arg_list)
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
        if not isinstance(sem.eval_stack[-1].expected_type, (InbuiltPredicate, EvaluatedPredicate)):
            return False
        else:
            for eval_params in sem.eval_stack:
                if eval_params.node == override.reference and override.reference is not None:
                    return True
            return False

    def set_is_bound(self):
        self._is_bound = True
