from anytree import AnyNode, PreOrderIter
from poc.fplerror import FplAmbiguousSignature
from poc.fplerror import FplCorollaryMissingTheoremLikeStatement
from poc.fplerror import FplForbiddenOverride
from poc.fplerror import FplIdentifierAlreadyDeclared
from poc.fplerror import FplIdentifierNotDeclared
from poc.fplerror import FplMalformedGlobalId
from poc.fplerror import FplMisspelledConstructor
from poc.fplerror import FplMisspelledProperty
from poc.fplerror import FplProofMissingTheoremLikeStatement
from poc.fplerror import FplProvedConjecture
from poc.fplerror import FplTypeNotAllowed
from poc.fplerror import FplVariableBound
from poc.fplerror import FplUndeclaredVariable
from poc.fplerror import FplUnusedVariable
from poc.classes.AuxBits import AuxBits
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltIndex, InbuiltObject, InbuiltPredicate, \
    InbuiltFunctionalTerm, InbuiltExtension, InbuiltGeneric
from poc.classes.AuxOverrideHandler import AuxOverrideHandler
from poc.classes.AuxSTAxiom import AuxSTAxiom
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTClassInstance import AuxSTClassInstance
from poc.classes.AuxSTConjecture import AuxSTConjecture
from poc.classes.AuxSTConstructor import AuxSTConstructor
from poc.classes.AuxSTCorollary import AuxSTCorollary
from poc.classes.AuxSTDefinitionFunctionalTerm import AuxSTDefinitionFunctionalTerm
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate
from poc.classes.AuxSTFunctionalTermInstance import AuxSTFunctionalTermInstance
from poc.classes.AuxSTLemma import AuxSTLemma
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTPredicateInstance import AuxSTPredicateInstance
from poc.classes.AuxSTProposition import AuxSTProposition
from poc.classes.AuxSTProof import AuxSTProof
from poc.classes.AuxSTRuleOfInference import AuxSTRuleOfInference
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTTheorem import AuxSTTheorem
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import search
from poc.fplerror import FplMissingProof


class SemCheckerIdentifiers:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        # a stack to evaluate recursively the semantics of the symbol table
        self.eval_stack = list()
        # append root (dummy) params for later recursion
        self.eval_stack.append(EvaluateParams())
        # a dictionary of all nodes by id (non-global identifier)
        self.theorem_like_statements = dict()  # all theorem like statements by id (non-global identifier)

        # In the following, we specify, which building blocks are allowed to have overrides
        # (i.e. the same identifiers, but different signatures).
        self.theorems = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.lemmas = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.propositions = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.corollaries = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.axioms = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.conjectures = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.classes = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.proofs = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.instance_classes = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.instance_functional_terms = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.instance_predicates = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.functional_terms = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.predicates = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        # allowed ones:
        self.overridden_qualified_ids = AuxOverrideHandler(AuxOverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.inference_rules = AuxOverrideHandler(AuxOverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.constructors = AuxOverrideHandler(AuxOverrideHandler.ALLOWED, self.analyzer.error_mgr)

    def analyse(self):
        """
        Check different semantics about FPL user-defined identifiers.
        Implementation Note: We use one loop for different checks per building blocks for performance reasons.
        :return: None
        """
        for child in self.analyzer.globals_node.children:
            qualified_identifier = child.get_qualified_id()
            self.overridden_qualified_ids.add(qualified_identifier, child, None)
            self._check_for_malformed_gid(qualified_identifier, child)
            self._check_uniqueness_identifiers(qualified_identifier, child)
        self._check_override_consistency()
        self._check_referencing_proof_corollary()
        self._check_misspelled_types()
        self._check_vars()
        self.evaluate()

    def _check_vars(self):
        for child in self.analyzer.globals_node.children:
            declared_vars = child.reference.get_declared_vars()
            used_vars = child.reference.get_used_vars()
            self._check_undeclared_var_usages(used_vars, declared_vars, child.theory.file_name)
            self._check_for_unused_vars(child.reference, child.theory.file_name, declared_vars)
            self._check_bound_vars(child.reference, used_vars, declared_vars)

    def _check_undeclared_var_usages(self, used_vars: tuple, declared_vars: dict, file_name: str):
        """
        Checks if all used variables are declared in each building block, depending on their scope.
        :param used_vars: tuple of used vars of the building block
        :param declared_vars: dictionary of declared vars of the building block
        :param file_name: FPL file name in which the building block is declared.
        :return: None, but each used variable stores internally a pointer to the symbol table node containing its type

        """
        for var_node in used_vars:
            if var_node.id not in declared_vars:
                # the variable is undeclared if it was not found among the declared variables
                self.analyzer.error_mgr.add_error(FplUndeclaredVariable(var_node.zfrom, var_node.id, file_name))
                # set the type fo the variable to InbuiltUndefined
                var_node.set_declared_type(InbuiltUndefined())
            elif not declared_vars[var_node.id].has_in_scope(var_node.zfrom):
                # the variable is also undeclared if it was found among the declared variables
                # but is outside the scope of this variable declaration
                if isinstance(var_node.path[3], AuxSTProof) and not isinstance(declared_vars[var_node.id], AuxSTProof):
                    # unless it is a variable of a proof because in this case we have to
                    # extend the 'scope' of variables declared in the corresponding theorem-like statement
                    # to all proofs, in particular to this one
                    # set the declared type to the type node in the symbol table
                    var_node.set_declared_type(declared_vars[var_node.id].children[0])
                else:
                    self.analyzer.error_mgr.add_error(FplUndeclaredVariable(var_node.zfrom, var_node.id, file_name))
            else:
                var_node.set_declared_type(declared_vars[var_node.id].children[0])

    def _check_for_unused_vars(self, node: AnyNode, file_name: str, declared_vars):
        """
        Checks if all declared variables are used in each building block, depending on their scope.
        :param node: node declared in the FPL code (object instance of the symbol table node)
        :param file_name: FPL file name in which the building block is declared.
        :param: dictionary of declared vars of the building block
        :return: None
        """
        # dictionary of used vars of the building block (values are lists of all occurrences)
        used_vars_dict = SemCheckerIdentifiers.__get_all_used_vars(node)
        # To avoid false positives, we have to remove for this check all 'outer' declared variables
        # We have to do it, because e.g. those variables declared in the class do not necessarily have to be used
        # in the scope of each property or each constructor of the class.
        only_inner_declared = dict()
        # in the same loop we identify the vars that are bound in the signature

        for identifier in declared_vars:
            if declared_vars[identifier].parent.parent == node:
                only_inner_declared[identifier] = declared_vars[identifier]

        for identifier in only_inner_declared:
            if identifier not in used_vars_dict:
                # Even if the variable was not used, this might make sense semantically,
                # If the variable was declared in the signature and there is an intrinsic definition.
                # So we check for this additional condition
                if not SemCheckerIdentifiers.__unused_variable_declared_in_signature_of_intrinsic(node,
                                                                                                  declared_vars[
                                                                                                      identifier]):
                    self.analyzer.error_mgr.add_error(
                        FplUnusedVariable(declared_vars[identifier].zfrom, identifier, file_name))

                # initialize the main instance with the variable and type that has empty occurrences
                empty_occurrences = list()
                node.add_var_to_main_instance(identifier, empty_occurrences,
                                              only_inner_declared[identifier].children[0])
            else:
                # add the type and all variable occurrences of the variable to the main instance of the node
                # (the main instance will be a blueprint for creating new instances of the same node)
                node.add_var_to_main_instance(identifier, used_vars_dict[identifier],
                                              only_inner_declared[identifier].children[0])

    def _check_bound_vars(self, node, used_vars, declared_vars):
        """
        :param used_vars: tuple of used vars of the building block
        :param declared_vars: dictionary of declared vars of the building block
        :return: None
        """
        # Calculate a set of variables that are bound in the signature
        vars_bound_in_signature = dict()
        for var_id in declared_vars:
            var_declaration = declared_vars[var_id]
            for path_node in var_declaration.path:
                if isinstance(path_node, AuxSTSignature):
                    if var_id not in vars_bound_in_signature:
                        vars_bound_in_signature[var_id] = declared_vars[var_id]
                    break

        # First, mark all variable usages inside the block as 'bound', if they were declared
        # in the signature of the block
        for var_node in used_vars:
            if var_node.id in vars_bound_in_signature:
                # set the variable as bound if was bound in the signature
                var_node.set_is_bound()

        # Now, try to mark recursively also all variables that are bound in quantors (for all / exists)
        self._bound_vars_in_quantors_rek(node, vars_bound_in_signature)

    def _bound_vars_in_quantors_rek(self, current_node, vars_bound_so_far):
        """
        Prevents variables of being bound more than once in nested constructs inside the symbol table.
        :param current_node: a node in the symbol table that bounds some further variables
        :param vars_bound_so_far: dictionary of (key,value) pairs, key= var id, value = node bounding the variable,
        that lists all variables that were already bound in the outer scope of current_node
        :return:
        """
        # gather the quantors sub nodes of the node in pre-order
        quantor_nodes = list(n for n in PreOrderIter(current_node, filter_=
        lambda n1: isinstance(n1, AuxSTPredicate) and n1.outline in [AuxSymbolTable.predicate_all,
                                                                     AuxSymbolTable.predicate_exists]))

        for quantor in quantor_nodes:
            for var_id in quantor.bound_vars:
                if var_id in vars_bound_so_far:
                    self.analyzer.error_mgr.add_error(FplVariableBound(var_id, quantor, vars_bound_so_far[var_id]))
                else:
                    # remember the quantor as a node bounding the variable
                    vars_bound_so_far[var_id] = quantor
                    # todo: mark all occurrences of the variable inside the quantor block as bound
                    # todo: identify the case that the bound variable is never used inside the block
                    pass
            pass

    def _check_for_malformed_gid(self, qualified_identifier, node):
        """
        Checks if referenced identifiers do not conflict with chunks of names of the namespace.
        :param qualified_identifier: reference identifier (might be qualified like in 'ClassName.PropertyName')
        :param node: the global node with this identifier
        :param theory_node: theory node in which the identifier is declared
        :return: None
        """
        namespace = node.theory.namespace
        split_q_id = qualified_identifier.split(".")
        if len(split_q_id) == 2:
            if split_q_id[0] == split_q_id[1] and not isinstance(node.reference, AuxSTConstructor):
                # the property of a definition cannot be named the same as its main name
                parent = node.reference.parent.parent
                if isinstance(parent, AuxSTClass):
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], node))
                elif isinstance(parent, AuxSTDefinitionPredicate):
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], node))
                elif isinstance(parent, AuxSTDefinitionFunctionalTerm):
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], node))
                else:
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], node))
        identifier = split_q_id[-1]
        if isinstance(node.reference, AuxSTConstructor):
            class_name = node.reference.parent.parent.id
            if identifier != class_name:
                # the constructor of a (class) definition has to be named the same as the class name
                self.analyzer.error_mgr.add_error(FplMisspelledConstructor(class_name, identifier, node))

        if identifier in namespace:
            namespace = namespace.replace(identifier, "")
            if namespace == "" or namespace.startswith(".") or namespace.endswith(".") or ".." in namespace:
                if isinstance(node.reference, AuxSTConstructor):
                    # ignore constructors since the class's name already does conflict too and generates a similar error
                    pass
                else:
                    self.analyzer.error_mgr.add_error(FplMalformedGlobalId(identifier, node))

    def _check_uniqueness_identifiers(self, qualified_identifier: str, global_node):
        """
        Checks for different identifier-related errors of building blocks have the same qualified identifiers.
        :param global_node: Some child node from the globals node of the symbol table.
        :param global_node: Some child node from the globals node of the symbol table.
        :return: None, but after this method, gid_collection is complete and ready to be used for other analysis steps
        """
        block_list = self.overridden_qualified_ids.get(qualified_identifier)
        if len(block_list) > 1:
            # only if there is more than one building block with the same qualified identifier, errors might occur
            unique_gids = dict()
            for block in block_list:
                if block.gid not in unique_gids:
                    unique_gids[block.gid] = block
                    self._dispatch(qualified_identifier, block, None)
                else:
                    # We have detected two blocks with same qualified_identifier in the same namespace.
                    # In this case, we have to check if this an allowed override.
                    if unique_gids[block.gid].reference.get_node_type_str() != block.reference.get_node_type_str():
                        # In case we have two blocks with different types, we trigger an FplAmbiguousSignature error
                        # unless in case of a allowed class/constructor pair
                        if not (isinstance(unique_gids[block.gid].reference, AuxSTConstructor) and
                                isinstance(block.reference, AuxSTClass) or
                                isinstance(unique_gids[block.gid].reference, AuxSTClass) and
                                isinstance(block.reference, AuxSTConstructor)):
                            self.analyzer.error_mgr.add_error(
                                FplAmbiguousSignature(block, unique_gids[block.gid])
                            )
                    elif unique_gids[block.gid].reference.id == block.reference.id and \
                            not (isinstance(block.reference, AuxSTConstructor) and
                                 isinstance(unique_gids[block.gid].reference, AuxSTConstructor)):
                        # If the types are the same and even the signature is the same, we have a duplicate declaration
                        if block.reference.outline != AuxSymbolTable.classDefaultConstructor:
                            self.analyzer.error_mgr.add_error(
                                FplIdentifierAlreadyDeclared(block.reference.id,
                                                             block.reference.zfrom,
                                                             block.theory.file_name,
                                                             unique_gids[block.gid].reference.zfrom,
                                                             unique_gids[block.gid].theory.file_name))
                    else:
                        self._dispatch(qualified_identifier, block, unique_gids[block.gid])
        else:
            self._dispatch(qualified_identifier, block_list[0], None)

    def _check_misspelled_types(self):
        """
        All AuxSTType nodes across all theories in the symbol table will be set to some internal representation,
        even those that have undefined identifiers will be set to an internal representation of Undefined.
        :return:
        """
        for theory_node in self.analyzer.loaded_theories:
            # by convention of the FPL syntax, all pascal-case type names are user-defined
            # collect them
            collect_type_references = search.findall(theory_node, filter_=lambda node: isinstance(node, AuxSTType))
            for type_node in collect_type_references:
                qualified_identifier = type_node.get_qualified_id()
                if type_node.id[0].isupper():  # if the identifier starts with a Capital, we have a user-defined type
                    if qualified_identifier in self.classes.dictionary():
                        type_node.set_repr(self.classes.get(qualified_identifier))
                    elif qualified_identifier in self.predicates.dictionary():
                        type_node.set_repr(self.predicates.get(qualified_identifier))
                    elif qualified_identifier in self.functional_terms.dictionary():
                        type_node.set_repr(self.functional_terms.get(qualified_identifier))
                    elif qualified_identifier in self.overridden_qualified_ids.dictionary():
                        # any other found declared block is semantically not an allowed type,
                        # we trigger the
                        self.analyzer.error_mgr.add_error(
                            FplTypeNotAllowed(self.overridden_qualified_ids.get(qualified_identifier)[0],
                                              type_node.zfrom,
                                              theory_node.file_name)
                        )
                        type_node.set_repr(InbuiltUndefined())
                    else:
                        self.analyzer.error_mgr.add_error(
                            FplIdentifierNotDeclared(qualified_identifier, theory_node.file_name, type_node.zfrom)
                        )
                        type_node.set_repr(InbuiltUndefined())
                elif AuxBits.is_index(type_node.type_pattern):
                    type_node.set_repr(InbuiltIndex())
                elif AuxBits.is_predicate(type_node.type_pattern):
                    type_node.set_repr(InbuiltPredicate())
                elif AuxBits.is_functional_term(type_node.type_pattern):
                    type_node.set_repr(InbuiltFunctionalTerm())
                elif AuxBits.is_generic(type_node.type_pattern):
                    type_node.set_repr(InbuiltGeneric(type_node.id))
                elif AuxBits.is_inbuilt_object(type_node.type_pattern):
                    type_node.set_repr(InbuiltObject())
                elif AuxBits.is_extension(type_node.type_pattern):
                    type_node.set_repr(InbuiltExtension(type_node.id))
                else:
                    raise NotImplementedError("type_pattern " + str(self.type_pattern))

    def _check_override_consistency(self):
        """
        Checks if, per identifier, all list elements have the same building block type.
        Only in this case, we can interpret them as overriding the same type of a building block.
        The different types will be distributed over different dictionaries of the object instance
        depending on the type of a building block so that we will be able to access them by that type directly
        in later steps of the semantical analysis.
        :return: None
        """
        for identifier in self.overridden_qualified_ids.keys():
            # in this first loop, we check if there are same signatures with different types of blocks
            last_block = None
            for block in self.overridden_qualified_ids.get(identifier):
                if last_block is None:
                    last_block = block
                else:
                    if last_block.reference.get_node_type_str() != block.reference.get_node_type_str():
                        if last_block.reference.id == block.reference.id:
                            # Since we have unequal building block types with the same signature,
                            # we trigger the FplAmbiguousSignature error
                            self.analyzer.error_mgr.add_error(FplAmbiguousSignature(block, last_block))
                        elif not (isinstance(last_block.reference, AuxSTClass) and
                                  isinstance(block.reference, AuxSTConstructor) or
                                  isinstance(last_block.reference, AuxSTConstructor) and
                                  isinstance(block.reference, AuxSTClass)):
                            # Since we have unequal building block types the same identifier,
                            # we trigger the FplForbiddenOverride error, unless in case of constructors of classes
                            # which by default have a different signature but the same identifier as the class.
                            self.analyzer.error_mgr.add_error(FplForbiddenOverride(block, last_block))
                    else:
                        if last_block.reference.id != block.reference.id and \
                                isinstance(block.reference,
                                           (AuxSTConjecture, AuxSTClass, AuxSTProof, AuxSTTheorem, AuxSTProposition,
                                            AuxSTLemma,
                                            AuxSTCorollary, AuxSTAxiom)):
                            # Since we have equal building block types with different signatures,
                            # we trigger the FplForbiddenOverride error,
                            # if the type is one of the unallowed override types
                            self.analyzer.error_mgr.add_error(FplForbiddenOverride(block, last_block))

    def _dispatch(self, qualified_identifier: str, block, possible_duplicate):
        # we now dispatch the collected nodes
        reference = block.reference
        if isinstance(reference, AuxSTClass):
            self.classes.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTConstructor):
            self.constructors.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTDefinitionFunctionalTerm):
            self.functional_terms.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTDefinitionPredicate):
            reference.set_declared_type(InbuiltPredicate())
            self.predicates.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTClassInstance):
            self.instance_classes.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTPredicateInstance):
            self.instance_predicates.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTFunctionalTermInstance):
            self.instance_functional_terms.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTProof):
            self.proofs.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTTheorem):
            self.theorems.add(qualified_identifier, block, possible_duplicate)
            self.theorem_like_statements[qualified_identifier] = block
        elif isinstance(reference, AuxSTProposition):
            self.propositions.add(qualified_identifier, block, possible_duplicate)
            self.theorem_like_statements[qualified_identifier] = block
        elif isinstance(reference, AuxSTLemma):
            self.lemmas.add(qualified_identifier, block, possible_duplicate)
            self.theorem_like_statements[qualified_identifier] = block
        elif isinstance(reference, AuxSTCorollary):
            self.corollaries.add(qualified_identifier, block, possible_duplicate)
            self.theorem_like_statements[qualified_identifier] = block
        elif isinstance(reference, AuxSTAxiom):
            self.axioms.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTRuleOfInference):
            self.inference_rules.add(qualified_identifier, block, possible_duplicate)
        elif isinstance(reference, AuxSTConjecture):
            self.conjectures.add(qualified_identifier, block, possible_duplicate)
        else:
            raise NotImplementedError(type(reference))

    def _check_referencing_proof_corollary(self):
        """
        Checks all global nodes whose ids end with a DollarDigitList grammar rule production (e.g. $1$3)
        Semantically, those nodes can only be proofs or corollaries of some theorem-like statements.
        We have to check if there is a corresponding:
        a) theorem-like statement for a given corollary -> FplCorollaryMissingTheoremLikeStatement
        b) theorem-like statement for a given proof -> FplProofMissingTheoremLikeStatement
        c) proof for a given theorem-like statement -> FplMissingProof
        d) proof for a statement formulated as a conjecture -> FplProvedConjecture
        :return: None, updates the error list
        """
        for qualified_identifier in self.theorem_like_statements:
            s = qualified_identifier.split("$")
            referenced_identifier = "".join(s[0:-1])
            global_node = self.theorem_like_statements[qualified_identifier]
            reference = global_node.reference
            # check for FplCorollaryMissingTheoremLikeStatement error
            if isinstance(reference, AuxSTCorollary):
                if referenced_identifier not in self.theorem_like_statements:
                    self.analyzer.error_mgr.add_error(
                        FplCorollaryMissingTheoremLikeStatement(referenced_identifier,
                                                                self.theorem_like_statements[qualified_identifier]))
            # check for the FplMissingProof warning
            proof_found = False
            for proof_id in self.proofs.keys():
                if proof_id.startswith(qualified_identifier + "$"):
                    proof_found = True
            if not proof_found:
                self.analyzer.error_mgr.add_error(FplMissingProof(global_node))

        for qualified_identifier in self.proofs.keys():
            # check for the FplProofMissingTheoremLikeStatement error
            s = qualified_identifier.split("$")
            referenced_identifier = "".join(s[0:-1])
            # syntactically, proofs cannot be overridden, thus there is only one per identifier
            global_proof_node = self.proofs.get(qualified_identifier)[0]  # so we take this only one [0]
            proof_node = global_proof_node.reference
            if referenced_identifier not in self.theorem_like_statements:
                self.analyzer.error_mgr.add_error(
                    FplProofMissingTheoremLikeStatement(referenced_identifier, global_proof_node))
            else:
                # Remember the proof's theorem-like statement once and for ever so we do not need to look for it anymore
                proof_node.set_referenced_theorem_like_stmt(
                    self.theorem_like_statements[referenced_identifier].reference)

            # Now, it is possible to initialize the declared and used variables in the proof properly, since we
            # (hopefully) know its theorem-like statement.
            # Hereby we check for unused variables and already declared variables
            proof_node.initialize_vars(self.proofs.get(qualified_identifier)[0].theory.file_name,
                                       self.analyzer.error_mgr)

            # check for the FplProvedConjecture error
            if referenced_identifier in self.conjectures.keys():
                self.analyzer.error_mgr.add_error(
                    FplProvedConjecture(global_proof_node, self.conjectures.get(referenced_identifier)[0])
                )

    @staticmethod
    def __gather_used_vars(gather_used_set: dict, node: AnyNode):
        # tuple of used vars of the building block
        used_vars = node.get_used_vars()
        for var_node in used_vars:
            if var_node.id not in gather_used_set:
                gather_used_set[var_node.id] = list()
            else:
                gather_used_set[var_node.id].append(var_node)

    @staticmethod
    def __get_all_used_vars(node: AnyNode):
        gather_used_dict = dict()
        SemCheckerIdentifiers.__gather_used_vars(gather_used_dict, node)
        if isinstance(node, AuxSTClass):
            # for classes, enrich also all variables used in constructors
            constructors = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.classConstructors)
            for child in constructors.children:
                SemCheckerIdentifiers.__gather_used_vars(gather_used_dict, child)
            # ... and properties
            properties = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.properties)
            for child in properties.children:
                SemCheckerIdentifiers.__gather_used_vars(gather_used_dict, child)
        elif isinstance(node, (AuxSTDefinitionPredicate, AuxSTDefinitionFunctionalTerm)):
            # for functional term definitions or predicate definitions, enrich also all variables used in properties
            properties = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.properties)
            for child in properties.children:
                SemCheckerIdentifiers.__gather_used_vars(gather_used_dict, child)
        return gather_used_dict

    @staticmethod
    def __unused_variable_declared_in_signature_of_intrinsic(node: AnyNode, var_decl):
        if isinstance(var_decl.parent, AuxSTSignature):
            if var_decl.parent.parent == node:
                if isinstance(node, AuxSTDefinitionFunctionalTerm) or isinstance(node, AuxSTFunctionalTermInstance):
                    definition = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.var_spec)
                    # The functional term's definition was intrinsic if its var specification subnode is empty
                    return len(definition.children) == 0
                elif isinstance(node, AuxSTDefinitionPredicate) or isinstance(node, AuxSTPredicateInstance):
                    # The predicate's definition was intrinsic if it has an
                    found_intrinsic_definition = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.intrinsic)
                    return found_intrinsic_definition is not None and \
                           isinstance(found_intrinsic_definition, AuxSTPredicate) and \
                           found_intrinsic_definition.parent == node
            elif var_decl.parent.parent == node.parent.parent:
                # if the variable was declared in the signature of the parent definition of a property node
                # ignore that the variable not used in the body of the property since it is not semantically required.
                return True
        return False

    def evaluate(self):
        """
        The method will check all the global nodes if they can be evaluated consistently.
        :return: True, iff all global nodes could be evaluated consistently.
        """
        globals_node = AuxSymbolTable.get_child_by_outline(self.analyzer.symbol_table_root, AuxSymbolTable.globals)
        for child in globals_node.children:
            EvaluateParams.evaluate_recursion(self, child.reference, child.reference.get_declared_type())
