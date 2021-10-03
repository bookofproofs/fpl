from classes.AuxDeclaredVariable import AuxDeclaredVariable
from classes.AuxStringConcatenationRules import AuxStringConcatenationRules
from classes.AuxInterpretation import AuxInterpretation
from classes.VariableList import VariableList
from classes.GeneralType import GeneralType
from classes.AuxAstInfo import AuxAstInfo
from classes.Prettifier import Prettifier
from classes.SymbolTable import SymbolTable
from classes.AuxContext import AuxContext
from classes.AuxOutlines import AuxOutlines
from anytree import AnyNode


class FPLSemantics(object):
    errors = None
    warnings = None
    parse_list = None
    _prettifier = None
    _context = None
    _namespace_node = None
    switcher = None
    _theory_node = None
    _working_stack = None

    def __init__(self, root: AnyNode, theory_name: str, errors: list):
        self.errors = errors
        self.warnings = []
        self.parse_list = []
        self.ast_list = []
        self._prettifier = Prettifier()
        self._working_stack = []
        self._context = AuxContext()
        self._theory_node = SymbolTable.add_or_get_theory(root, theory_name)
        self._context.push_context(AuxOutlines.root)

        self.switcher = {
            "Alias": self.ignore_production,
            "alias": self.ignore_production,
            "AliasedId": self.concatenation_of_proceeding_string_rules,
            "All": self.default_interpretation,  # todo
            "all": self.default_interpretation,  # todo
            "Ampersand": self.default_interpretation,  # todo
            "AmpersandVariable": self.default_interpretation,  # todo
            "and": self.default_interpretation,  # todo
            "AnonymousDeclaration": self.default_interpretation,  # todo
            "AnonymousSignature": self.default_interpretation,  # todo
            "ArgumentIdentifier": self.default_interpretation,  # todo
            "ArgumentInference": self.default_interpretation,  # todo
            "ass": self.default_interpretation,  # todo
            "assert": self.default_interpretation,  # todo
            "AssertionStatement": self.default_interpretation,  # todo
            "Assignee": self.default_interpretation,  # todo
            "AssignmentStatement": self.default_interpretation,  # todo
            "assume": self.default_interpretation,  # todo
            "AssumedPredicate": self.default_interpretation,  # todo
            "AssumeHeader": self.default_interpretation,  # todo
            "At": self.string_interpretation,
            "AtList": self.concatenation_of_proceeding_string_rules,
            "ax": self.default_interpretation,  # todo
            "Axiom": self.default_interpretation,  # todo
            "axiom": self.ignore_production,
            "AxiomBlock": self.default_interpretation,  # todo
            "AxiomHeader": self.start_context_signature_axiom,
            "BuildingBlock": self.ignore_production,
            "BuildingBlockList": self.ignore_production,
            "CallModifier": self.concatenation_of_proceeding_string_rules,
            "case": self.default_interpretation,  # todo
            "CaseStatement": self.default_interpretation,  # todo
            "cl": self.ignore_production,
            "class": self.ignore_production,
            "ClassHeader": self.start_context_class_declaration,
            "ClassInstance": self.default_interpretation,  # todo
            "ClosedOrOpenRange": self.default_interpretation,  # todo
            "Colon": self.default_interpretation,  # todo
            "ColonEqual": self.default_interpretation,  # todo
            "Comma": self.default_interpretation,  # todo
            "Comment": self.default_interpretation,  # todo
            "CompoundPredicate": self.default_interpretation,  # todo
            "con": self.default_interpretation,  # todo
            "conclusion": self.default_interpretation,  # todo
            "ConclusionBlock": self.default_interpretation,  # todo
            "ConclusionHeader": self.default_interpretation,  # todo
            "ConditionFollowedByResult": self.default_interpretation,  # todo
            "ConditionFollowedByResultList": self.default_interpretation,  # todo
            "conj": self.default_interpretation,  # todo
            "conjecture": self.default_interpretation,  # todo
            "Conjunction": self.default_interpretation,  # todo
            "Constructor": self.default_interpretation,  # todo
            "Coord": self.default_interpretation,  # todo
            "CoordInSignature": self.default_interpretation,  # todo
            "CoordList": self.default_interpretation,  # todo
            "cor": self.default_interpretation,  # todo
            "corollary": self.default_interpretation,  # todo
            "CW": self.ignore_production,
            "DefaultResult": self.default_interpretation,  # todo
            "Definition": self.ignore_production,
            "DefinitionClass": self.default_interpretation,  # todo
            "DefinitionContent": self.default_interpretation,  # todo
            "DefinitionContentList": self.default_interpretation,  # todo
            "DefinitionFunctionalTerm": self.default_interpretation,  # todo
            "DefinitionPredicate": self.default_interpretation,  # todo
            "DefinitionProperty": self.default_interpretation,  # todo
            "DerivedPredicate": self.default_interpretation,  # todo
            "Digit": self.string_interpretation,
            "Disjunction": self.default_interpretation,  # todo
            "Dollar": self.default_interpretation,  # todo
            "Dot": self.string_interpretation,
            "EBNFBar": self.default_interpretation,  # todo
            "EBNFFactor": self.default_interpretation,  # todo
            "EBNFString": self.default_interpretation,  # todo
            "EBNFTerm": self.default_interpretation,  # todo
            "EBNFTransl": self.default_interpretation,  # todo
            "else": self.default_interpretation,  # todo
            "end": self.default_interpretation,  # todo
            "Entity": self.default_interpretation,  # todo
            "EntityWithCoord": self.default_interpretation,  # todo
            "Equivalence": self.default_interpretation,  # todo
            "ex": self.default_interpretation,  # todo
            "ExclamationMark": self.string_interpretation,
            "ExclusiveOr": self.default_interpretation,  # todo
            "Exists": self.default_interpretation,  # todo
            "ExistsHeader": self.default_interpretation,  # todo
            "ExistsTimesN": self.default_interpretation,  # todo
            "ext": self.string_interpretation,
            "extDigit": self.default_interpretation,  # todo
            "ExtensionBlock": self.default_interpretation,  # todo
            "ExtensionContent": self.default_interpretation,  # todo
            "ExtensionHeader": self.default_interpretation,  # todo
            "ExtensionTail": self.default_interpretation,  # todo
            "false": self.default_interpretation,  # todo
            "func": self.ignore_production,
            "function": self.ignore_production,
            "FunctionalTermDefinitionBlock": self.default_interpretation,  # todo
            "FunctionalTermHeader": self.start_context_functional_term_declaration,
            "FunctionalTermInstance": self.default_interpretation,  # todo
            "FunctionalTermSignature": self.default_interpretation,  # todo
            "GeneralType": self.general_type_interpretation,
            "Identifier": self.default_interpretation,  # todo
            "IdStartsWithCap": self.string_interpretation,
            "IdStartsWithSmallCase": self.string_interpretation,
            "iif": self.default_interpretation,  # todo
            "impl": self.default_interpretation,  # todo
            "Implication": self.default_interpretation,  # todo
            "ind": self.default_interpretation,  # todo
            "index": self.default_interpretation,  # todo
            "IndexHeader": self.default_interpretation,  # todo
            "IndexValue": self.default_interpretation,  # todo
            "inf": self.ignore_production,
            "inference": self.ignore_production,
            "InferenceHeader": self.start_context_inference,
            "InstanceBlock": self.default_interpretation,  # todo
            "is": self.default_interpretation,  # todo
            "IsOperator": self.default_interpretation,  # todo
            "IW": self.ignore_production,
            "Justification": self.default_interpretation,  # todo
            "KeysOfVariadicVariable": self.default_interpretation,  # todo
            "LanguageCode": self.default_interpretation,  # todo
            "LeftBound": self.concatenation_of_proceeding_string_rules,
            "LeftBrace": self.start_block,
            "LeftBracket": self.string_interpretation,
            "LeftParen": self.default_interpretation,  # todo
            "lem": self.default_interpretation,  # todo
            "lemma": self.default_interpretation,  # todo
            "loc": self.default_interpretation,  # todo
            "Localization": self.default_interpretation,  # todo
            "localization": self.default_interpretation,  # todo
            "LocalizationBlock": self.default_interpretation,  # todo
            "LocalizationHeader": self.default_interpretation,  # todo
            "LocalizationList": self.default_interpretation,  # todo
            "LongComment": self.default_interpretation,  # todo
            "LongTemplateHeader": self.default_interpretation,  # todo
            "loop": self.default_interpretation,  # todo
            "LoopStatement": self.default_interpretation,  # todo
            "mand": self.default_interpretation,  # todo
            "mandatory": self.default_interpretation,  # todo
            "Mapping": self.handle_mapping,
            "NamedVariableDeclaration": self.default_interpretation,  # todo
            "Namespace": self.ignore_production,
            "NamespaceBlock": self.ignore_production,
            "NamespaceIdentifier": self.handle_namespace_identifier,
            "NamespaceModifier": self.handle_namespace_modifier,
            "Negation": self.default_interpretation,  # todo
            "not": self.default_interpretation,  # todo
            "obj": self.default_interpretation,  # todo
            "object": self.default_interpretation,  # todo
            "ObjectDefinitionBlock": self.default_interpretation,  # todo
            "ObjectHeader": self.default_interpretation,  # todo
            "opt": self.default_interpretation,  # todo
            "optional": self.default_interpretation,  # todo
            "or": self.default_interpretation,  # todo
            "ParamList": self.default_interpretation,  # todo
            "ParamTuple": self.default_interpretation,  # todo
            "ParenthesisedPredicate": self.default_interpretation,  # todo
            "Plus": self.string_interpretation,
            "post": self.default_interpretation,  # todo
            "postulate": self.ignore_production,
            "pre": self.default_interpretation,  # todo
            "pred": self.ignore_production,
            "predicate": self.ignore_production,
            "Predicate": self.default_interpretation,  # todo
            "PredicateDefinitionBlock": self.default_interpretation,  # todo
            "PredicateHeader": self.handle_predicate_header,
            "PredicateIdentifier": self.handle_predicate_identifier,
            "PredicateList": self.default_interpretation,  # todo
            "PredicateWithArguments": self.default_interpretation,  # todo
            "premise": self.default_interpretation,  # todo
            "PremiseBlock": self.default_interpretation,  # todo
            "PremiseConclusionBlock": self.default_interpretation,  # todo
            "PremiseHeader": self.default_interpretation,  # todo
            "PremiseOrOtherPredicate": self.default_interpretation,  # todo
            "prf": self.default_interpretation,  # todo
            "PrimePredicate": self.default_interpretation,  # todo
            "Proof": self.default_interpretation,  # todo
            "proof": self.default_interpretation,  # todo
            "ProofArgument": self.default_interpretation,  # todo
            "ProofArgumentList": self.default_interpretation,  # todo
            "ProofBlock": self.default_interpretation,  # todo
            "ProofHeadHeader": self.default_interpretation,  # todo
            "ProofIdentifier": self.default_interpretation,  # todo
            "prop": self.default_interpretation,  # todo
            "Property": self.default_interpretation,  # todo
            "PropertyHeader": self.default_interpretation,  # todo
            "PropertyList": self.default_interpretation,  # todo
            "proposition": self.default_interpretation,  # todo
            "py": self.default_interpretation,  # todo
            "PythonDelegate": self.default_interpretation,  # todo
            "PythonIdentifier": self.default_interpretation,  # todo
            "qed": self.default_interpretation,  # todo
            "QualifiedIdentifier": self.default_interpretation,  # todo
            "Range": self.default_interpretation,  # todo
            "range": self.default_interpretation,  # todo
            "RangeInSignature": self.default_interpretation,  # todo
            "RangeOrLoopBody": self.default_interpretation,  # todo
            "RangeStatement": self.default_interpretation,  # todo
            "ReferencedResultIdentifier": self.default_interpretation,  # todo
            "ret": self.default_interpretation,  # todo
            "return": self.default_interpretation,  # todo
            "ReturnHeader": self.default_interpretation,  # todo
            "ReturnStatement": self.default_interpretation,  # todo
            "rev": self.default_interpretation,  # todo
            "Revoke": self.default_interpretation,  # todo
            "revoke": self.default_interpretation,  # todo
            "RevokeHeader": self.default_interpretation,  # todo
            "RightBound": self.concatenation_of_proceeding_string_rules,
            "RightBrace": self.stop_block,
            "RightBracket": self.string_interpretation,
            "RightParen": self.default_interpretation,  # todo
            "RuleOfInference": self.ignore_production,
            "RuleOfInferenceList": self.default_interpretation,  # todo
            "RulesOfInferenceBlock": self.ignore_production,
            "self": self.default_interpretation,  # todo
            "SemiColon": self.default_interpretation,  # todo
            "Signature": self.default_interpretation,  # todo
            "Slash": self.default_interpretation,  # todo
            "Star": self.string_interpretation,
            "Statement": self.default_interpretation,  # todo
            "StatementList": self.default_interpretation,  # todo
            "SW": self.ignore_production,
            "template": self.default_interpretation,  # todo
            "TemplateHeader": self.default_interpretation,  # todo
            "th": self.default_interpretation,  # todo
            "theorem": self.default_interpretation,  # todo
            "TheoremLikeStatementOrConjecture": self.default_interpretation,  # todo
            "TheoremLikeStatementOrConjectureHeader": self.default_interpretation,  # todo
            "theory": self.ignore_production,
            "TheoryBlock": self.ignore_production,
            "TheoryHeader": self.start_context_theory,
            "thm": self.default_interpretation,  # todo
            "Tilde": self.default_interpretation,  # todo
            "To": self.default_interpretation,  # todo
            "tpl": self.default_interpretation,  # todo
            "Translation": self.default_interpretation,  # todo
            "TranslationList": self.default_interpretation,  # todo
            "trivial": self.default_interpretation,  # todo
            "true": self.default_interpretation,  # todo
            "TupleOfTypes": self.default_interpretation,  # todo
            "Type": self.default_interpretation,  # todo
            "TypeOrTupleOfTypes": self.default_interpretation,  # todo
            "TypeWithCoord": self.default_interpretation,  # todo
            "undef": self.default_interpretation,  # todo
            "undefined": self.default_interpretation,  # todo
            "UndefinedHeader": self.default_interpretation,  # todo
            "uses": self.start_context_uses,
            "UsesClause": self.stop_context_uses,
            "Variable": self.concatenation_of_proceeding_string_rules,
            "VariableDeclaration": self.default_interpretation,  # todo
            "VariableDeclarationList": self.default_interpretation,  # todo
            "VariableList": self.variable_list_interpretation,
            "VariableSpecification": self.default_interpretation,  # todo
            "VariableSpecificationList": self.default_interpretation,  # todo
            "VariableType": self.default_interpretation,  # todo
            "VDash": self.default_interpretation,  # todo
            "WildcardTheoryNamespace": self.ignore_production,
            "WildcardTheoryNamespaceList": self.ignore_production,
            "XId": self.concatenation_of_proceeding_string_rules,
            "xor": self.default_interpretation,  # todo
        }

    @staticmethod
    def _debug():
        return False

    def get_debug_parsing_info(self, parsing_info: AuxInterpretation):
        if self._debug():
            return str(parsing_info)
        else:
            return None

    def get_minified(self):
        return self._prettifier.get_minified()

    def get_prettified(self):
        return self._prettifier.get_prettified()

    def _default(self, ast):
        """
        If there’s no method matching the rule’s name, TatSu will invoke this method.
        :param ast: ast
        :return: ast
        """
        return ast

    def _minify(self, ast_info: AuxAstInfo):
        """
        Builds up a minified representation of the parsed fpl file during the parsing process
        :param ast_info: info about the parsed item
        :return: None
        """
        self._prettifier.minify(ast_info)

    def _postproc(self, context, ast):
        """
        This TatSu method will be called after each rule is processed.
        In contrast to _default, this method will receive the current parsing context as a parameter:
        :param context: parsing context
        :param ast: ast
        :return: ast
        """

        ast_info = AuxAstInfo(context)
        self.ast_list.append(ast_info)
        # minify
        self._minify(ast_info)
        parsing_info = AuxInterpretation(ast_info, self.errors)
        interpretation = self.interpret_switcher(parsing_info)
        if interpretation is not None:
            # append all interpretations that returned something else than None
            self.parse_list.append(interpretation)
        return ast

    def interpret_switcher(self, parsing_info: AuxInterpretation):
        rule = parsing_info.rule_name()
        func = self.switcher.get(rule, lambda: "Invalid rule")
        # call the function depending on the rule in the switcher and modify its interpretation and returns its value
        return func(parsing_info)

    """
    All interpretation delegates
    """

    @staticmethod
    def default_interpretation(parsing_info: AuxInterpretation):
        """
        Copies the parsing context of TatSu into an interpretation
        :param parsing_info: the interpretation for a rule
        :return: modified parsing_info
        """
        cst = parsing_info.get_cst()
        if type(cst) is str:
            parsing_info.set_interpretation(cst)
        else:
            parsing_info.set_interpretation("NotImplemented " + str(cst))
        return parsing_info

    @staticmethod
    def ignore_production(parsing_info: AuxInterpretation):
        return None

    @staticmethod
    def string_interpretation(parsing_info: AuxInterpretation):
        cst = parsing_info.get_cst()
        if type(cst) is str:
            parsing_info.set_interpretation(cst)
        else:
            raise AssertionError("String interpretation expected, received " + str(cst))
        return parsing_info

    def handle_namespace_identifier(self, parsing_info: AuxInterpretation):
        parsing_info = self.concatenation_of_proceeding_string_rules(parsing_info)
        # NamespaceIdentifer can occur in the following contexts:
        if self._context.is_parsing_context([AuxOutlines.root]):
            # tag the namespace to the theory node
            self._theory_node.namespace = parsing_info.get_interpretation()
        elif self._context.is_parsing_context([AuxOutlines.root, AuxOutlines.block, AuxOutlines.uses]):
            # as a name of namespaces used in the current namespace
            # In this case, remember the node of the used namespace added to the symbol table
            # because we will need it again when handling the NamespaceModifier rule (see last_element_of_list_or_tuple)
            self._working_stack.append(
                SymbolTable.add_usage_to_theory(self._theory_node, parsing_info))

        else:
            if self._debug():
                print(
                    "########### Unhandled context in handle_predicate_identifier " + str(
                        self._context.get_context()) + " " + str(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def handle_predicate_identifier(self, parsing_info: AuxInterpretation):
        parsing_info = self.concatenation_of_proceeding_string_rules(parsing_info)
        # PredicateIdentifier can occur in following different  contexts:
        if self._context.is_parsing_context([AuxOutlines.inferenceRules, AuxOutlines.block]):
            # as a name of an inference rule
            SymbolTable.add_inference_rule_to_theory(self._theory_node, parsing_info)
            self._context.push_context(AuxOutlines.inferenceRule, self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.theory, AuxOutlines.block, AuxOutlines.axiom]):
            # as a name of an axiom that is global
            SymbolTable.add_axiom_to_theory(self._theory_node, parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.classDeclaration]):
            # as a name of a class definition
            # we put the class name on the working stack because we have yet to update it with its type
            # (see handle_general_type)
            self._working_stack.append(SymbolTable.add_class_to_theory(self._theory_node, parsing_info))
            self._context.push_context(AuxOutlines.classType, self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.classType]):
            # as a name of a class type, do nothing since handle_general_type handles this
            pass
        elif self._context.is_parsing_context([AuxOutlines.theory, AuxOutlines.block, AuxOutlines.predicate]):
            # as a name of a predicate definition that is global
            SymbolTable.add_predicate_to_theory(self._theory_node, parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.theory, AuxOutlines.block, AuxOutlines.functionalTerm]):
            # as a name of a functional term definition that is global
            # we put the functional term name on the working stack because we have yet to update
            # it with its image (see handle_general_type)
            self._working_stack.append(SymbolTable.add_functional_term_to_theory(self._theory_node, parsing_info))
            self._context.push_context(AuxOutlines.functionalTermImage, self.get_debug_parsing_info(parsing_info))
        else:
            if self._debug():
                print(
                    "########### Unhandled context in handle_predicate_identifier " + str(
                        self._context.get_context()) + " " + str(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def start_context_uses(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.uses, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def stop_context_uses(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.uses], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def start_context_inference(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.inferenceRules, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def start_context_theory(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.theory, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def start_context_signature_axiom(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.axiom, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def handle_predicate_header(self, parsing_info: AuxInterpretation):
        # a predicate header can occur in the following contexts:
        if self._context.is_parsing_context([AuxOutlines.theory, AuxOutlines.block]):
            # inside a theory (top level) - in this case, we have a new global predicate definition
            self._context.push_context(AuxOutlines.predicate, self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.inferenceRules, AuxOutlines.block]):
            # inside an inference (top level) - in this case, we have a new global inference rule definition
            self._context.push_context(AuxOutlines.inferenceRule, self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.axiom, AuxOutlines.block]):
            # predicate type declaration inside an axiom, todo
            pass
        elif self._context.is_parsing_context([AuxOutlines.classDeclaration, AuxOutlines.block]):
            # predicate declaration or usage inside an class block, todo
            pass
        else:
            if self._debug():
                print("########### Unhandled context in handle_predicate_header" + str(
                    self._context.get_context()) + " " + str(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def start_block(self, parsing_info: AuxInterpretation):
        # starts a new block
        self._context.push_context(AuxOutlines.block, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def stop_block(self, parsing_info: AuxInterpretation):
        # stops a block
        self._context.pop_context([AuxOutlines.block], self.get_debug_parsing_info(parsing_info))
        # garbage collector, remove any additional infos depending on the context
        if self._context.is_parsing_context([AuxOutlines.root]):
            # root? => do nothing since this is a global interpreter context built up in the caller of fplsemantics
            pass
        elif self._context.is_parsing_context([AuxOutlines.theory]):
            # end of the theory block
            self._context.pop_context([AuxOutlines.theory], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.inferenceRules]):
            # end of inference block
            self._context.pop_context([AuxOutlines.inferenceRules], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.inferenceRule]):
            # end of the inference rule block
            self._context.pop_context([AuxOutlines.inferenceRule],
                                      self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.axiom]):
            self._context.pop_context([AuxOutlines.axiom], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.predicate]):
            self._context.pop_context([AuxOutlines.predicate], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.classDeclaration]):
            self._context.pop_context([AuxOutlines.classDeclaration], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.functionalTerm]):
            self._context.pop_context([AuxOutlines.functionalTerm], self.get_debug_parsing_info(parsing_info))
        else:
            if self._debug():
                print("########### Unhandled context in stop_block" + str(self._context.get_context()) + " " + str(
                    parsing_info))

    def start_context_class_declaration(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.classDeclaration, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def start_context_functional_term_declaration(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.functionalTerm, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def concatenation_of_proceeding_string_rules(self, parsing_info: AuxInterpretation):
        """
        Removes all rules from parsing_list that can be ignored because the interpretation of
        the current rule is a string concatenation of the interpretations of to be ignored rules
        :param parsing_info: the interpretation for a rule
        :return: modified parsing_info
        """
        # concatenate the interpretations of the proceeding rules and remove them from self.parse_list
        aux_ignore = AuxStringConcatenationRules(self.parse_list, parsing_info.rule_name())
        # the (string) concatenated interpretation of the proceeding rules replaces the interpretation of this rule
        parsing_info.set_interpretation(aux_ignore.inter())
        # replace the complex cst (e.g. lists and dictionaries) by None to save memory. We won't need it any more.
        parsing_info.clear_cst()
        return parsing_info

    def handle_namespace_modifier(self, parsing_info: AuxInterpretation):
        if type(parsing_info.get_cst()) is list or tuple:
            used_namespace_node = self._working_stack.pop()
            used_namespace_node.modifier = parsing_info.get_cst()[-1]  # last element of the list or tuple
            # remove from parse list rules proceeding Alias (if any)
            self.clean_up_parse_list(["IdStartsWithCap", "Star", "Comma"])
        return None  # do not append to parse_list, we are done with this

    def clean_up_parse_list(self, removable_rules: list):
        something_found = True
        while len(self.parse_list) > 0 and something_found:
            something_found = False  # prevent an endless while loop after the for loop
            for rule in removable_rules:
                if len(self.parse_list) > 0:
                    if self.parse_list[-1].rule_name() == rule:
                        self.parse_list.pop()
                        something_found = True

    def variable_list_interpretation(self, parsing_info: AuxInterpretation):
        """
        Simplifies the parse_list by removing all rules that contribute to a VariableList
        :param parsing_info: the interpretation for a rule
        :return: VariableList object
        """
        # consume all proceeding variables into a VariableList and remove them from self.parse_list
        variable_list = VariableList(self.parse_list, parsing_info)
        return variable_list

    def general_type_interpretation(self, parsing_info: AuxInterpretation):
        """
        Simplifies the parse_list by removing all rules that contribute to a GeneralType
        :param parsing_info: the interpretation for a rule
        :return: GeneralType object
        """
        # consume all proceeding variables into a GeneralType and remove them from self.parse_list
        general_type = GeneralType(self.parse_list, parsing_info)
        # remove from parse list rules proceeding Alias (if any)
        self.clean_up_parse_list(["Colon", "obj", "ObjectHeader"])
        if self._context.is_parsing_context([AuxOutlines.classType]):
            # in the context of a class declaration, we have to update the type of the class
            class_node = self._working_stack.pop()
            class_node.type = general_type.get_type()
            # we clear the context of classType
            self._context.pop_context([AuxOutlines.classType], self.get_debug_parsing_info(parsing_info))
            return None  # this general type is handled completely
        else:
            return general_type

    def handle_mapping(self, parsing_info: AuxInterpretation):
        if self._context.is_parsing_context([AuxOutlines.functionalTermImage]):
            # in the context of a functional term declaration, we have to update the image of the functional term
            functional_term_node = self._working_stack.pop()
            functional_term_node.image = parsing_info.get_cst()[-1]
            # clear the context of functionalTermImage
            self._context.pop_context([AuxOutlines.functionalTermImage], self.get_debug_parsing_info(parsing_info))
            return None  # this general type is handled completely
