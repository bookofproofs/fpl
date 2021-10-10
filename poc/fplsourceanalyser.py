from classes.AuxDeclaredVariable import AuxDeclaredVariable
from classes.AuxStringConcatenationRules import AuxStringConcatenationRules
from classes.AuxInterpretation import AuxInterpretation
from classes.VariableList import VariableList
from classes.GeneralType import GeneralType
from classes.Type import Type
from classes.AuxAstInfo import AuxAstInfo
from classes.Prettifier import Prettifier
from classes.SymbolTable import SymbolTable
from classes.AuxContext import AuxContext
from classes.AuxOutlines import AuxOutlines
from anytree import AnyNode
import fplerror


class FPLSourceAnalyser(object):
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
            "All": self.all_quantor_stop,
            "all": self.all_quantor_start,
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
            "ax": self.ignore_production,
            "Axiom": self.axiom_stop,
            "axiom": self.ignore_production,
            "AxiomBlock": self.default_interpretation,  # todo
            "AxiomHeader": self.axiom_start,
            "BuildingBlock": self.ignore_production,
            "BuildingBlockList": self.ignore_production,
            "CallModifier": self.concatenation_of_proceeding_string_rules,
            "case": self.default_interpretation,  # todo
            "CaseStatement": self.default_interpretation,  # todo
            "cl": self.ignore_production,
            "class": self.ignore_production,
            "ClassHeader": self.class_start,
            "ClassInstance": self.class_instance_declaration_stop,
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
            "conj": self.ignore_production,
            "conjecture": self.ignore_production,
            "Conjunction": self.default_interpretation,  # todo
            "Constructor": self.constructor_stop,
            "Coord": self.default_interpretation,  # todo
            "CoordInSignature": self.default_interpretation,  # todo
            "CoordList": self.default_interpretation,  # todo
            "cor": self.ignore_production,
            "corollary": self.ignore_production,
            "CW": self.ignore_production,
            "DefaultResult": self.default_interpretation,  # todo
            "Definition": self.ignore_production,
            "DefinitionClass": self.class_stop,
            "DefinitionContent": self.default_interpretation,  # todo
            "DefinitionContentList": self.default_interpretation,  # todo
            "DefinitionFunctionalTerm": self.functional_term_stop,
            "DefinitionPredicate": self.predicate_declaration_stop,
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
            "ex": self.ex_quantor_start,
            "ExclamationMark": self.string_interpretation,
            "ExclusiveOr": self.default_interpretation,  # todo
            "Exists": self.ex_quantor_stop,
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
            "FunctionalTermHeader": self.functional_term_start,
            "FunctionalTermInstance": self.functional_term_stop,
            "FunctionalTermSignature": self.default_interpretation,  # todo
            "GeneralType": self.general_type_dispatcher,
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
            "InferenceHeader": self.inference_block_start,
            "InstanceBlock": self.default_interpretation,  # todo
            "is": self.is_operator_start,
            "IsOperator": self.is_operator_stop,
            "IW": self.ignore_production,
            "Justification": self.default_interpretation,  # todo
            "KeysOfVariadicVariable": self.default_interpretation,  # todo
            "LanguageCode": self.default_interpretation,  # todo
            "LeftBound": self.concatenation_of_proceeding_string_rules,
            "LeftBrace": self.block_start,
            "LeftBracket": self.string_interpretation,
            "LeftParen": self.paren_start,
            "lem": self.ignore_production,
            "lemma": self.ignore_production,
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
            "Mapping": self.mapping_stop,
            "NamedVariableDeclaration": self.named_variable_declaration_stop,
            "Namespace": self.ignore_production,
            "NamespaceBlock": self.ignore_production,
            "NamespaceIdentifier": self.namespace_identifier_dispatcher,
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
            "post": self.ignore_production,
            "postulate": self.ignore_production,
            "pre": self.default_interpretation,  # todo
            "pred": self.ignore_production,
            "predicate": self.ignore_production,
            "Predicate": self.default_interpretation,  # todo
            "PredicateDefinitionBlock": self.default_interpretation,  # todo
            "PredicateHeader": self.predicate_header_dispatcher,
            "PredicateIdentifier": self.predicate_identifier_dispatcher,
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
            "prop": self.ignore_production,
            "Property": self.property_stop,
            "PropertyHeader": self.property_start,
            "PropertyList": self.default_interpretation,  # todo
            "proposition": self.ignore_production,
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
            "RightBrace": self.block_stop,
            "RightBracket": self.string_interpretation,
            "RightParen": self.paren_stop,
            "RuleOfInference": self.inference_stop,
            "RuleOfInferenceList": self.ignore_production,
            "RulesOfInferenceBlock": self.inference_block_stop,
            "self": self.default_interpretation,  # todo
            "SemiColon": self.default_interpretation,  # todo
            "Signature": self.signature_stop,
            "Slash": self.default_interpretation,  # todo
            "Star": self.string_interpretation,
            "Statement": self.default_interpretation,  # todo
            "StatementList": self.default_interpretation,  # todo
            "SW": self.ignore_production,
            "template": self.default_interpretation,  # todo
            "TemplateHeader": self.default_interpretation,  # todo
            "th": self.default_interpretation,  # todo
            "theorem": self.ignore_production,
            "TheoremLikeStatementOrConjecture": self.theorem_like_statement_stop,
            "TheoremLikeStatementOrConjectureHeader": self.theorem_like_statement_start,
            "theory": self.ignore_production,
            "TheoryBlock": self.theory_stop,
            "TheoryHeader": self.theory_start,
            "thm": self.ignore_production,
            "Tilde": self.default_interpretation,  # todo
            "To": self.default_interpretation,  # todo
            "tpl": self.default_interpretation,  # todo
            "Translation": self.default_interpretation,  # todo
            "TranslationList": self.default_interpretation,  # todo
            "trivial": self.default_interpretation,  # todo
            "true": self.default_interpretation,  # todo
            "TupleOfTypes": self.default_interpretation,  # todo
            "Type": self.handle_type,
            "TypeOrTupleOfTypes": self.default_interpretation,  # todo
            "TypeWithCoord": self.default_interpretation,  # todo
            "undef": self.default_interpretation,  # todo
            "undefined": self.default_interpretation,  # todo
            "UndefinedHeader": self.default_interpretation,  # todo
            "uses": self.uses_start,
            "UsesClause": self.uses_stop,
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
        interpretation = None
        try:
            interpretation = self.interpret_switcher(parsing_info)
        except AssertionError as err:
            self.errors.append(
                fplerror.FplInterpreterMessage(str(err), parsing_info.rule_line(), parsing_info.rule_col()))
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

    def namespace_identifier_dispatcher(self, parsing_info: AuxInterpretation):
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
                    "########### Unhandled context in predicate_identifier_dispatcher " + str(
                        self._context.get_context()) + " " + str(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def predicate_identifier_dispatcher(self, parsing_info: AuxInterpretation):
        parsing_info = self.concatenation_of_proceeding_string_rules(parsing_info)
        # PredicateIdentifier can occur in following different  contexts:
        if self._context.is_parsing_context([AuxOutlines.inferenceRules, AuxOutlines.block]):
            # as a name of an inference rule
            SymbolTable.add_inference_rule_to_theory(self._theory_node, parsing_info)
            return self.inference_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.axiom, AuxOutlines.signature]):
            # as a name of an axiom that is global
            SymbolTable.add_axiom_to_theory(self._theory_node, parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.classDeclaration]):
            # as a name of a class instance definition
            # we put the class instance name on the working stack because we have yet to update it with its type
            # (see general_type_dispatcher)
            self._working_stack.append(SymbolTable.add_class_to_theory(self._theory_node, parsing_info))
            self._context.push_context(AuxOutlines.classType, self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.classType]):
            # as a name of a class type, do nothing since general_type_dispatcher handles this
            pass
        elif self._context.is_parsing_context([AuxOutlines.mandatoryProperty]) or \
                self._context.is_parsing_context([AuxOutlines.optionalProperty]):
            # as the type of a class instance definition
            # we put the type name on the working stack so we can get it back
            # when the name of the class instance definition will be parsed next in the context
            # [AuxOutlines.mandatoryProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            # [AuxOutlines.optionalProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            self._working_stack.append(parsing_info.get_interpretation())
            return self.class_instance_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.theoremLikeStmtThm, AuxOutlines.signature]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtLem, AuxOutlines.signature]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtProp, AuxOutlines.signature]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtCor, AuxOutlines.signature]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtConj, AuxOutlines.signature]):
            # as a name of a predicate definition that is global
            SymbolTable.add_theorem_like_stmt(self._theory_node, parsing_info, self._context.get_context()[-2])
        elif self._context.is_parsing_context([AuxOutlines.predicateDeclaration, AuxOutlines.signature]):
            # as a name of a predicate definition that is global
            SymbolTable.add_predicate_to_theory(self._theory_node, parsing_info)
        elif self._context.is_parsing_context(
                [AuxOutlines.mandatoryProperty, AuxOutlines.functionalTerm, AuxOutlines.signature]) or \
                self._context.is_parsing_context(
                    [AuxOutlines.optionalProperty, AuxOutlines.functionalTerm, AuxOutlines.signature]):
            # as a name of a functional term property
            # we put the functional term name on the working stack because we have yet to update
            # it with its image (see general_type_dispatcher)
            parent_node = self._working_stack[-1]
            is_mandatory = (self._context.get_context()[-3] == AuxOutlines.mandatoryProperty)
            self._working_stack.append(
                SymbolTable.add_property_to_node(parent_node, parsing_info, is_mandatory,
                                                 self._context.get_context()[-2]))
        elif self._context.is_parsing_context(
                [AuxOutlines.mandatoryProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature]) or \
                self._context.is_parsing_context(
                    [AuxOutlines.optionalProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature]):
            # as a name of a class instance property
            # we put the class instance name on the working stack because we have yet to update
            # it with its image (see general_type_dispatcher)
            property_type = self._working_stack.pop()
            parent_node = self._working_stack[-1]
            is_mandatory = (self._context.get_context()[-3] == AuxOutlines.mandatoryProperty)
            self._working_stack.append(
                SymbolTable.add_property_to_node(parent_node, parsing_info, is_mandatory, property_type))
        elif self._context.is_parsing_context([AuxOutlines.functionalTerm, AuxOutlines.signature]):
            # as a name of a functional term definition that is global
            # we put the functional term name on the working stack because we have yet to update
            # it with its image (see general_type_dispatcher)
            self._working_stack.append(SymbolTable.add_functional_term_to_theory(self._theory_node, parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.classDeclaration, AuxOutlines.block]):
            # as the name of a Constructor
            class_node = self._working_stack[-1]
            SymbolTable.add_constructor_to_class(class_node, parsing_info)
            return self.constructor_start(parsing_info)
        else:
            if self._debug():
                print(
                    "########### Unhandled context in predicate_identifier_dispatcher " + str(
                        self._context.get_context()) + " " + str(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def named_variable_declaration_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.varDeclaration), self.get_debug_parsing_info(parsing_info)
        return parsing_info

    def named_variable_declaration_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.varDeclaration], self.get_debug_parsing_info(parsing_info))
        return None

    def uses_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.uses, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def uses_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.uses], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def inference_block_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.inferenceRules, self.get_debug_parsing_info(parsing_info))
        return None

    def inference_block_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.inferenceRules], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def inference_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.inferenceRule, self.get_debug_parsing_info(parsing_info))
        return self.signature_start(parsing_info)

    def inference_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.inferenceRule], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def theory_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.theory, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def theory_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.theory], self.get_debug_parsing_info(parsing_info))
        return None

    def axiom_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.axiom, self.get_debug_parsing_info(parsing_info))
        return self.signature_start(parsing_info)

    def axiom_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.axiom], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def theorem_like_statement_start(self, parsing_info: AuxInterpretation):
        if parsing_info.get_cst() == 'thm' or parsing_info.get_cst() == 'theorem':
            self._context.push_context(AuxOutlines.theoremLikeStmtThm, self.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'prop' or parsing_info.get_cst() == 'proposition':
            self._context.push_context(AuxOutlines.theoremLikeStmtProp, self.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'lem' or parsing_info.get_cst() == 'lemma':
            self._context.push_context(AuxOutlines.theoremLikeStmtLem, self.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'cor' or parsing_info.get_cst() == 'corollary':
            self._context.push_context(AuxOutlines.theoremLikeStmtCor, self.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'conj' or parsing_info.get_cst() == 'conjecture':
            self._context.push_context(AuxOutlines.theoremLikeStmtConj, self.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected keyword in theorem_like_statement_start " + parsing_info.get_cst())
        return self.signature_start(parsing_info)

    def theorem_like_statement_stop(self, parsing_info: AuxInterpretation):
        if self._context.is_parsing_context([AuxOutlines.theoremLikeStmtThm]):
            self._context.pop_context([AuxOutlines.theoremLikeStmtThm], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.theoremLikeStmtProp]):
            self._context.pop_context([AuxOutlines.theoremLikeStmtProp], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.theoremLikeStmtLem]):
            self._context.pop_context([AuxOutlines.theoremLikeStmtLem], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.theoremLikeStmtCor]):
            self._context.pop_context([AuxOutlines.theoremLikeStmtCor], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.theoremLikeStmtConj]):
            self._context.pop_context([AuxOutlines.theoremLikeStmtConj], self.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected context in theorem_like_statement_stop " + parsing_info.get_cst())
        return None  # do not append to parse_list, we are done with this

    def property_start(self, parsing_info: AuxInterpretation):
        if parsing_info.get_cst() == 'opt' or parsing_info.get_cst() == 'optional':
            self._context.push_context(AuxOutlines.optionalProperty, self.get_debug_parsing_info(parsing_info))
        elif parsing_info.get_cst() == 'mand' or parsing_info.get_cst() == 'mandatory':
            self._context.push_context(AuxOutlines.mandatoryProperty, self.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected keyword in property_start " + parsing_info.get_cst())
        return None

    def property_stop(self, parsing_info: AuxInterpretation):
        if self._context.is_parsing_context([AuxOutlines.optionalProperty]):
            self._context.pop_context([AuxOutlines.optionalProperty], self.get_debug_parsing_info(parsing_info))
        elif self._context.is_parsing_context([AuxOutlines.mandatoryProperty]):
            self._context.pop_context([AuxOutlines.mandatoryProperty], self.get_debug_parsing_info(parsing_info))
        else:
            raise AssertionError("Unexpected context in property_stop " + str(parsing_info.get_cst()))
        return None  # do not append to parse_list, we are done with this

    def constructor_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.classConstructor, self.get_debug_parsing_info(parsing_info))
        return self.signature_start(parsing_info)

    def constructor_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.classConstructor], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def predicate_header_dispatcher(self, parsing_info: AuxInterpretation):
        # a predicate header can occur in the following contexts:
        if self._context.is_parsing_context([AuxOutlines.theory, AuxOutlines.block]):
            # inside a theory as a global predicate definition
            return self.predicate_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.optionalProperty]) or \
                self._context.is_parsing_context([AuxOutlines.mandatoryProperty]):
            # inside a class, or functional term, a predicate instance
            return self.predicate_declaration_start(parsing_info)
        else:
            if self._debug():
                print("########### Unhandled context in predicate_header_dispatcher" + str(
                    self._context.get_context()) + " " + str(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def paren_start(self, parsing_info: AuxInterpretation):
        # starts a new parenthesis
        self._context.push_context(AuxOutlines.paren, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def paren_stop(self, parsing_info: AuxInterpretation):
        # stops a parenthesis
        self._context.pop_context([AuxOutlines.paren], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def block_start(self, parsing_info: AuxInterpretation):
        # starts a new block
        self._context.push_context(AuxOutlines.block, self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def block_stop(self, parsing_info: AuxInterpretation):
        # stops a block
        self._context.pop_context([AuxOutlines.block], self.get_debug_parsing_info(parsing_info))

    def predicate_declaration_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.predicateDeclaration, self.get_debug_parsing_info(parsing_info))
        return self.signature_start(parsing_info)

    def predicate_declaration_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.predicateDeclaration], self.get_debug_parsing_info(parsing_info))
        return None  # do not append to parse_list, we are done with this

    def class_instance_declaration_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.classInstanceDeclaration, self.get_debug_parsing_info(parsing_info))
        return self.signature_start(parsing_info)

    def class_instance_declaration_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.classInstanceDeclaration], self.get_debug_parsing_info(parsing_info))
        self._working_stack.pop()  # remove the class instance node from the working stack
        return None  # do not append to parse_list, we are done with this

    def class_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.classDeclaration, self.get_debug_parsing_info(parsing_info))
        return None  # classes have no signature, we are done

    def class_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.classDeclaration], self.get_debug_parsing_info(parsing_info))
        self._working_stack.pop()  # remove the class node
        return None  # do not append to parse_list, we are done with this

    def functional_term_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.functionalTerm, self.get_debug_parsing_info(parsing_info))
        return self.signature_start(parsing_info)

    def functional_term_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.functionalTerm], self.get_debug_parsing_info(parsing_info))
        self._working_stack.pop()
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
        if self._context.is_parsing_context([AuxOutlines.signature, AuxOutlines.paren]):
            return self.named_variable_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.classDeclaration, AuxOutlines.block]):
            return self.named_variable_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.axiom, AuxOutlines.block]):
            return self.named_variable_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.inferenceRule, AuxOutlines.block]):
            return self.named_variable_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.predicateDeclaration, AuxOutlines.block]):
            return self.named_variable_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.theoremLikeStmtThm, AuxOutlines.block]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtLem, AuxOutlines.block]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtConj, AuxOutlines.block]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtCor, AuxOutlines.block]) or \
                self._context.is_parsing_context([AuxOutlines.theoremLikeStmtProp, AuxOutlines.block]):
            return self.named_variable_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.classConstructor, AuxOutlines.block]):
            return self.named_variable_declaration_start(parsing_info)
        else:
            if self._debug():
                print(
                    "########### Unhandled context in variable_list_interpretation " + str(
                        self._context.get_context()) + " " + str(parsing_info))
        return variable_list

    def general_type_dispatcher(self, parsing_info: AuxInterpretation):
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
            class_node = self._working_stack[-1]
            class_node.type = general_type.typeRepresentation
            # we clear the context of classType
            self._context.pop_context([AuxOutlines.classType], self.get_debug_parsing_info(parsing_info))
            return None  # this general type is handled completely
        elif self._context.is_parsing_context([AuxOutlines.optionalProperty]) or \
                self._context.is_parsing_context([AuxOutlines.mandatoryProperty]):
            # as the type of property definition
            # we put the type name on the working stack so we can get it back
            # when the name of the class instance definition will be parsed next in the context
            # [AuxOutlines.mandatoryProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            # [AuxOutlines.optionalProperty, AuxOutlines.classInstanceDeclaration, AuxOutlines.signature] or
            self._working_stack.append(general_type.typeRepresentation)
            return self.class_instance_declaration_start(parsing_info)
        elif self._context.is_parsing_context([AuxOutlines.functionalTerm, AuxOutlines.functionalTermImage]):
            # as the image of a functional term
            functional_term_node = self._working_stack[-1]
            image_node = SymbolTable.get_image_node(functional_term_node)
            SymbolTable.add_param_to_image_node(image_node, general_type)
            return None
        else:
            if self._debug():
                print("########### Unhandled context in general_type_dispatcher" + str(
                    self._context.get_context()) + " " + str(parsing_info))
            return general_type

    def mapping_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.functionalTermImage, self.get_debug_parsing_info(parsing_info))
        return None

    def mapping_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.functionalTermImage], self.get_debug_parsing_info(parsing_info))
        return None

    def signature_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.signature, self.get_debug_parsing_info(parsing_info))
        return None

    def signature_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.signature], self.get_debug_parsing_info(parsing_info))
        if self._context.is_parsing_context([AuxOutlines.functionalTerm]):
            return self.mapping_start(parsing_info)
        return None

    def is_operator_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.isoperator, self.get_debug_parsing_info(parsing_info))
        return None

    def is_operator_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.isoperator], self.get_debug_parsing_info(parsing_info))
        return None

    def all_quantor_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.allquantor, self.get_debug_parsing_info(parsing_info))
        return None

    def all_quantor_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.allquantor], self.get_debug_parsing_info(parsing_info))
        return None

    def ex_quantor_start(self, parsing_info: AuxInterpretation):
        self._context.push_context(AuxOutlines.exquantor, self.get_debug_parsing_info(parsing_info))
        return None

    def ex_quantor_stop(self, parsing_info: AuxInterpretation):
        self._context.pop_context([AuxOutlines.exquantor], self.get_debug_parsing_info(parsing_info))
        return None

    def handle_type(self, paring_info: AuxInterpretation):
        self.clean_up_parse_list(
            ["tpl", "template", "TemplateHeader", "IdStartsWithCap", "LongTemplateHeader", "obj", "object",
             "ObjectHeader", "Digit", "function", "func", "FunctionalTermHeader", "predicate", "pred",
             "PredicateHeader", "AliasedId", "Dot", "PredicateIdentifier", "At", "ext"])
        return Type(paring_info)
