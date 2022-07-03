from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTVariable import AuxSTVariable
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from fplerror import FplIdentifierNotDeclared, FplWrongArguments
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

    def get_type_signature(self):
        return self.reference.get_type_signature()

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
        self.reference = None
        self._calculate_argument_types(sem)
        self._check_if_referenced_id_exists(sem)
        # at this stage, there is exactly one override determined (even if is an InbuiltUndefined instance)
        if isinstance(self.reference, InbuiltUndefined):
            sem.eval_stack[-1].value = InbuiltUndefined()
            return
        # at this stage, we can call the predicate with args
        propagated_expected_type = sem.eval_stack[-1].expected_type
        arg_list = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.arg_list)
        # recursive call
        ret = EvaluateParams.evaluate_recursion(sem, self.reference, propagated_expected_type, list(arg_list.children))
        if ret.returned_value is None:
            sem.eval_stack[-1].value = InbuiltUndefined()
        else:
            EvaluateParams.propagate(sem, ret)
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
                self.reference = InbuiltUndefined()
            else:
                self._match_override(sem, sem.overridden_qualified_ids.get(qualified_identifier))
        elif self.outline == AuxSymbolTable.var:
            self._match_override([self.get_declared_type().get_type_node()])
        else:
            raise NotImplementedError()

    def _match_override(self, sem, expected_overrides: list):
        matching_overrides = list()
        for override in expected_overrides:
            if self._arguments_match_override(sem, override.reference):
                matching_overrides.append(override.reference)
        if len(matching_overrides) == 0:
            sem.analyzer.error_mgr.add_error(FplWrongArguments(self.__calc_signature_from_args(sem), self))
            self.reference = InbuiltUndefined()
        elif len(matching_overrides) > 1:
            raise NotImplementedError()
        else:
            self.reference = matching_overrides[0]

    def _arguments_match_override(self, sem, node):
        arg_types_list = sem.eval_stack[-1].arg_types_list
        signature_node = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.signature)
        if len(arg_types_list) == 0 and len(signature_node.children) == 0:
            return True
        for child in signature_node.children:
            raise NotImplementedError()

    def _calculate_argument_types(self, sem):
        # create a list of argument types to be matched with any of the available overrides
        args = AuxSymbolTable.get_child_by_outline(self, AuxSymbolTable.arg_list)
        arg_types_list = sem.eval_stack[-1].arg_types_list
        arg_value_list = sem.eval_stack[-1].arg_value_list
        for argument_node in args.children:
            if isinstance(argument_node, AuxSTPredicateWithArgs):
                # recursive call of for a new argument being itself a predicate with arguments
                argument_node.evaluate(sem)
                arg_types_list.append(argument_node.get_type_signature())
                arg_value_list.append(argument_node.get_value())
            elif isinstance(argument_node, AuxSTVariable):
                arg_types_list.append(argument_node.get_declared_type().get_type_signature())
                arg_value_list.append(argument_node.get_value())
            elif isinstance(argument_node, AuxSTSelf):
                arg_types_list.append(argument_node.get_declared_type().get_type_signature())
                arg_value_list.append(argument_node)
            elif isinstance(argument_node, AuxSTStatement):
                arg_types_list.append(AuxSymbolTable.undefined)
                arg_value_list.append(argument_node.get_value())
            else:
                arg_types_list.append(argument_node.get_type_signature())
                arg_value_list.append(argument_node.get_value())

    def __calc_signature_from_args(self, sem):
        ret = list()
        running_type = ""
        type_counter = 0
        arg_types_list = sem.eval_stack[-1].arg_types_list
        for current_type in arg_types_list:
            if running_type != current_type:
                if running_type != "":
                    ret.append(str(type_counter) + ":" + running_type)
                type_counter = 1
                running_type = current_type
            else:
                type_counter += 1
        if type_counter == 1 and len(ret) == 0:
            ret.append(str(type_counter) + ":" + running_type)
        elif type_counter > 0 and len(ret) == 0:
            ret.append(str(type_counter) + ":" + running_type)
        return self.reference.get_qualified_id() + "[" + ",".join(ret) + "]"
