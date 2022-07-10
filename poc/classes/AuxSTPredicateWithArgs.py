from poc.classes.AuxSTBlock import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate, EvaluatedPredicate
from fplerror import FplIdentifierNotDeclared, FplWrongArguments, FplPredicateRecursion, FplVariableNotInitialized
from poc.classes.AuxEvaluation import EvaluateParams


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
        self.reference = None

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateWithArgs(self._i))
        new_predicate.id = self.id
        new_predicate.outline = self.outline
        new_predicate.reference = self.reference
        new_predicate._value = self._value
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
        possible_overrides = self._check_if_referenced_id_exists(sem)
        if len(possible_overrides) == 0:
            # if no possible overrides found
            sem.eval_stack[-1].value = InbuiltUndefined()
            return

        # at this stage, we have a list of possible overrides, we now try to "call" them with the given arguments
        mismatched_overrides = list()
        for override in possible_overrides:
            propagated_expected_type = sem.eval_stack[-1].expected_type
            if self._check_illegal_recursion(sem, override):
                sem.analyzer.error_mgr.add_error(FplPredicateRecursion(override.reference, self))
                sem.eval_stack[-1].value = InbuiltUndefined()
                return
            ret = EvaluateParams.evaluate_recursion(sem, override.reference, propagated_expected_type, arg_list, True)
            if ret.argument_error is not None:
                mismatched_overrides.append(str(ret.argument_error))
            else:
                # break searching for matching overrides, if one was found
                break

        if len(mismatched_overrides) >= len(possible_overrides):
            arg_types = list()
            for type_node in ret.arg_type_list:
                arg_types.append(type_node.to_string2())
            sem.analyzer.error_mgr.add_error(FplWrongArguments(arg_types, mismatched_overrides, self))
            ret.returned_value = None

        if ret.returned_value is None:
            sem.eval_stack[-1].value = InbuiltUndefined()
        else:
            sem.eval_stack[-1].value = EvaluatedPredicate(ret.returned_value.get_repr())
        return

    def _check_if_referenced_id_exists(self, sem):
        if self.id[0].isupper():
            base_identifier = self.get_qualified_id()
        else:
            base_identifier = self.get_declared_type().get_qualified_id()
        parent_identifier = sem.eval_stack[-1].parent_identifier
        if parent_identifier != "":
            qualified_identifier = parent_identifier + "." + base_identifier
        else:
            qualified_identifier = base_identifier

        if self.id[0].isupper():
            if qualified_identifier not in sem.overridden_qualified_ids.dictionary():
                # the reference of the predicate_with_args is never declared
                sem.analyzer.error_mgr.add_error(
                    FplIdentifierNotDeclared(qualified_identifier, self.path[1].file_name, self.zfrom))
                return list()
            else:
                return sem.overridden_qualified_ids.get(qualified_identifier)
        elif self.outline == AuxSymbolTable.var:
            return [self.get_declared_type()]
        else:
            raise NotImplementedError()

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
                    sem.analyzer.error_mgr.add_error(FplVariableNotInitialized(argument_node))
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
                if eval_params.node == override.reference:
                    return True
