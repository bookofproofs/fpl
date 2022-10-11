from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from anytree import search
from poc.fplerror import FplErrorManager


class AuxSTConstructor(AuxSTBuildingBlock):

    def __init__(self, i):
        super().__init__(AuxSTConstants.classConstructor, i)
        self.id = ""
        self._base_class_type = None

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        # Note: Default constructors are omitted since they do not declare any variables
        # but still are called in the loop (otherwise we would cause double-listing of the same errors).
        if self.outline != AuxSTConstants.classDefaultConstructor:
            # include the variables declared in the class (outer scope)
            classes_var_spec_list = AuxSymbolTable.get_child_by_outline(self.parent.parent, AuxSTConstants.var_spec)
            class_var_declarations = search.findall_by_attr(classes_var_spec_list, AuxSTConstants.var_decl,
                                                            AuxSTConstants.outline)
            for class_var_declaration in class_var_declarations:
                if class_var_declaration.id not in self._declared_vars:
                    # set the scope of the class variable to the end of the class
                    class_var_declaration.initialize_scope(self.parent.parent.zto)
                    # add the class variable declaration into a dictionary of the constructor for fast searching
                    self._declared_vars[class_var_declaration.id] = class_var_declaration
                else:
                    # we have a potential duplicate variable declaration
                    self.append_variable_already_declared(class_var_declaration, error_mgr, filename)

            # include constructor's own variables (i.e. both, its signature and body)
            own_var_declarations = search.findall_by_attr(self, AuxSTConstants.var_decl, AuxSTConstants.outline)
            for var_declaration in own_var_declarations:
                if var_declaration.id not in self._declared_vars:
                    # set the scope of the class variable to the end of the class
                    var_declaration.initialize_scope(self.parent.parent.zto)
                    # add the class variable declaration into a dictionary of the constructor for fast searching
                    self._declared_vars[var_declaration.id] = var_declaration
                else:
                    # we have a potential duplicate variable declaration
                    self.append_variable_already_declared(var_declaration, error_mgr, filename)

            # the used variables are only in the body
            self._used_vars += search.findall_by_attr(self, AuxSTConstants.var, AuxSTConstants.outline)
            self.filter_misused_templates(error_mgr, filename)

    def evaluate(self, sem):

        for child in self.children:
            if isinstance(child, AuxSTSignature):
                EvaluateParams.evaluate_recursion(sem, child)
            elif isinstance(child, AuxSTVarSpecList):
                EvaluateParams.evaluate_recursion(sem, child)
            elif isinstance(child, AuxSTPredicateWithArgs):
                # The semantics of any AuxSTPredicateWithArgs call inside the constructor of a class
                # is to call the constructor of its base class. Therefore, we expect the type of the base class
                ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=self.get_base_class_type(sem))
                # todo: we still have to embed the variables and asserted predicates
                # of the called base class inside the constructor's class instance
            else:
                raise NotImplementedError(str(type(child)))
        # the value of the constructor is a wrapper object with the type of its class
        sem.eval_stack[-1].value = InbuiltValueAtRuntime(self, self.parent.parent)
        self.set_sc_ready()

    def get_declared_type(self):
        if self._declared_type is None:
            # the type of the constructor corresponds to the type of its class
            self.set_declared_type(self.parent.parent.get_declared_type())
        return self._declared_type

    def get_base_class_type(self, sem):
        if self._base_class_type is None:
            # determine the
            base_class_id = self.parent.parent.class_types[0]
            base_class = sem.classes.identify_representative(base_class_id)
            self._base_class_type = base_class.reference.get_declared_type()
        return self._base_class_type
