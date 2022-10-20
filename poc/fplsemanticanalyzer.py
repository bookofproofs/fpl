import traceback
from anytree import AnyNode
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxOverrideHandler import AuxOverrideHandler
from poc.classes.AuxSelfContainment import AuxSelfContainment
from poc.SemCheckerIdentifiers import SemCheckerIdentifiers
from poc.fplerror import FplErrorManager, FplIdentifierAlreadyDeclared, FplMalformedNamespace
from poc.fplmessage import FplInterpreterSystemError


class SemanticAnalyser:

    def __init__(self, symbol_table_root: AnyNode, error_mgr: FplErrorManager):
        self.symbol_table_root = symbol_table_root
        self.error_mgr = error_mgr
        self.loaded_theories = AuxSymbolTable.get_theories(self.symbol_table_root)
        self.globals_node = AuxSymbolTable.get_child_by_outline(self.symbol_table_root, AuxSTConstants.globals)
        # self-containment
        self.sc = AuxSelfContainment()
        self.sem_checker_identifiers = SemCheckerIdentifiers(self)
        # a stack to evaluate recursively the semantics of the symbol table
        self.eval_stack = list()
        # a dictionary of all nodes by id (non-global identifier)
        self.theorem_like_statements = dict()  # all theorem like statements by id (non-global identifier)
        # In the following, we specify, which building blocks are allowed to have overrides
        # (i.e. the same identifiers, but different signatures).
        self.theorems = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.lemmas = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.propositions = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.corollaries = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.axioms = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.conjectures = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.classes = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.proofs = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.instance_classes = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.instance_functional_terms = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.instance_predicates = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.functional_terms = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        self.predicates = AuxOverrideHandler(AuxOverrideHandler.NOT_ALLOWED, self.error_mgr)
        # allowed ones:
        self.overridden_qualified_ids = AuxOverrideHandler(AuxOverrideHandler.ALLOWED, self.error_mgr)
        self.inference_rules = AuxOverrideHandler(AuxOverrideHandler.ALLOWED, self.error_mgr)
        self.constructors = AuxOverrideHandler(AuxOverrideHandler.ALLOWED, self.error_mgr)
        self.last_value = None  # this attributes stores the last value established during the evaluation process

    def semantic_analysis(self):
        """
        Semantic analysis
        :return:
        """
        if AuxISourceAnalyser.verbose:
            self._check_theories()
            self.sem_checker_identifiers.analyse()
            self.evaluate()
        else:
            # in non-verbose mode, we handle all exceptions 'user-friendly' as not to cause the main loop to halt
            try:
                self._check_theories()
                self.sem_checker_identifiers.analyse()
                self.evaluate()
            except Exception:  # noqa
                # add any exceptions during the semantic analysis into the regular error list
                self.error_mgr.add_error(
                    FplInterpreterSystemError(
                        traceback.format_exc().replace("Traceback (most recent call last):\n  ", "")))

    def _check_theories(self):
        for theory in self.loaded_theories:
            self.__check_namespace_identifiers(theory)
            self.__check_malformed_namespace(theory)

    def __check_namespace_identifiers(self, theory):
        """
        Check if all namespaces are listed only once in the the uses clause of each theory
        :return: None
        """
        duplicate_checker = dict()
        uses_node = AuxSymbolTable.get_child_by_outline(theory, AuxSTConstants.uses)
        for child in uses_node.children:
            if child.id not in duplicate_checker:
                duplicate_checker[child.id] = child
            else:
                self.error_mgr.add_error(
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
                self.error_mgr.add_error(FplMalformedNamespace(theory.namespace, theory.file_name))

    def evaluate(self):
        """
        The method will check all the global nodes if they can be evaluated consistently.
        :return: True, iff all global nodes could be evaluated consistently.
        """
        globals_node = AuxSymbolTable.get_child_by_outline(self.symbol_table_root, AuxSTConstants.globals)
        for child in globals_node.children:
            expected_type = child.reference.get_declared_type()
            # start recursive evaluation for each reference
            EvaluateParams.evaluate_recursion(self, child.reference,
                                              expected_type=expected_type,
                                              building_block=child.reference,
                                              instance_guid=child.reference.get_main_instance().id)
