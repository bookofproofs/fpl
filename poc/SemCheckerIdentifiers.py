from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
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
from poc.fplerror import FplUndeclaredVariable
from poc.fplerror import FplUnusedVariable
from poc.fplerror import FplWrongArguments
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltType
from poc.classes.AuxOverrideHandler import AuxOverrideHandler
from poc.classes.AuxSTAxiom import AuxSTAxiom
from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTClassInstance import AuxSTClassInstance
from poc.classes.AuxSTConjecture import AuxSTConjecture
from poc.classes.AuxSTConstructor import AuxSTConstructor
from poc.classes.AuxSTCorollary import AuxSTCorollary
from poc.classes.AuxSTDefinitionFunctionalTerm import AuxSTDefinitionFunctionalTerm
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate
from poc.classes.AuxSTFunctionalTermInstance import AuxSTFunctionalTermInstance
from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSTLemma import AuxSTLemma
from poc.classes.AuxSTLocalization import AuxSTLocalization
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTPredicateInstance import AuxSTPredicateInstance
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxSTProposition import AuxSTProposition
from poc.classes.AuxSTProof import AuxSTProof
from poc.classes.AuxSTQualified import AuxSTQualified
from poc.classes.AuxSTRuleOfInference import AuxSTRuleOfInference
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxSTTheorem import AuxSTTheorem
from poc.classes.AuxSTTheory import AuxSTTheory
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSTVariable import AuxSTVariable
from anytree import search
from poc.fplerror import FplMissingProof


class SemCheckerIdentifiers:
    def __init__(self, analyzer):
        self.analyzer = analyzer
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
        self.check_signatures()

    def _check_vars(self):
        for child in self.analyzer.globals_node.children:
            self._check_undeclared_var_usages(child.reference.get_used_vars(), child.reference.get_declared_vars(),
                                              child.theory.file_name)
            self._check_for_unused_vars(child.reference, child.theory.file_name)

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

    def _check_for_unused_vars(self, node: AnyNode, file_name: str):
        """
        Checks if all declared variables are used in each building block, depending on their scope.
        :param node: node declared in the FPL code (object instance of the symbol table node)
        :param file_name: FPL file name in which the building block is declared.
        :return: None
        """
        # tuple of used vars of the building block
        used_vars = SemCheckerIdentifiers.__get_all_used_vars(node)
        # dictionary of declared vars of the building block
        declared_vars = node.get_declared_vars()
        # To avoid false positives, we have to remove for this check all 'outer' declared variables
        # We have to do it, because e.g. those variables declared in the class do not necessarily have to be used
        # in the scope of each property or each constructor of the class.
        only_inner_declared = dict()
        for identifier in declared_vars:
            if declared_vars[identifier].parent.parent == node:
                only_inner_declared[identifier] = declared_vars[identifier]

        for identifier in only_inner_declared:
            if identifier not in used_vars:
                # Even if the variable was not used, this might make sense semantically,
                # If the variable was declared in the signature and there is an intrinsic definition.
                # So we check for this additional condition
                if not SemCheckerIdentifiers.__unused_variable_declared_in_signature_of_intrinsic(node,
                                                                                                  declared_vars[
                                                                                                      identifier]):
                    self.analyzer.error_mgr.add_error(
                        FplUnusedVariable(declared_vars[identifier].zfrom, identifier, file_name))

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
                type_node.set_type_node(self, theory_node.file_name)

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
    def __gather_used_vars(gather_used_set: set, node: AnyNode):
        # tuple of used vars of the building block
        used_vars = node.get_used_vars()
        for var_node in used_vars:
            if var_node.id not in gather_used_set:
                gather_used_set.add(var_node.id)

    @staticmethod
    def __get_all_used_vars(node: AnyNode):
        gather_used_set = set()
        SemCheckerIdentifiers.__gather_used_vars(gather_used_set, node)
        if isinstance(node, AuxSTClass):
            # for classes, enrich also all variables used in constructors
            constructors = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.classConstructors)
            for child in constructors.children:
                SemCheckerIdentifiers.__gather_used_vars(gather_used_set, child)
            # ... and properties
            properties = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.properties)
            for child in properties.children:
                SemCheckerIdentifiers.__gather_used_vars(gather_used_set, child)
        elif isinstance(node, (AuxSTDefinitionPredicate, AuxSTDefinitionFunctionalTerm)):
            # for functional term definitions or predicate definitions, enrich also all variables used in properties
            properties = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.properties)
            for child in properties.children:
                SemCheckerIdentifiers.__gather_used_vars(gather_used_set, child)
        return gather_used_set

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

    def check_signatures(self):
        """
        The method will check if the arguments in predicate_with_args match a given signature
        :return:
        """
        collect_preds_with_args = search.findall(self.analyzer.symbol_table_root,
                                                 filter_=lambda node: isinstance(node, AuxSTPredicateWithArgs) and
                                                                      not isinstance(node.parent, AuxSTLocalization))
        for pred_with_args in collect_preds_with_args:
            self._determine_caller_signature_rek(pred_with_args)

    def _determine_caller_signature_rek(self, predicate_with_args: AuxSTPredicateWithArgs):
        if predicate_with_args.type_signature_correct() is None:
            if predicate_with_args.id[0].isupper():
                base_identifier = predicate_with_args.get_qualified_id()
            else:
                base_identifier = predicate_with_args.get_declared_type().get_qualified_id()

            if isinstance(predicate_with_args.parent, AuxSTQualified):
                parent_identifier = self.__resolve_parent_identifier(predicate_with_args.parent)
            else:
                parent_identifier = ""

            if parent_identifier != "":
                qualified_identifier = parent_identifier + "." + base_identifier
            else:
                qualified_identifier = base_identifier

            if predicate_with_args.id[0].isupper():
                if qualified_identifier not in self.overridden_qualified_ids.dictionary():
                    # the reference of the predicate_with_args is never declared
                    self.analyzer.error_mgr.add_error(
                        FplIdentifierNotDeclared(qualified_identifier,
                                                 predicate_with_args.path[1].file_name,
                                                 predicate_with_args.zfrom))
                    predicate_with_args.reference = InbuiltUndefined()
                    predicate_with_args.set_type_signature_correctness(False)
                else:
                    self.__match_override_depending_on_arguments(predicate_with_args,
                                                                 self.overridden_qualified_ids.get(
                                                                     qualified_identifier))
            elif predicate_with_args.outline == AuxSymbolTable.var:
                self.__match_override_depending_on_arguments(predicate_with_args,
                                                             [predicate_with_args.get_declared_type().get_type_node()])
            else:
                raise NotImplementedError()

    def __match_override_depending_on_arguments(self, predicate_with_args: AuxSTPredicateWithArgs,
                                                expected_overrides: list):
        if isinstance(expected_overrides[0], InbuiltType):
            predicate_with_args.reference = expected_overrides[0]
        else:
            predicate_with_args.reference = expected_overrides[0].reference
        args = AuxSymbolTable.get_child_by_outline(predicate_with_args, AuxSymbolTable.arg_list)
        arg_types = list()
        for argument_node in args.children:
            if isinstance(argument_node, AuxSTPredicateWithArgs):
                # recursive call of for a new argument being itself a predicate with arguments
                self._determine_caller_signature_rek(argument_node)
                arg_types.append(argument_node.get_type_signature())
            elif isinstance(argument_node, AuxSTVariable):
                arg_types.append(argument_node.get_declared_type().get_type_signature())
            elif isinstance(argument_node, AuxSTSelf):
                self.__calculate_declared_type_of_self(argument_node)
                arg_types.append(argument_node.get_declared_type().get_type_signature())
            elif isinstance(argument_node, AuxSTPredicate):
                arg_types.append(argument_node.get_type_signature())
            elif isinstance(argument_node, AuxSTStatement):
                arg_types.append(AuxSymbolTable.undefined)
            else:
                raise NotImplementedError(str(type(argument_node)))
        calc_signature = SemCheckerIdentifiers.__calc_signature_from_args(predicate_with_args, arg_types)
        correct = calc_signature == predicate_with_args.reference.id
        predicate_with_args.set_type_signature_correctness(correct)
        if not correct:
            self.analyzer.error_mgr.add_error(FplWrongArguments(calc_signature, predicate_with_args))

    @staticmethod
    def __calc_signature_from_args(predicate_with_args: AuxSTPredicateWithArgs, arg_types: list):
        ret = list()
        running_type = ""
        type_counter = 0
        for current_type in arg_types:
            if running_type != current_type:
                if running_type != "":
                    ret.append(str(type_counter) + ":" + running_type)
                type_counter = 1
                running_type = current_type
            else:
                type_counter += 1
        if type_counter == 1 and len(ret) == 0:
            ret.append(running_type)
        return predicate_with_args.reference.get_qualified_id() + "[" + ",".join(ret) + "]"

    def __calculate_declared_type_of_self(self, self_instance):
        test_node = self_instance
        maximum_reached = False
        at = 0
        while at <= self_instance.number_ats and not maximum_reached:
            test_node = test_node.parent
            if isinstance(test_node, (AuxSTInstance, AuxSTConstructor, AuxSTBlockWithSignature, AuxSTClass)):
                at += 1
            if isinstance(test_node.parent, AuxSTTheory):
                maximum_reached = True
        declared_type = None
        if at > self_instance.number_ats and not maximum_reached:
            # the test_node points to the intended node referenced by 'self'
            # also remember the node in the this qualified identifier
            declared_type = test_node

        if declared_type is None:
            declared_type = InbuiltUndefined()
        self_instance.set_declared_type(declared_type)

    def __resolve_parent_identifier(self, qualified_instance: AuxSTQualified):
        parent = qualified_instance.parent
        if isinstance(parent, AuxSTVariable):
            return parent.get_declared_type().get_qualified_id()
        elif isinstance(parent, AuxSTSelf):
            self.__calculate_declared_type_of_self(parent)
            return parent.get_declared_type().get_qualified_id()
        elif isinstance(parent, AuxSTPredicateWithArgs):
            if parent.type_signature_correct() is None:
                self._determine_caller_signature_rek(parent)
            return parent.get_qualified_id()
        else:
            raise NotImplementedError(str(type(parent)))
