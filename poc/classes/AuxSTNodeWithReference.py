from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime, InbuiltValueUndefined, AuxInbuiltValue, \
    InbuiltValueNamedUndefined
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTCoords import AuxSTCoords
from poc.classes.AuxSTRange import AuxSTRange
from poc.classes.AuxSTExt import AuxSTExt
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxST import AuxST
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from fplerror import FplWrongArguments, FplIdentifierNotDeclared, FplVariableNotInitialized, FplIllegalRecursion


class AuxSTNodeWithReference(AuxST, AuxInterfaceSTType):

    def __init__(self, outline, i):
        AuxST.__init__(self, outline, i)
        AuxInterfaceSTType.__init__(self)
        self.id = ""
        self.reference = None
        self._sem = None
        self._arity = -1
        self._has_args = None
        self._arg_list = list()
        self._possible_overrides = list()
        self._override_id = ""
        self._reference_established = None

    def to_string(self):
        """
        Provides an interface for the to_string() method of AuxSTType, child of which AuxSTVariable can be.
        :return: id of the variable
        """
        return self.id

    def evaluate(self, sem):
        if self.outline != AuxSTConstants.ids:
            self.initialize_has_reference_calculations(sem)
        if self.get_arity() >= 0:
            evaluated_arguments = list()
            # if this AuxInterfaceSTHasReference has arguments, evaluate them first
            error_for_some_argument_detected = False
            for argument in self.get_argument_list():
                # try to evaluate each argument according to its expected declared type
                ret = EvaluateParams.evaluate_recursion(sem, argument, expected_type=argument.get_declared_type())
                if ret.evaluation_error:
                    error_for_some_argument_detected = True
                evaluated_arguments.append(ret)
            if error_for_some_argument_detected:
                # since the arguments cannot be evaluated, the whole evaluation fails
                sem.eval_stack[-1].value = InbuiltValueUndefined(self)
            else:
                if self.has_overrides():
                    # case self.has_overrides() and self.get_arity() >= 0 and all arguments could be evaluated:
                    # here, we have to try out each override to find the right one
                    propagated_expected_type = sem.eval_stack[-1].expected_type
                    if self.reference_established(evaluated_arguments):
                        if self._check_illegal_recursion():
                            self._sem.error_mgr.add_error(FplIllegalRecursion(self.reference))
                            sem.eval_stack[-1].value = InbuiltValueUndefined(self)
                        else:
                            ret = EvaluateParams.evaluate_recursion(sem, self.reference,
                                                                    expected_type=propagated_expected_type,
                                                                    building_block=self.reference,
                                                                    instance_guid=self.reference.clone_main_instance().id)
                            sem.eval_stack.pop()
                            sem.eval_stack.append(ret)
                    else:
                        # since the reference could not be established, flag wrong arguments
                        self._flag_wrong_arguments()
                        sem.eval_stack[-1].value = InbuiltValueUndefined(self)
                else:
                    sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())
        else:
            if self.has_overrides():
                # case self.has_overrides() and self.get_arity() < 0:
                if self.outline == AuxSTConstants.var:
                    # for variables, this case is normal
                    sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())
                else:
                    # each override will need at least 0 arguments, so we flag FplWrongArguments
                    self._flag_wrong_arguments()
                    sem.eval_stack[-1].value = InbuiltValueUndefined(self)
            else:
                # case not self.has_overrides() and self.get_arity() < 0:
                if self.reference_established(list()):
                    sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())
                else:
                    # since the reference could not be established,
                    if self.id[0].isupper():
                        # if the identifier is PascalCase,
                        # flag FplIdentifierNotDeclared
                        sem.error_mgr.add_error(FplIdentifierNotDeclared(self.id, self.path[1].file_name, self.zfrom))
                        sem.eval_stack[-1].value = InbuiltValueUndefined(self)
                    else:
                        sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.get_declared_type())

        self._set_evaluated_register(sem)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.id
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def _set_evaluated_register(self, sem):
        instance = sem.eval_stack[-1].instance
        register = sem.eval_stack[-1]
        register_id = self.get_long_id()
        if not instance.has_register(register_id):
            instance.set_register(register_id, register)

    def _flag_wrong_arguments(self):
        arg_types = list()
        if self.has_arguments():
            for node in self.get_argument_list():
                arg_types.append(node.get_declared_type().to_string2())
        mismatched_overrides = list()
        if self.has_overrides():
            for node in self.get_overrides():
                mismatched_overrides.append(node.reference.get_signature_types())
        self._sem.error_mgr.add_error(FplWrongArguments(arg_types, mismatched_overrides, self))

    def initialize_has_reference_calculations(self, sem):
        self._sem = sem
        if self._has_args is None:
            args_found = False
            for child in self.children:
                if child.outline == AuxSTConstants.arg_list:
                    self._has_args = True
                    self._arity = len(child.children)
                    args_found = True
                    self._calculate_arguments()
                    break
            if not args_found:
                self._has_args = False
        self._find_possible_overrides()

    def has_arguments(self):
        return self._has_args

    def get_arity(self):
        return self._arity

    def get_argument_list(self):
        return self._arg_list

    def has_overrides(self):
        return len(self._possible_overrides) > 0

    def get_overrides(self):
        return self._possible_overrides

    def get_override_id(self):
        return self._override_id

    def _find_possible_overrides(self):
        self._possible_overrides = list()
        self._establish_override_id()
        if self._override_id[0].isupper() or "." in self._override_id:
            self.__find_possible_overrides_for_pascal_case()

    def __find_possible_overrides_for_pascal_case(self):
        """
        Tries to find all possible overrides based on a PascalCase identifier, which is the FPL convention
        for user-defined identifiers. Issues the FplIdentifierNotDeclared error, if not found.
        :return: None, internal variable self._possible_overrides will be empty if not. Otherwise, it will contain a
        list of possible overrides.
        """
        if self._override_id not in self._sem.overridden_qualified_ids.dictionary():
            # if the qualified_identifier is not found, re-check the current scope
            # (addressing properties directly and without "@self."
            # inside the definition where there are declared)
            scope = self.get_scope()
            s = scope.id.split("[")
            another_override_id = s[0] + "." + self._override_id
            if another_override_id not in self._sem.overridden_qualified_ids.dictionary():
                # the reference of the predicate_with_args is nowhere in the FPL sourcecode declared
                self._sem.error_mgr.add_error(
                    FplIdentifierNotDeclared(self._override_id, self.path[1].file_name, self.zfrom))
                self.reference = InbuiltValueNamedUndefined(self, self._override_id)
                self.reference.set_declared_type(self.reference.get_declared_type())
            else:
                self._possible_overrides.extend(self._sem.overridden_qualified_ids.get(another_override_id))
        else:
            self._possible_overrides.extend(self._sem.overridden_qualified_ids.get(self._override_id))

    def _calculate_arguments(self):
        # create a list of argument types to be matched with any of the available overrides
        args = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.arg_list)
        self._arg_list = list()
        for argument_node in args.children:
            if isinstance(argument_node, AuxInterfaceSTType):
                if argument_node.outline == AuxSTConstants.var:
                    if not argument_node.is_bound_or_initialized():
                        self._sem.error_mgr.add_error(FplVariableNotInitialized(argument_node))
                self._arg_list.append(argument_node)
            else:
                raise NotImplementedError(str(type(argument_node)))

    def _check_illegal_recursion(self):
        for register in self._sem.eval_stack:
            if register.node == self.reference and self.reference is not None:
                return True
        return False

    def _establish_override_id(self):
        if self.id[0].isupper():
            base_identifier = self.get_qualified_id()
        else:
            base_identifier = self.get_declared_type().get_qualified_id()
        # check if the predecessor was an AuxSTQualified node
        if isinstance(self.parent, AuxSTQualified):
            # if so, correct the qualified identifier by its identifier
            if self.parent.parent.outline == AuxSTConstants.selfInstance:
                self._override_id = self.parent.parent.get_qualified_id() + "." + base_identifier
            else:
                self._override_id = self.parent.parent.get_declared_type().get_qualified_id() + "." + base_identifier
        else:
            self._override_id = base_identifier
        if "." in self._override_id:
            return
        elif self._override_id[0].isupper():
            if self._override_id not in self._sem.overridden_qualified_ids.dictionary():
                # if the qualified_identifier is not found, re-check the current scope
                scope = self.get_scope()
                if scope.outline == AuxSTConstants.block_def:
                    # for all definitions, it might be that the user wants to address a property in the scope
                    s = scope.id.split("[")
                    self._override_id = s[0] + "." + self._override_id

    def reference_established(self, evaluated_arguments):
        if self._reference_established is None:
            if len(self._possible_overrides) == 0:
                self._reference_established = False
            else:
                for node in self._possible_overrides:
                    # set the declared type of self to the declared type of the building block we are checking
                    # we will need this setting even if no reference can be found.
                    if node.reference.outline == AuxSTConstants.block_def and \
                            node.reference.def_type == AuxSTConstants.classDeclaration:
                        # classes can never match something with arguments
                        pass
                    elif node.reference.arguments_match(evaluated_arguments):
                        # we have found a matching override
                        self.reference = node.reference
                        self._reference_established = True
                        return self._reference_established
                # no matching override found
                self._reference_established = False
        return self._reference_established

