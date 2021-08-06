from classes.AuxDeclaredVariable import AuxDeclaredVariable
from classes.AuxAggrRulesText import AuxAggrRulesText
from classes.AuxInterpretation import AuxInterpretation
from classes.AuxScope import AuxScope
from classes.VariableList import VariableList
from classes.GeneralType import GeneralType
from classes.AuxAstInfo import AuxAstInfo
from classes.Prettifier import Prettifier
import fplerror


class FPLSemantics(object):
    errors = None
    warnings = None
    parse_list = None
    _prettifier = None
    switcher = None
    __scope_stack = None  # used to gather all identified scopes

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.parse_list = []
        self.ast_list = []
        self._prettifier = Prettifier()
        self.__scope_stack = []

        self.switcher = {
            "Alias": self.default_interpretation,
            "alias": self.default_interpretation,
            "AliasedId": self.inter_equals_proceeding_ignored_rules,
            "All": self.default_interpretation,
            "all": self.default_interpretation,
            "Ampersand": self.default_interpretation,
            "AmpersandVariable": self.default_interpretation,
            "and": self.default_interpretation,
            "AnonymousDeclaration": self.default_interpretation,
            "AnonymousSignature": self.default_interpretation,
            "ArgumentIdentifier": self.default_interpretation,
            "ArgumentInference": self.default_interpretation,
            "ass": self.default_interpretation,
            "assert": self.default_interpretation,
            "AssertionStatement": self.default_interpretation,
            "Assignee": self.default_interpretation,
            "AssignmentStatement": self.default_interpretation,
            "assume": self.default_interpretation,
            "AssumedPredicate": self.default_interpretation,
            "AssumeHeader": self.default_interpretation,
            "At": self.default_interpretation,
            "AtList": self.inter_equals_proceeding_ignored_rules,
            "ax": self.default_interpretation,
            "Axiom": self.default_interpretation,
            "axiom": self.default_interpretation,
            "AxiomBlock": self.default_interpretation,
            "AxiomHeader": self.default_interpretation,
            "BuildingBlock": self.default_interpretation,
            "BuildingBlockList": self.default_interpretation,
            "CallModifier": self.inter_equals_proceeding_ignored_rules,
            "case": self.default_interpretation,
            "CaseStatement": self.default_interpretation,
            "cl": self.default_interpretation,
            "class": self.default_interpretation,
            "ClassHeader": self.default_interpretation,
            "ClassInstance": self.default_interpretation,
            "ClosedOrOpenRange": self.default_interpretation,
            "Colon": self.default_interpretation,
            "ColonEqual": self.default_interpretation,
            "Comma": self.default_interpretation,
            "Comment": self.default_interpretation,
            "CompoundPredicate": self.default_interpretation,
            "con": self.default_interpretation,
            "conclusion": self.default_interpretation,
            "ConclusionBlock": self.default_interpretation,
            "ConclusionHeader": self.default_interpretation,
            "ConditionFollowedByResult": self.default_interpretation,
            "ConditionFollowedByResultList": self.default_interpretation,
            "conj": self.default_interpretation,
            "conjecture": self.default_interpretation,
            "Conjunction": self.default_interpretation,
            "Constructor": self.default_interpretation,
            "Coord": self.default_interpretation,
            "CoordInSignature": self.default_interpretation,
            "CoordList": self.default_interpretation,
            "cor": self.default_interpretation,
            "corollary": self.default_interpretation,
            "CW": self.inter_equals_proceeding_ignored_rules,
            "DefaultResult": self.default_interpretation,
            "Definition": self.default_interpretation,
            "DefinitionClass": self.default_interpretation,
            "DefinitionContent": self.default_interpretation,
            "DefinitionContentList": self.default_interpretation,
            "DefinitionFunctionalTerm": self.default_interpretation,
            "DefinitionPredicate": self.default_interpretation,
            "DefinitionProperty": self.default_interpretation,
            "DerivedPredicate": self.default_interpretation,
            "Digit": self.default_interpretation,
            "Disjunction": self.default_interpretation,
            "Dollar": self.default_interpretation,
            "Dot": self.default_interpretation,
            "EBNFBar": self.default_interpretation,
            "EBNFFactor": self.default_interpretation,
            "EBNFString": self.default_interpretation,
            "EBNFTerm": self.default_interpretation,
            "EBNFTransl": self.default_interpretation,
            "else": self.default_interpretation,
            "end": self.default_interpretation,
            "Entity": self.default_interpretation,
            "EntityWithCoord": self.default_interpretation,
            "Equivalence": self.default_interpretation,
            "ex": self.default_interpretation,
            "ExclamationMark": self.default_interpretation,
            "ExclusiveOr": self.default_interpretation,
            "Exists": self.default_interpretation,
            "ExistsHeader": self.default_interpretation,
            "ExistsTimesN": self.default_interpretation,
            "ext": self.default_interpretation,
            "extDigit": self.default_interpretation,
            "ExtensionBlock": self.default_interpretation,
            "ExtensionContent": self.default_interpretation,
            "ExtensionHeader": self.default_interpretation,
            "ExtensionTail": self.default_interpretation,
            "false": self.default_interpretation,
            "func": self.default_interpretation,
            "function": self.default_interpretation,
            "FunctionalTermDefinitionBlock": self.default_interpretation,
            "FunctionalTermHeader": self.inter_equals_proceeding_ignored_rules,
            "FunctionalTermInstance": self.default_interpretation,
            "FunctionalTermSignature": self.default_interpretation,
            "GeneralType": self.general_type_interpretation,
            "Identifier": self.default_interpretation,
            "IdStartsWithCap": self.default_interpretation,
            "IdStartsWithSmallCase": self.default_interpretation,
            "iif": self.default_interpretation,
            "impl": self.default_interpretation,
            "Implication": self.default_interpretation,
            "ind": self.default_interpretation,
            "index": self.default_interpretation,
            "IndexHeader": self.inter_equals_proceeding_ignored_rules,
            "IndexValue": self.default_interpretation,
            "inf": self.default_interpretation,
            "inference": self.default_interpretation,
            "InferenceHeader": self.default_interpretation,
            "InstanceBlock": self.default_interpretation,
            "is": self.default_interpretation,
            "IsOperator": self.default_interpretation,
            "IW": self.default_interpretation,
            "Justification": self.default_interpretation,
            "KeysOfVariadicVariable": self.default_interpretation,
            "LanguageCode": self.default_interpretation,
            "LeftBound": self.inter_equals_proceeding_ignored_rules,
            "LeftBrace": self.start_new_scope,
            "LeftBracket": self.default_interpretation,
            "LeftParen": self.start_new_scope,
            "lem": self.default_interpretation,
            "lemma": self.default_interpretation,
            "loc": self.default_interpretation,
            "Localization": self.default_interpretation,
            "localization": self.default_interpretation,
            "LocalizationBlock": self.default_interpretation,
            "LocalizationHeader": self.default_interpretation,
            "LocalizationList": self.default_interpretation,
            "LongComment": self.default_interpretation,
            "LongTemplateHeader": self.inter_equals_proceeding_ignored_rules,
            "loop": self.default_interpretation,
            "LoopStatement": self.default_interpretation,
            "mand": self.default_interpretation,
            "mandatory": self.default_interpretation,
            "Mapping": self.default_interpretation,
            "NamedVariableDeclaration": self.default_interpretation,
            "Namespace": self.default_interpretation,
            "NamespaceBlock": self.default_interpretation,
            "NamespaceIdentifier": self.inter_equals_proceeding_ignored_rules,
            "NamespaceModifier": self.default_interpretation,
            "Negation": self.default_interpretation,
            "not": self.default_interpretation,
            "obj": self.default_interpretation,
            "object": self.default_interpretation,
            "ObjectDefinitionBlock": self.default_interpretation,
            "ObjectHeader": self.inter_equals_proceeding_ignored_rules,
            "opt": self.default_interpretation,
            "optional": self.default_interpretation,
            "or": self.default_interpretation,
            "ParamList": self.default_interpretation,
            "ParamTuple": self.default_interpretation,
            "ParenthesisedPredicate": self.default_interpretation,
            "Plus": self.default_interpretation,
            "post": self.default_interpretation,
            "postulate": self.default_interpretation,
            "pre": self.default_interpretation,
            "pred": self.default_interpretation,
            "predicate": self.default_interpretation,
            "Predicate": self.default_interpretation,
            "PredicateDefinitionBlock": self.default_interpretation,
            "PredicateHeader": self.inter_equals_proceeding_ignored_rules,
            "PredicateIdentifier": self.inter_equals_proceeding_ignored_rules,
            "PredicateList": self.default_interpretation,
            "PredicateWithArguments": self.default_interpretation,
            "premise": self.default_interpretation,
            "PremiseBlock": self.default_interpretation,
            "PremiseConclusionBlock": self.default_interpretation,
            "PremiseHeader": self.default_interpretation,
            "PremiseOrOtherPredicate": self.default_interpretation,
            "prf": self.default_interpretation,
            "PrimePredicate": self.default_interpretation,
            "Proof": self.default_interpretation,
            "proof": self.default_interpretation,
            "ProofArgument": self.default_interpretation,
            "ProofArgumentList": self.default_interpretation,
            "ProofBlock": self.default_interpretation,
            "ProofHeadHeader": self.default_interpretation,
            "ProofIdentifier": self.default_interpretation,
            "prop": self.default_interpretation,
            "Property": self.default_interpretation,
            "PropertyHeader": self.default_interpretation,
            "PropertyList": self.default_interpretation,
            "proposition": self.default_interpretation,
            "py": self.default_interpretation,
            "PythonDelegate": self.default_interpretation,
            "PythonIdentifier": self.default_interpretation,
            "qed": self.default_interpretation,
            "QualifiedIdentifier": self.default_interpretation,
            "Range": self.default_interpretation,
            "range": self.default_interpretation,
            "RangeInSignature": self.default_interpretation,
            "RangeOrLoopBody": self.default_interpretation,
            "RangeStatement": self.default_interpretation,
            "ReferencedResultIdentifier": self.default_interpretation,
            "ret": self.default_interpretation,
            "return": self.default_interpretation,
            "ReturnHeader": self.default_interpretation,
            "ReturnStatement": self.default_interpretation,
            "rev": self.default_interpretation,
            "Revoke": self.default_interpretation,
            "revoke": self.default_interpretation,
            "RevokeHeader": self.default_interpretation,
            "RightBound": self.inter_equals_proceeding_ignored_rules,
            "RightBrace": self.end_new_scope,
            "RightBracket": self.default_interpretation,
            "RightParen": self.end_new_scope,
            "RuleOfInference": self.default_interpretation,
            "RuleOfInferenceList": self.default_interpretation,
            "RulesOfInferenceBlock": self.default_interpretation,
            "self": self.default_interpretation,
            "SemiColon": self.default_interpretation,
            "Signature": self.default_interpretation,
            "Slash": self.default_interpretation,
            "Star": self.default_interpretation,
            "Statement": self.default_interpretation,
            "StatementList": self.default_interpretation,
            "SW": self.inter_equals_proceeding_ignored_rules,
            "template": self.default_interpretation,
            "TemplateHeader": self.inter_equals_proceeding_ignored_rules,
            "th": self.default_interpretation,
            "theorem": self.default_interpretation,
            "TheoremLikeStatementOrConjecture": self.default_interpretation,
            "TheoremLikeStatementOrConjectureHeader": self.default_interpretation,
            "theory": self.default_interpretation,
            "TheoryBlock": self.default_interpretation,
            "TheoryHeader": self.default_interpretation,
            "thm": self.default_interpretation,
            "Tilde": self.default_interpretation,
            "To": self.default_interpretation,
            "tpl": self.default_interpretation,
            "Translation": self.default_interpretation,
            "TranslationList": self.default_interpretation,
            "trivial": self.default_interpretation,
            "true": self.default_interpretation,
            "TupleOfTypes": self.default_interpretation,
            "Type": self.inter_equals_proceeding_ignored_rules,
            "TypeOrTupleOfTypes": self.default_interpretation,
            "TypeWithCoord": self.default_interpretation,
            "undef": self.default_interpretation,
            "undefined": self.default_interpretation,
            "UndefinedHeader": self.default_interpretation,
            "uses": self.default_interpretation,
            "UsesClause": self.default_interpretation,
            "Variable": self.inter_equals_proceeding_ignored_rules,
            "VariableDeclaration": self.default_interpretation,
            "VariableDeclarationList": self.default_interpretation,
            "VariableList": self.variable_list_interpretation,
            "VariableSpecification": self.default_interpretation,
            "VariableSpecificationList": self.default_interpretation,
            "VariableType": self.default_interpretation,
            "VDash": self.default_interpretation,
            "WildcardTheoryNamespace": self.default_interpretation,
            "WildcardTheoryNamespaceList": self.default_interpretation,
            "XId": self.inter_equals_proceeding_ignored_rules,
            "xor": self.default_interpretation,
        }

    @staticmethod
    def _debug():
        return True

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
        In contrast to _default, this method will receive the current parsing context as parameter:
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
            # append all interpretations that returned something else as None
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

    def inter_equals_proceeding_ignored_rules(self, parsing_info: AuxInterpretation):
        """
        Removes all rules from parsing_list that can be ignored because the interpretation of
        the current rule is a string concatenation of the interpretations of to be ignored rules
        :param parsing_info: the interpretation for a rule
        :return: modified parsing_info
        """
        # concatenate the interpretations of the proceeding rules and remove them from self.parse_list
        aux_ignore = AuxAggrRulesText(self.parse_list, parsing_info.rule_name())
        # the (string) concatenated interpretation of the proceeding rules replaces the interpretation of this rule
        parsing_info.set_interpretation(aux_ignore.inter())
        # replace the complex cst (e.g. lists and dictionaries) by None to save memory. We won't need it any more.
        parsing_info.clear_cst()
        return parsing_info

    def start_new_scope(self, parsing_info: AuxInterpretation):
        """
        Starts a new scope and returns None to prevent appending the beginning of the scope in the parse_list
        :param parsing_info: the interpretation for a rule
        :return: None
        """
        scope = AuxScope()
        scope.set_start(parsing_info)
        parsing_info.set_interpretation("\'" + parsing_info.get_cst() + "\'")
        self.__scope_stack.append(scope)
        return None

    def end_new_scope(self, parsing_info: AuxInterpretation):
        """
        Ends a new scope and returns it so it will be appended in the parse_list
        :param parsing_info: the interpretation for a rule
        :return: Scope object
        """
        if len(self.__scope_stack) > 0:
            scope = self.__scope_stack.pop()
            # does the start correspond to the end?
            if scope.get_start().rule_name() == "LeftParen" and parsing_info.rule_name() != "RightParen":
                self.errors.append(fplerror.FplUnclosedScope(parsing_info, "RightParen"))
            elif scope.get_start().rule_name() == "LeftBrace" and parsing_info.rule_name() != "RightBrace":
                self.errors.append(fplerror.FplUnclosedScope(parsing_info, "RightBrace"))
            else:
                parsing_info.set_interpretation("\'" + parsing_info.get_cst() + "\'")
                scope.set_end(parsing_info)
            return scope
        else:
            self.errors.append(fplerror.FplUnopenedScope(parsing_info))

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
        return general_type

