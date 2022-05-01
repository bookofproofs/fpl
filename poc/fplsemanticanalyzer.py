from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplIdentifierAlreadyDeclared
from poc.fplerror import FplMalformedNamespace
from poc.fplerror import FplUndeclaredVariable
from poc.fplerror import FplUnusedVariable
from poc.fplerror import FplIdentifierNotDeclared
from poc.fplerror import FplMalformedGlobalId
from poc.fplerror import FplMisspelledConstructor
from poc.fplerror import FplMisspelledProperty
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTDefinitionFunctionalTerm import AuxSTDefinitionFunctionalTerm
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate
from poc.classes.AuxSTLemma import AuxSTLemma
from poc.classes.AuxSTTheorem import AuxSTTheorem
from poc.classes.AuxSTProposition import AuxSTProposition
from poc.classes.AuxSTCorollary import AuxSTCorollary
from poc.classes.AuxSTRuleOfInference import AuxSTRuleOfInference
from poc.classes.AuxSTAxiom import AuxSTAxiom
from poc.classes.AuxSTConjecture import AuxSTConjecture
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxSTConstructor import AuxSTConstructor
from anytree import search


class SemanticAnalyser:

    def __init__(self, symbol_table_root: AnyNode, errors: list):
        self._symbol_table_root = symbol_table_root
        self._globals_node = None
        self._errors = errors
        self._loaded_theories = tuple()
        self._gid_collection = dict()
        self._signature_collection = dict()
        # in this dictionary we collect lists of nodes by the same referencee (identifier)
        self._references = dict()
        self._loaded_theories = AuxSymbolTable.get_theories(self._symbol_table_root)
        self._globals_node = AuxSymbolTable.get_child_by_outline(self._symbol_table_root, AuxSymbolTable.globals)

    def semantic_analysis(self):
        """
        Semantic analysis
        :return:
        """
        self._check_theories()
        self._check_identifiers()
        self._check_misspelled_references()

    def _check_theories(self):
        for theory in self._loaded_theories:
            self.__check_namespace_identifiers(theory)
            self.__check_malformed_namespace(theory)

    def __check_namespace_identifiers(self, theory):
        """
        Check if all namespaces are listed only once in the the uses clause of each theory
        :return: None
        """
        duplicate_checker = dict()
        uses_node = AuxSymbolTable.get_child_by_outline(theory, AuxSymbolTable.uses)
        for child in uses_node.children:
            if child.id not in duplicate_checker:
                duplicate_checker[child.id] = child
            else:
                self._errors.append(
                    FplIdentifierAlreadyDeclared(child.id, child.zfrom, theory.file_name,
                                                 duplicate_checker[child.id].zfrom,
                                                 theory.file_name))

    def __check_malformed_namespace(self, theory):
        """
        Check if each loaded namespace consists of different names separated by a dot
        :return: None
        """
        duplicate_checker = set()
        namespace_split = theory.namespace.split(".")
        for chunk in namespace_split:
            if chunk not in duplicate_checker:
                duplicate_checker.add(chunk)
            else:
                self._errors.append(FplMalformedNamespace(theory.namespace, theory.file_name))

    def _check_identifiers(self):
        """
        Check different semantics about FPL user-defined identifiers.
        Implementation Note: We use one loop for different checks per building blocks for performance reasons.
        :return: None
        """
        for child in self._globals_node.children:
            identifier = child.id.split("[")[0]
            if identifier not in self._references:
                self._references[identifier] = list()
                self._references[identifier].append(child)
            self.__check_undeclared_var_usages(child.reference.get_used_vars(), child.reference.get_declared_vars(),
                                               child.theory.file_name)
            self.__check_for_unused_vars(child.reference.get_used_vars(), child.reference.get_declared_vars(),
                                         child.theory.file_name)
            self.__check_for_malformed_gid(identifier, child, child.theory)
            self.__check_uniqueness_gid(child)
            self.__check_uniqueness_signature(child)

    def __check_undeclared_var_usages(self, used_vars: tuple, declared_vars: dict, file_name: str):
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
                self._errors.append(FplUndeclaredVariable(var_node.zfrom, var_node.id, file_name))
            elif not declared_vars[var_node.id].has_in_scope(var_node.zfrom):
                # the variable is also undeclared if it was found among the declared variables
                # but is outside the scope of this variable declaration
                self._errors.append(FplUndeclaredVariable(var_node.zfrom, var_node.id, file_name))

    def __check_for_unused_vars(self, used_vars: tuple, declared_vars: dict, file_name: str):
        """
        Checks if all declared variables are used in each building block, depending on their scope.
        :param used_vars: tuple of used vars of the building block
        :param declared_vars: dictionary of declared vars of the building block
        :param file_name: FPL file name in which the building block is declared.
        :return: None
        """
        for identifier in declared_vars:
            was_used = False
            for var_node in used_vars:
                if var_node.id == identifier:
                    was_used = True
                    break
            if not was_used:
                # the variable is not used
                self._errors.append(FplUnusedVariable(declared_vars[identifier].zfrom, identifier, file_name))

    def __check_for_malformed_gid(self, qualified_identifier, node, theory_node):
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
                    self._errors.append(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 1, node.reference.zfrom,
                                              theory_node.file_name))
                elif isinstance(parent, AuxSTDefinitionPredicate):
                    self._errors.append(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 2, node.reference.zfrom,
                                              theory_node.file_name))
                elif isinstance(parent, AuxSTDefinitionFunctionalTerm):
                    self._errors.append(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 3, node.reference.zfrom,
                                              theory_node.file_name))
                else:
                    self._errors.append(
                        FplMisspelledProperty(split_q_id[0], split_q_id[1], 4, node.reference.zfrom,
                                              theory_node.file_name))
        identifier = split_q_id[-1]
        if isinstance(node.reference, AuxSTConstructor):
            class_name = node.reference.parent.parent.id
            if identifier != class_name:
                # the constructor of a (class) definition has to be named the same as the class name
                self._errors.append(
                    FplMisspelledConstructor(class_name, identifier, node.reference.zfrom, theory_node.file_name))

        if identifier in namespace:
            namespace = namespace.replace(identifier, "")
            if namespace == "" or namespace.startswith(".") or namespace.endswith(".") or ".." in namespace:
                if isinstance(node.reference, AuxSTConstructor):
                    # ignore constructors since the class's name already does conflict too and generates a similar error
                    pass
                else:
                    self._errors.append(
                        FplMalformedGlobalId(identifier, theory_node.namespace, node.reference.zfrom,
                                             theory_node.file_name))

    def __check_uniqueness_gid(self, global_node):
        """
        Checks the uniqueness of fully qualified global identifiers. (If not, the user has used the same name of a
        building block across different namespaces.)
        :return: None
        """
        if global_node.gid not in self._gid_collection:
            self._gid_collection[global_node.gid] = global_node
        else:
            node = global_node.reference
            theory_node = global_node.theory
            if node.outline != AuxSymbolTable.classDefaultConstructor:
                existing_node = self._gid_collection[global_node.gid].reference
                existing_theory_node = self._gid_collection[global_node.gid].theory
                self._errors.append(
                    FplIdentifierAlreadyDeclared(global_node.id, node.zfrom, theory_node.file_name, existing_node.zfrom,
                                                 existing_theory_node.file_name))

    def __check_uniqueness_signature(self, global_node):
        """
        Checks the uniqueness of signatures (If not, the user has duplicated a building block
        in the source code of the same namespace.) For instance, there a two theorems that can be referred
        by the name "FundamentalTheorem", one in an Algebra namespace, another in an Arithmetics namespace.
        :param global_node: Some child node from the globals node of the symbol table.
        :return: None
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
                    self._errors.append(
                        FplIdentifierAlreadyDeclared(global_node.id, node.zfrom, theory_node.file_name,
                                                     existing_node.zfrom,
                                                     existing_theory_node.file_name))

    def _check_misspelled_references(self):
        for theory_node in self._loaded_theories:
            # by convention of the FPL syntax, all pascal-case type names are user-defined
            # collect them
            collect_type_references = search.findall(theory_node,
                                                     filter_=lambda node: isinstance(node, AuxSTType)
                                                                          and node.id[0].isupper())
            for type_node in collect_type_references:
                if type_node.id not in self._references:
                    # the type is never declared
                    self._errors.append(
                        FplIdentifierNotDeclared(type_node.id, theory_node.file_name, type_node.zfrom))

            # by convention of the FPL syntax, all pascal-case reference names are user-defined
            # collect them
            collect_other_references = search.findall(theory_node,
                                                      filter_=lambda node: isinstance(node, AuxSTPredicateWithArgs)
                                                                           and node.id[0].isupper())
            for reference_node in collect_other_references:
                if reference_node.id not in self._references:
                    # the reference is never declared
                    self._errors.append(
                        FplIdentifierNotDeclared(reference_node.id, theory_node.file_name, reference_node.zfrom))

    @staticmethod
    def is_type(reference):
        return isinstance(reference, (AuxSTClass, AuxSTDefinitionPredicate, AuxSTDefinitionFunctionalTerm))

    @staticmethod
    def is_theorem_like_statement(reference):
        return isinstance(reference, (AuxSTCorollary, AuxSTLemma, AuxSTProposition, AuxSTTheorem))

    @staticmethod
    def is_asserted(reference):
        return isinstance(reference, (AuxSTAxiom, AuxSTRuleOfInference))

    @staticmethod
    def is_conjecture(reference):
        return isinstance(reference, AuxSTConjecture)
