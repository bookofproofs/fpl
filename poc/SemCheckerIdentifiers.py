from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplErrorManager
from poc.fplerror import FplIdentifierAlreadyDeclared
from poc.fplerror import FplUndeclaredVariable
from poc.fplerror import FplUnusedVariable
from poc.fplerror import FplMalformedGlobalId
from poc.fplerror import FplMisspelledConstructor
from poc.fplerror import FplMisspelledProperty
from poc.fplerror import FplIdentifierNotDeclared
from poc.fplerror import FplProofMissingTheoremLikeStatement
from poc.fplerror import FplCorollaryMissingTheoremLikeStatement
from poc.fplerror import FplProvedConjecture
from poc.fplerror import FplAmbiguousSignature
from poc.fplerror import FplForbiddenOverride
from poc.classes.AuxSTConstructor import AuxSTConstructor
from poc.classes.AuxSTSignature import AuxSTSignature
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTFunctionalTermInstance import AuxSTFunctionalTermInstance
from poc.classes.AuxSTPredicateInstance import AuxSTPredicateInstance
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTClassInstance import AuxSTClassInstance
from poc.classes.AuxSTDefinitionFunctionalTerm import AuxSTDefinitionFunctionalTerm
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate
from poc.classes.AuxSTLemma import AuxSTLemma
from poc.classes.AuxSTTheorem import AuxSTTheorem
from poc.classes.AuxSTProposition import AuxSTProposition
from poc.classes.AuxSTCorollary import AuxSTCorollary
from poc.classes.AuxSTRuleOfInference import AuxSTRuleOfInference
from poc.classes.AuxSTAxiom import AuxSTAxiom
from poc.classes.AuxSTConjecture import AuxSTConjecture
from poc.classes.AuxSTProof import AuxSTProof
from anytree import search
from poc.fplerror import FplMissingProof

"""
The OverrideHandler class provides
"""


class OverrideHandler:
    ALLOWED = True
    NOT_ALLOWED = False

    def __init__(self, mode: bool, error_mgr: FplErrorManager):
        self._mode = mode
        self._error_mgr = error_mgr
        self._dict = dict()

    def add(self, identifier, node):
        if self._mode == OverrideHandler.ALLOWED:
            if identifier not in self._dict:
                self._dict[identifier] = list()
            self._dict[identifier].append(node)
        else:
            if identifier not in self._dict:
                self._dict[identifier] = node
            else:
                # an error detected
                if node.reference.id == self._dict[identifier].reference.id:
                    # the case == of the same signatures would be a false pasitive
                    # for FplForbiddenOverride, because this kind of
                    # error is already detected by the FplAmbiguousSignature error
                    pass
                else:
                    self._error_mgr.add_error(FplForbiddenOverride(node, self._dict[identifier]))

    def get(self, identifier):
        return self._dict[identifier]

    def keys(self):
        return self._dict.keys()

    def dictionary(self):
        return self._dict


class SemCheckerIdentifiers:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        # a dictionary of all nodes by id (non-global identifier)
        self._signature_collection = dict()  # all nodes by signature
        self.theorem_like_statements = dict()  # all theorem like statements by id (non-global identifier)

        # In the following, we specify, which building blocks are allowed to have overrides
        # (i.e. the same identifiers, but different signatures).
        self.theorems = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.lemmas = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.propositions = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.corollaries = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.axioms = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.conjectures = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.types = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        self.proofs = OverrideHandler(OverrideHandler.NOT_ALLOWED, self.analyzer.error_mgr)
        # allowed ones:
        self.overridden_signatures = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.inference_rules = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.instance_classes = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.instance_functional_terms = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.instance_predicates = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.constructors = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.predicates = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)
        self.functional_terms = OverrideHandler(OverrideHandler.ALLOWED, self.analyzer.error_mgr)

    def analyse(self):
        """
        Check different semantics about FPL user-defined identifiers.
        Implementation Note: We use one loop for different checks per building blocks for performance reasons.
        :return: None
        """
        for child in self.analyzer.globals_node.children:
            identifier = child.id.split("[")[0]

            self.overridden_signatures.add(identifier, child)
            self._check_for_malformed_gid(identifier, child, child.theory)
            self._check_uniqueness_gid(child)
            self._check_uniqueness_signature(child)
        self._check_misspelled_references()
        self._check_override_consistency()
        self._check_referencing_identifiers()
        self._check_vars()

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
        :return: None
        """
        for var_node in used_vars:
            if var_node.id not in declared_vars:
                # the variable is undeclared if it was not found among the declared variables
                self.analyzer.error_mgr.add_error(FplUndeclaredVariable(var_node.zfrom, var_node.id, file_name))
            elif not declared_vars[var_node.id].has_in_scope(var_node.zfrom):
                # the variable is also undeclared if it was found among the declared variables
                # but is outside the scope of this variable declaration
                if isinstance(var_node.path[3], AuxSTProof) and not isinstance(declared_vars[var_node.id], AuxSTProof):
                    # unless it is a variable of a proof because in this case we have to
                    # extend the 'scope' of variables declared in the corresponding theorem-like statement
                    # to all proofs, in particular to this one
                    pass
                else:
                    self.analyzer.error_mgr.add_error(FplUndeclaredVariable(var_node.zfrom, var_node.id, file_name))

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
        # remove for this check all 'outer' declared variables
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

    def _check_for_malformed_gid(self, qualified_identifier, node, theory_node):
        """
        Checks if referenced identifiers do not conflict with chunks of names of the namespace.
        :param qualified_identifier: reference identifier (might be qualified like in 'ClassName.PropertyName')
        :param node: the global node with this identifier
        :param theory_node: theory node in which the identifier is declared
        :return: None
        """
        namespace = theory_node.namespace
        split_q_id = qualified_identifier.split(".")
        if len(split_q_id) == 2:
            if split_q_id[0] == split_q_id[1] and not isinstance(node.reference, AuxSTConstructor):
                # the property of a definition cannot be named the same as its main name
                parent = node.reference.parent.parent
                if isinstance(parent, AuxSTClass):
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 1, node.reference.zfrom,
                                              theory_node.file_name))
                elif isinstance(parent, AuxSTDefinitionPredicate):
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 2, node.reference.zfrom,
                                              theory_node.file_name))
                elif isinstance(parent, AuxSTDefinitionFunctionalTerm):
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 3, node.reference.zfrom,
                                              theory_node.file_name))
                else:
                    self.analyzer.error_mgr.add_error(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 4, node.reference.zfrom,
                                              theory_node.file_name))
        identifier = split_q_id[-1]
        if isinstance(node.reference, AuxSTConstructor):
            class_name = node.reference.parent.parent.id
            if identifier != class_name:
                # the constructor of a (class) definition has to be named the same as the class name
                self.analyzer.error_mgr.add_error(
                    FplMisspelledConstructor(class_name, identifier, node.reference.zfrom, theory_node.file_name))

        if identifier in namespace:
            namespace = namespace.replace(identifier, "")
            if namespace == "" or namespace.startswith(".") or namespace.endswith(".") or ".." in namespace:
                if isinstance(node.reference, AuxSTConstructor):
                    # ignore constructors since the class's name already does conflict too and generates a similar error
                    pass
                else:
                    self.analyzer.error_mgr.add_error(
                        FplMalformedGlobalId(identifier, theory_node.namespace, node.reference.zfrom,
                                             theory_node.file_name))

    def _check_uniqueness_gid(self, global_node):
        """
        Checks the uniqueness of fully qualified global identifiers. (If not, the user has used the same name of a
        building block across different namespaces.)
        :return: None, but after this method, gid_collection is complete and ready to be used for other analysis steps
        """
        if global_node.gid not in self.analyzer.gid_collection:
            self.analyzer.gid_collection[global_node.gid] = global_node
        else:
            node = global_node.reference
            theory_node = global_node.theory
            if node.outline != AuxSymbolTable.classDefaultConstructor:
                existing_node = self.analyzer.gid_collection[global_node.gid].reference
                existing_theory_node = self.analyzer.gid_collection[global_node.gid].theory
                self.analyzer.error_mgr.add_error(
                    FplIdentifierAlreadyDeclared(global_node.id, node.zfrom, theory_node.file_name, existing_node.zfrom,
                                                 existing_theory_node.file_name))

    def _check_uniqueness_signature(self, global_node):
        """
        Checks the uniqueness of signatures (If not, the user has duplicated a building block
        in the source code of different namespaces.) For instance, there are two theorems that can be referred to
        as "FundamentalTheorem", one located in the "Algebra", another located in the "Arithmetics" namespace.
        :param global_node: Some child node from the globals node of the symbol table.
        :return: None, but after this method, signature_collection is complete and ready to be used for other analysis steps
        """
        if global_node.id not in self._signature_collection:
            self._signature_collection[global_node.id] = global_node
        else:
            if global_node.theory.namespace != self._signature_collection[global_node.id].theory.namespace:
                # The id of the node should be also unique across different namespaces.
                node = global_node.reference
                theory_node = global_node.theory
                if node.outline != AuxSymbolTable.classDefaultConstructor:
                    existing_node = self._signature_collection[global_node.id].reference
                    existing_theory_node = self._signature_collection[global_node.id].theory
                    self.analyzer.error_mgr.add_error(
                        FplIdentifierAlreadyDeclared(global_node.id, node.zfrom, theory_node.file_name,
                                                     existing_node.zfrom,
                                                     existing_theory_node.file_name))

    def _check_misspelled_references(self):
        for theory_node in self.analyzer.loaded_theories:
            # by convention of the FPL syntax, all pascal-case type names are user-defined
            # collect them
            collect_type_references = search.findall(theory_node,
                                                     filter_=lambda node: isinstance(node, AuxSTType)
                                                                          and node.id[0].isupper())
            for type_node in collect_type_references:
                if type_node.id not in self.overridden_signatures.dictionary():
                    # the type is never declared
                    self.analyzer.error_mgr.add_error(
                        FplIdentifierNotDeclared(type_node.id, theory_node.file_name, type_node.zfrom))

            # by convention of the FPL syntax, all pascal-case reference names are user-defined
            # collect them
            collect_other_references = search.findall(theory_node,
                                                      filter_=lambda node: isinstance(node, AuxSTPredicateWithArgs)
                                                                           and node.id[0].isupper())
            for reference_node in collect_other_references:
                if reference_node.id not in self.overridden_signatures.dictionary():
                    # the reference is never declared
                    self.analyzer.error_mgr.add_error(
                        FplIdentifierNotDeclared(reference_node.id, theory_node.file_name, reference_node.zfrom))

    def _check_override_consistency(self):
        """
        Checks if, per identifier, all list elements have the same building block type.
        Only in this case, we can interpret them as overriding the same type of a building block.
        The different types will be distributed over different dictionaries of the object instance
        depending on the type of a building block so that we will be able to access them by that type directly
        in later steps of the semantical analysis.
        :return: None
        """
        for identifier in self.overridden_signatures.keys():
            # in this first loop, we check if there are same signatures with different types of blocks
            last_block = None
            for block in self.overridden_signatures.get(identifier):
                if last_block is None:
                    last_block = block
                else:
                    if last_block.reference.get_node_type_str() != block.reference.get_node_type_str() and \
                            last_block.reference.id == block.reference.id:
                        # in all other case with the same signature we have the FplAmbiguousSignature error
                        self.analyzer.error_mgr.add_error(FplAmbiguousSignature(block, last_block))

            # In the next loop, we dispatch the nodes and detect FplForbiddenOverride errors (if any)
            for global_node in self.overridden_signatures.get(identifier):
                reference = block.reference
                if isinstance(reference, AuxSTClass):
                    self.types.add(identifier, global_node)
                elif isinstance(reference, AuxSTConstructor):
                    self.constructors.add(identifier, global_node)
                elif isinstance(reference, AuxSTDefinitionFunctionalTerm):
                    self.functional_terms.add(identifier, global_node)
                elif isinstance(reference, AuxSTDefinitionPredicate):
                    self.predicates.add(identifier, global_node)
                elif isinstance(reference, AuxSTClassInstance):
                    self.instance_classes.add(identifier, global_node)
                elif isinstance(reference, AuxSTPredicateInstance):
                    self.instance_predicates.add(identifier, global_node)
                elif isinstance(reference, AuxSTFunctionalTermInstance):
                    self.instance_functional_terms.add(identifier, global_node)
                elif isinstance(reference, AuxSTProof):
                    self.proofs.add(identifier, global_node)
                elif isinstance(reference, AuxSTTheorem):
                    self.theorems.add(identifier, global_node)
                    self.theorem_like_statements[identifier] = global_node
                elif isinstance(reference, AuxSTProposition):
                    self.propositions.add(identifier, global_node)
                    self.theorem_like_statements[identifier] = global_node
                elif isinstance(reference, AuxSTLemma):
                    self.lemmas.add(identifier, global_node)
                    self.theorem_like_statements[identifier] = global_node
                elif isinstance(reference, AuxSTCorollary):
                    self.corollaries.add(identifier, global_node)
                    self.theorem_like_statements[identifier] = global_node
                elif isinstance(reference, AuxSTAxiom):
                    self.axioms.add(identifier, global_node)
                elif isinstance(reference, AuxSTRuleOfInference):
                    self.inference_rules.add(identifier, global_node)
                elif isinstance(reference, AuxSTConjecture):
                    self.conjectures.add(identifier, global_node)
                else:
                    raise NotImplementedError(type(reference))

    def _check_referencing_identifiers(self):
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
        for identifier in self.theorem_like_statements:
            s = identifier.split("$")
            referenced_identifier = "".join(s[0:-1])
            global_node = self.theorem_like_statements[identifier]
            reference = global_node.reference
            # check for FplCorollaryMissingTheoremLikeStatement error
            if isinstance(reference, AuxSTCorollary):
                if referenced_identifier not in self.theorem_like_statements:
                    self.analyzer.error_mgr.add_error(
                        FplCorollaryMissingTheoremLikeStatement(referenced_identifier, identifier, reference.zfrom,
                                                                self.theorem_like_statements[
                                                                    identifier].theory.file_name))
            # check for the FplMissingProof warning
            proof_found = False
            for proof_id in self.proofs.keys():
                if proof_id.startswith(identifier + "$"):
                    proof_found = True
            if not proof_found:
                self.analyzer.error_mgr.add_error(
                    FplMissingProof(identifier, reference.zfrom,
                                    self.theorem_like_statements[identifier].theory.file_name))

        for identifier in self.proofs.keys():
            # check for the FplProofMissingTheoremLikeStatement error
            s = identifier.split("$")
            referenced_identifier = "".join(s[0:-1])
            # syntactically, proofs cannot be overridden, thus there is only one per identifier
            proof_node = self.proofs.get(identifier).reference  # so we take this only one [0]
            if referenced_identifier not in self.theorem_like_statements:
                self.analyzer.error_mgr.add_error(
                    FplProofMissingTheoremLikeStatement(referenced_identifier, identifier, proof_node.zfrom,
                                                        self._signature_collection[identifier].theory.file_name))
            else:
                # Remember the proof's theorem-like statement once and for ever so we do not need to look for it anymore
                proof_node.set_referenced_theorem_like_stmt(
                    self.theorem_like_statements[referenced_identifier].reference)

            # Now, it is possible to initialize the declared and used variables in the proof properly, since we
            # (hopefully) know its theorem-like statement.
            # Hereby we check for unused variables and already declared variables
            proof_node.initialize_vars(self.proofs.get(identifier).theory.file_name, self.analyzer.error_mgr)

            # check for the FplProvedConjecture error
            if referenced_identifier in self.conjectures.keys():
                self.analyzer.error_mgr.add_error(
                    FplProvedConjecture(referenced_identifier, identifier, proof_node.zfrom,
                                        self.conjectures.get(referenced_identifier).theory.file_name))

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
