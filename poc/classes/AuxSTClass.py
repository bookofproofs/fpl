from anytree import search
from poc.classes.AuxBits import AuxBits
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltValues import InbuiltValueAtRuntime
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSelfContainment import AuxReferenceType
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTArgs import AuxSTArgs
from poc.classes.AuxSTBuildingBlock import AuxSTBuildingBlock
from poc.classes.AuxSTClassInstance import AuxSTClassInstance
from poc.classes.AuxSTConstructors import AuxSTConstructors
from poc.classes.AuxSTFunctionalTermInstance import AuxSTFunctionalTermInstance
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTPredicateInstance import AuxSTPredicateInstance
from poc.classes.AuxSTIdentifier import AuxSTIdentifier
from poc.classes.AuxSTProperties import AuxSTProperties
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTStatementAssign import AuxSTStatementAssign
from poc.classes.AuxSTStatementReturn import AuxSTStatementReturn
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplErrorManager


class AuxSTClass(AuxSTBuildingBlock):

    def __init__(self, i):
        AuxSTBuildingBlock.__init__(self, AuxSTConstants.block_def, i)
        self.class_types = []
        self.def_type = AuxSTConstants.classDeclaration
        self.id = ""
        self._content = None
        self.zfrom = i.corrected_position('ClassHeader')
        self.zto = i.last_positions_by_rule['DefinitionClass'].pos_to_str()
        self.keyword = ""
        self._hip = False

    def add_type(self, class_type: str):
        if class_type not in AuxRuleDependencies.dep["ObjectHeader"]:
            self.class_types.append(class_type)

    def initialize_vars(self, filename, error_mgr: FplErrorManager):
        # The declared variables of a class are in its variable specification list only.
        # (i.e. do not consider the sub-scopes of constructors and properties)
        var_spec_list_node = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.var_spec)

        declared_vars_tuple = search.findall_by_attr(var_spec_list_node, AuxSTConstants.var_decl,
                                                     AuxSTConstants.outline)
        for var_declaration in declared_vars_tuple:
            if var_declaration.id not in self._declared_vars:
                # set the scope of the variable
                var_declaration.initialize_scope(self.zto)
                # add the variable declaration into a dictionary for fast searching
                self._declared_vars[var_declaration.id] = var_declaration
            else:
                # we have a potential duplicate variable declaration
                self.append_variable_already_declared(var_declaration, error_mgr, filename)

        # The used variables might be spread across the scope of the class, including its constructors and properties.
        # However, we omit those scopes because they have their own _used_vars tuples. Thus, we have to limit
        # The used variables of a class are, therefore, limited to the scope of the class without the scopes
        # of its sub nodes.
        self._used_vars = search.findall_by_attr(var_spec_list_node, AuxSTConstants.var, AuxSTConstants.outline)
        self.filter_misused_templates(error_mgr, filename)

    def create_callers_parent_properties(self, parent_class):
        """
        This method creates callers of all the properties of the parent class unless there are
        already properties with the same name overriding those parent properties
        :return:
        """
        self._hip = True
        self.get_declared_type().register_base_class(parent_class.get_declared_type().id)
        parents_properties = AuxSymbolTable.get_child_by_outline(parent_class, AuxSTConstants.properties)
        my_properties = AuxSymbolTable.get_child_by_outline(self, AuxSTConstants.properties)
        for parent_property in parents_properties.children:
            if parent_property.base_id() in my_properties.children:
                # the property was overridden exists
                pass
            else:
                if isinstance(parent_property,
                              (AuxSTPredicateInstance, AuxSTClassInstance, AuxSTFunctionalTermInstance)):
                    # common code for all three types of properties:
                    new_instance = parent_property.clone()
                    new_instance.parent = my_properties  # add the new instance to the properties of the current class
                    # replace the var spec list of the new_instance
                    old_spec_list = AuxSymbolTable.get_child_by_outline(new_instance, AuxSTConstants.var_spec)
                    AuxSymbolTable.remove_node_recursively(old_spec_list)
                    new_spec_list = AuxSTVarSpecList()
                    new_spec_list.parent = new_instance
                    # we now replace the old contents with standard overrides calling the parent class' properties
                    # depending on the type of the property
                    if isinstance(parent_property, AuxSTPredicateInstance):
                        old_predicate = None
                        for child in new_instance.children:
                            if isinstance(child, (AuxSTPredicate, AuxSTIdentifier)):
                                old_predicate = child
                                break
                        AuxSymbolTable.remove_node_recursively(old_predicate)
                        new_predicate = AuxSTIdentifier(parent_property.isa())
                        new_predicate.id = parent_class.id + "." + parent_property.id
                        new_predicate.parent = new_instance
                        new_predicate.zfrom = parent_property.zfrom
                        new_predicate.zto = parent_property.zto
                        AuxSTArgs(parent_property.isa()).parent = new_predicate
                    elif isinstance(parent_property, AuxSTClassInstance):
                        stmt = AuxSTStatementAssign(parent_property.isa()).parent = new_spec_list
                        slf = AuxSTSelf(parent_property.isa()).parent = stmt
                        new_predicate = AuxSTIdentifier(parent_property.isa())
                        new_predicate.id = parent_class.id + "." + parent_property.id
                        new_predicate.parent = slf
                        new_predicate.zfrom = parent_property.zfrom
                        new_predicate.zto = parent_property.zto
                        AuxSTArgs(parent_property.isa()).parent = new_predicate
                    else:
                        stmt = AuxSTStatementReturn(parent_property.isa())
                        stmt.parent = new_spec_list
                        new_predicate = AuxSTIdentifier(parent_property.isa())
                        new_predicate.id = parent_class.id + "." + parent_property.id
                        new_predicate.parent = stmt
                        new_predicate.zfrom = parent_property.zfrom
                        new_predicate.zto = parent_property.zto
                        AuxSTArgs(parent_property.isa()).parent = new_predicate
                else:
                    raise AssertionError(str(type(parent_property)))

    def has_inherited_properties(self):
        return self._hip

    def evaluate(self, sem):
        if not self.is_sc_ready():
            sem.sc.add_reference(None, self.get_scope(), AuxReferenceType.semantical)
            self.set_sc_ready()
        if self.constant_value() is None:
            register = sem.eval_stack[-1]
            # the value of a class is a wrapper object with its type
            register.value = InbuiltValueAtRuntime(self, self.get_declared_type())
            self.set_constant_value(register)
            for child in self.children:
                if isinstance(child, AuxSTVarSpecList):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTConstructors):
                    EvaluateParams.evaluate_recursion(sem, child)
                elif isinstance(child, AuxSTProperties):
                    EvaluateParams.evaluate_recursion(sem, child)
                else:
                    raise NotImplementedError(child)
        sem.eval_stack.pop()
        sem.eval_stack.append(self.constant_value())

    def get_declared_type(self):
        """
        Override of the inherited method
        :return:
        """
        if self._declared_type is None:
            class_type = AuxSTType(self._i)
            class_type.id = self.id
            class_type.type_pattern = AuxBits.classBit
            self.set_declared_type(class_type)
        return self._declared_type

