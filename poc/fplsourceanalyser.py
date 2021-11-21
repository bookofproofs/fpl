from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from anytree import AnyNode
from poc.classes.ContextAll import ContextAll
from poc.classes.ContextAssertionStatement import ContextAssertionStatement
from poc.classes.ContextAssignee import ContextAssignee
from poc.classes.ContextAxiom import ContextAxiom
from poc.classes.ContextAxiomBlock import ContextAxiomBlock
from poc.classes.ContextBlock import ContextBlock
from poc.classes.ContextBound import ContextBound
from poc.classes.ContextClass import ContextClass
from poc.classes.ContextCompoundPredicate import ContextCompoundPredicate
from poc.classes.ContextConjunction import ContextConjunction
from poc.classes.ContextDisjunction import ContextDisjunction
from poc.classes.ContextEntity import ContextEntity
from poc.classes.ContextEquivalence import ContextEquivalence
from poc.classes.ContextExclusiveOr import ContextExclusiveOr
from poc.classes.ContextExists import ContextExists
from poc.classes.ContextFunctionalTerm import ContextFunctionalTerm
from poc.classes.ContextGeneralType import ContextGeneralType
from poc.classes.ContextIdentifier import ContextIdentifier
from poc.classes.ContextImplication import ContextImplication
from poc.classes.ContextIndexValue import ContextIndexValue
from poc.classes.ContextInference import ContextInference
from poc.classes.ContextInferenceRules import ContextInferenceRules
from poc.classes.ContextClassInstance import ContextClassInstance
from poc.classes.ContextConstructor import ContextConstructor
from poc.classes.ContextIsOperator import ContextIsOperator
from poc.classes.ContextMapping import ContextMapping
from poc.classes.ContextNamedVariableDeclaration import ContextNamedVariableDeclaration
from poc.classes.ContextNamespaceIdentifier import ContextNamespaceIdentifier
from poc.classes.ContextNegation import ContextNegation
from poc.classes.ContextParamTuple import ContextParamTuple
from poc.classes.ContextParen import ContextParen
from poc.classes.ContextParenthesisedGeneralType import ContextParenthesisedGeneralType
from poc.classes.ContextParenthesisedPredicate import ContextParenthesisedPredicate
from poc.classes.ContextPredicate import ContextPredicate
from poc.classes.ContextPredicateWithArguments import ContextPredicateWithArguments
from poc.classes.ContextDefinitionPredicate import ContextDefinitionPredicate
from poc.classes.ContextPredicateDefinitionBlock import ContextPredicateDefinitionBlock
from poc.classes.ContextPredicateHeader import ContextPredicateHeader
from poc.classes.ContextPredicateIdentifier import ContextPredicateIdentifier
from poc.classes.ContextPrimePredicate import ContextPrimePredicate
from poc.classes.ContextProperty import ContextProperty
from poc.classes.ContextSignature import ContextSignature
from poc.classes.ContextTheoremLikeStatement import ContextTheoremLikeStatement
from poc.classes.ContextTheory import ContextTheory
from poc.classes.ContextTrueFalse import ContextTrueFalse
from poc.classes.ContextType import ContextType
from poc.classes.ContextXid import ContextXid
from poc.classes.ContextUses import ContextUses
from poc.classes.ContextVariable import ContextVariable
from poc.classes.ContextVariableList import ContextVariableList
from poc.classes.ContextVariableType import ContextVariableType
from poc.classes.ContextWildcardTheoryNamespace import ContextWildcardTheoryNamespace
import poc.fplerror


class FPLSourceAnalyser(object):

    def __init__(self, root: AnyNode, theory_name: str, errors: list):
        self.i = AuxISourceAnalyser(errors, root, theory_name)
        self.ast_list = []
        self.i.context.push_context(AuxSymbolTable.root)

        self.switcher = {
            "Alias": self.default_interpretation,
            "alias": self.default_interpretation,
            "AliasedId": self.default_interpretation,
            "All": ContextAll.stop,
            "all": ContextAll.start,
            "and": self.default_interpretation,
            "ArgumentIdentifier": self.default_interpretation,
            "ArgumentInference": self.default_interpretation,
            "ArgumentParam": self.default_interpretation,
            "ass": self.default_interpretation,
            "assert": self.default_interpretation,
            "AssertionStatement": ContextAssertionStatement.dispatch,
            "Assignee": ContextAssignee.dispatch,
            "AssignmentStatement": self.default_interpretation,
            "assume": self.default_interpretation,
            "AssumedPredicate": self.default_interpretation,
            "AssumeHeader": self.default_interpretation,
            "At": self.default_interpretation,
            "AtList": self.default_interpretation,
            "ax": self.default_interpretation,
            "Axiom": ContextAxiom.stop,
            "axiom": self.default_interpretation,
            "AxiomBlock": ContextAxiomBlock.dispatch,
            "AxiomHeader": ContextAxiom.start,
            "BuildingBlock": self.default_interpretation,
            "BuildingBlockList": self.default_interpretation,
            "CallModifier": self.default_interpretation,
            "case": self.default_interpretation,
            "CaseStatement": self.default_interpretation,
            "cl": self.default_interpretation,
            "class": self.default_interpretation,
            "ClassHeader": ContextClass.start,
            "ClassInstance": ContextClassInstance.stop,
            "ClosedOrOpenRange": self.default_interpretation,
            "Colon": self.default_interpretation,
            "ColonEqual": self.default_interpretation,
            "Comma": self.default_interpretation,
            "Comment": self.default_interpretation,
            "CompoundPredicate": ContextCompoundPredicate.dispatch,
            "con": self.default_interpretation,
            "conclusion": self.default_interpretation,
            "ConclusionBlock": self.default_interpretation,
            "ConclusionHeader": self.default_interpretation,
            "ConditionFollowedByResult": self.default_interpretation,
            "ConditionFollowedByResultList": self.default_interpretation,
            "conj": self.default_interpretation,
            "conjecture": self.default_interpretation,
            "Conjunction": ContextConjunction.dispatch,
            "Constructor": ContextConstructor.stop,
            "Coord": self.default_interpretation,
            "CoordInType": self.default_interpretation,
            "CoordList": self.default_interpretation,
            "cor": self.default_interpretation,
            "corollary": self.default_interpretation,
            "CW": self.ignore_production,
            "DefaultResult": self.default_interpretation,
            "Definition": self.default_interpretation,
            "DefinitionClass": ContextClass.stop,
            "DefinitionContent": self.default_interpretation,
            "DefinitionContentList": self.default_interpretation,
            "DefinitionFunctionalTerm": ContextFunctionalTerm.stop,
            "DefinitionPredicate": ContextDefinitionPredicate.stop,
            "DefinitionProperty": self.default_interpretation,
            "DerivedPredicate": self.default_interpretation,
            "Digit": self.default_interpretation,
            "Disjunction": ContextDisjunction.dispatch,
            "Dollar": self.default_interpretation,
            "Dot": self.default_interpretation,
            "EBNFBar": self.default_interpretation,
            "EBNFFactor": self.default_interpretation,
            "EBNFString": self.default_interpretation,
            "EBNFTerm": self.default_interpretation,
            "EBNFTransl": self.default_interpretation,
            "else": self.default_interpretation,
            "end": self.default_interpretation,
            "Entity": ContextEntity.dispatch,
            "EntityWithCoord": self.default_interpretation,
            "Equivalence": ContextEquivalence.dispatch,
            "ex": ContextExists.start,
            "ExclamationMark": self.default_interpretation,
            "ExclusiveOr": ContextExclusiveOr.dispatch,
            "Exists": ContextExists.stop,
            "ExistsHeader": self.default_interpretation,
            "ExistsTimesN": self.default_interpretation,
            "ext": self.default_interpretation,
            "extDigit": self.default_interpretation,
            "ExtensionBlock": self.default_interpretation,
            "ExtensionContent": self.default_interpretation,
            "ExtensionHeader": self.default_interpretation,
            "ExtensionTail": self.default_interpretation,
            "false": ContextTrueFalse.dispatch,
            "func": self.default_interpretation,
            "function": self.default_interpretation,
            "FunctionalTermDefinitionBlock": self.default_interpretation,
            "FunctionalTermHeader": ContextFunctionalTerm.start,
            "FunctionalTermInstance": ContextFunctionalTerm.stop,
            "FunctionalTermSignature": self.default_interpretation,
            "GeneralType": ContextGeneralType.dispatch,
            "Identifier": ContextIdentifier.dispatch,
            "IdStartsWithCap": self.default_interpretation,
            "IdStartsWithSmallCase": self.default_interpretation,
            "iif": self.default_interpretation,
            "impl": self.default_interpretation,
            "Implication": ContextImplication.dispatch,
            "ind": self.default_interpretation,
            "index": self.default_interpretation,
            "IndexHeader": self.default_interpretation,
            "IndexValue": ContextIndexValue.dispatch,
            "inf": self.default_interpretation,
            "inference": self.default_interpretation,
            "InferenceHeader": ContextInferenceRules.start,
            "InstanceBlock": self.default_interpretation,
            "is": self.default_interpretation,
            "IsOperator": ContextIsOperator.dispatch,
            "IW": self.ignore_production,
            "Justification": self.default_interpretation,
            "KeysOfVariadicVariable": self.default_interpretation,
            "LanguageCode": self.default_interpretation,
            "LeftBound": ContextBound.start,
            "LeftBrace": ContextBlock.start,
            "LeftBracket": self.default_interpretation,
            "LeftParen": ContextParen.start,
            "lem": self.default_interpretation,
            "lemma": self.default_interpretation,
            "loc": self.default_interpretation,
            "Localization": self.default_interpretation,
            "localization": self.default_interpretation,
            "LocalizationBlock": self.default_interpretation,
            "LocalizationHeader": self.default_interpretation,
            "LocalizationList": self.default_interpretation,
            "LongComment": self.default_interpretation,
            "LongTemplateHeader": self.default_interpretation,
            "loop": self.default_interpretation,
            "LoopStatement": self.default_interpretation,
            "mand": self.default_interpretation,
            "mandatory": self.default_interpretation,
            "Mapping": ContextMapping.stop,
            "NamedVariableDeclaration": ContextNamedVariableDeclaration.stop,
            "NamedVariableDeclarationList": self.default_interpretation,
            "Namespace": self.default_interpretation,
            "NamespaceBlock": self.default_interpretation,
            "NamespaceIdentifier": ContextNamespaceIdentifier.dispatch,
            "NamespaceModifier": self.default_interpretation,
            "Negation": ContextNegation.dispatch,
            "not": self.default_interpretation,
            "obj": self.default_interpretation,
            "object": self.default_interpretation,
            "ObjectDefinitionBlock": self.default_interpretation,
            "ObjectHeader": self.default_interpretation,
            "opt": self.default_interpretation,
            "optional": self.default_interpretation,
            "or": self.default_interpretation,
            "ParamTuple": ContextParamTuple.dispatch,
            "ParenthesisedGeneralType": ContextParenthesisedGeneralType.dispatch,
            "ParenthesisedPredicate": ContextParenthesisedPredicate.dispatch,
            "Plus": self.default_interpretation,
            "post": self.default_interpretation,
            "postulate": self.default_interpretation,
            "pre": self.default_interpretation,
            "pred": self.default_interpretation,  # noqa
            "predicate": self.default_interpretation,
            "Predicate": ContextPredicate.dispatch,
            "PredicateDefinitionBlock": ContextPredicateDefinitionBlock.dispatch,
            "PredicateHeader": ContextPredicateHeader.dispatch,
            "PredicateIdentifier": ContextPredicateIdentifier.dispatch,
            "PredicateList": self.default_interpretation,
            "PredicateWithArguments": ContextPredicateWithArguments.dispatch,
            "premise": self.default_interpretation,
            "PremiseBlock": self.default_interpretation,
            "PremiseConclusionBlock": self.default_interpretation,
            "PremiseHeader": self.default_interpretation,
            "PremiseOrOtherPredicate": self.default_interpretation,
            "prf": self.default_interpretation,
            "PrimePredicate": ContextPrimePredicate.dispatch,
            "Proof": self.default_interpretation,
            "proof": self.default_interpretation,
            "ProofArgument": self.default_interpretation,
            "ProofArgumentList": self.default_interpretation,
            "ProofBlock": self.default_interpretation,
            "ProofHeadHeader": self.default_interpretation,
            "ProofIdentifier": self.default_interpretation,
            "prop": self.default_interpretation,
            "Property": ContextProperty.stop,
            "PropertyHeader": ContextProperty.start,
            "PropertyList": self.default_interpretation,
            "proposition": self.default_interpretation,
            "py": self.default_interpretation,
            "PythonDelegate": self.default_interpretation,
            "PythonIdentifier": self.default_interpretation,
            "qed": self.default_interpretation,
            "QualifiedIdentifier": self.default_interpretation,
            "Range": self.default_interpretation,
            "range": self.default_interpretation,
            "RangeInType": self.default_interpretation,
            "RangeOrLoopBody": self.default_interpretation,
            "RangeStatement": self.default_interpretation,
            "ret": self.default_interpretation,
            "return": self.default_interpretation,
            "ReturnHeader": self.default_interpretation,
            "ReturnStatement": self.default_interpretation,
            "rev": self.default_interpretation,
            "Revoke": self.default_interpretation,
            "revoke": self.default_interpretation,
            "RevokeHeader": self.default_interpretation,
            "RightBound": ContextBound.stop,
            "RightBrace": ContextBlock.stop,
            "RightBracket": self.default_interpretation,
            "RightParen": ContextParen.stop,
            "RuleOfInference": ContextInference.stop,
            "RuleOfInferenceList": self.default_interpretation,
            "RulesOfInferenceBlock": ContextInferenceRules.stop,
            "self": self.default_interpretation,
            "SemiColon": self.default_interpretation,
            "Signature": ContextSignature.stop,
            "Slash": self.default_interpretation,
            "Star": self.default_interpretation,
            "Statement": self.default_interpretation,
            "StatementList": self.default_interpretation,
            "SW": self.ignore_production,
            "template": self.default_interpretation,
            "TemplateHeader": self.default_interpretation,
            "th": self.default_interpretation,
            "theorem": self.default_interpretation,
            "TheoremLikeStatementOrConjecture": ContextTheoremLikeStatement.stop,
            "TheoremLikeStatementOrConjectureHeader": ContextTheoremLikeStatement.start,
            "theory": self.default_interpretation,
            "TheoryBlock": ContextTheory.stop,
            "TheoryHeader": ContextTheory.start,
            "thm": self.default_interpretation,
            "Tilde": self.default_interpretation,
            "To": self.default_interpretation,
            "tpl": self.default_interpretation,
            "Translation": self.default_interpretation,
            "TranslationList": self.default_interpretation,
            "trivial": self.default_interpretation,
            "true": ContextTrueFalse.dispatch,
            "Type": ContextType.dispatch,
            "TypeWithCoord": self.default_interpretation,
            "undef": self.default_interpretation,
            "undefined": self.default_interpretation,
            "UndefinedHeader": self.default_interpretation,
            "uses": ContextUses.start,
            "UsesClause": ContextUses.stop,
            "Variable": ContextVariable.dispatch,
            "VariableList": ContextVariableList.dispatch,
            "VariableSpecification": self.default_interpretation,
            "VariableSpecificationList": self.default_interpretation,
            "VariableType": ContextVariableType.dispatch,
            "VDash": self.default_interpretation,
            "WildcardTheoryNamespace": ContextWildcardTheoryNamespace.dispatch,
            "WildcardTheoryNamespaceList": self.default_interpretation,
            "XId": ContextXid.dispatch,
            "xor": self.default_interpretation,
        }

    @staticmethod
    def _default(ast):
        """
        If there’s no method matching the rule’s name, TatSu will invoke this method.
        :param ast: ast
        :return: ast
        """
        return ast

    def _postproc(self, context, ast):  # noqa
        """
        This TatSu method will be called after each rule is processed.
        In contrast to _default, this method receives the current parsing context as a parameter that contains
        valuable parsing information like the position and the cst.
        :param context: parsing context
        :param ast: ast
        :return: ast
        """

        ast_info = AuxAstInfo(context, self.i.theory_node.theory_name)
        self.ast_list.append(ast_info)
        parsing_info = AuxInterpretation(ast_info, self.i.errors)
        if self.i.verbose:
            # when in debug mode, do not catch AssertionErrors
            # We use AssertionErrors to mine the correctness of the FPL interpreter
            self.syntax_analysis_switcher(parsing_info)
        else:
            try:
                self.syntax_analysis_switcher(parsing_info)
            except AssertionError as err:
                self.i.errors.append(
                    poc.fplerror.FplInterpreterMessage(str(err), parsing_info.rule_line(), parsing_info.rule_col(),
                                                       self.i.theory_node.theory_name))
        return ast

    def syntax_analysis_switcher(self, parsing_info: AuxInterpretation):
        rule = parsing_info.rule_name()
        func = self.switcher.get(rule, lambda: "Invalid rule")
        if self.i.verbose:
            print("switched " + (str(func)).split(" ")[1] + " for " + str(parsing_info) + " in context " + str(
                self.i.context.get_context()))
        # call the function depending on the rule in the switcher and modify its interpretation and returns its value
        return func(self.i, parsing_info)

    """
    All interpretation delegates
    """

    @staticmethod
    def default_interpretation(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        """
        Copies the parsing context of TatSu into an interpretation
        :param i: interface to the classes named Context<Something>
        :param parsing_info: parsing info of the current rule
        :return: unmodified parsing_info
        """
        i.parse_list.append(parsing_info)
        return None

    @staticmethod
    def ignore_production(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):  # noqa
        """
        Returns None so that the rule will be ignored
        :param i: interface to the classes named Context<Something>
        :param parsing_info: parsing info of the current rule
        :return: None
        """
        return None
