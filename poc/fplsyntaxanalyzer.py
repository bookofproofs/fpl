from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.ContextAll import ContextAll
from poc.classes.ContextArgumentIdentifier import ContextArgumentIdentifier
from poc.classes.ContextArgumentInference import ContextArgumentInference
from poc.classes.ContextArgumentParam import ContextArgumentParam
from poc.classes.ContextAssertionStatement import ContextAssertionStatement
from poc.classes.ContextAssignee import ContextAssignee
from poc.classes.ContextAssignmentStatement import ContextAssignmentStatement
from poc.classes.ContextAssumedPredicate import ContextAssumedPredicate
from poc.classes.ContextAssumeHeader import ContextAssumeHeader
from poc.classes.ContextAxiom import ContextAxiom
from poc.classes.ContextAxiomHeader import ContextAxiomHeader
from poc.classes.ContextAxiomBlock import ContextAxiomBlock
from poc.classes.ContextBuildingBlock import ContextBuildingBlock
from poc.classes.ContextCaseStatement import ContextCaseStatement
from poc.classes.ContextClassHeader import ContextClassHeader
from poc.classes.ContextClassInstance import ContextClassInstance
from poc.classes.ContextConclusionHeader import ContextConclusionHeader
from poc.classes.ContextConstructor import ContextConstructor
from poc.classes.ContextCoordInType import ContextCoordInType
from poc.classes.ContextDefaultResult import ContextDefaultResult
from poc.classes.ContextDefinitionClass import ContextDefinitionClass
from poc.classes.ContextClassSignature import ContextClassSignature
from poc.classes.ContextClosedOrOpenRange import ContextClosedOrOpenRange
from poc.classes.ContextCompoundPredicate import ContextCompoundPredicate
from poc.classes.ContextConclusionBlock import ContextConclusionBlock
from poc.classes.ContextConditionFollowedByResult import ContextConditionFollowedByResult
from poc.classes.ContextConditionFollowedByResultList import ContextConditionFollowedByResultList
from poc.classes.ContextConjunction import ContextConjunction
from poc.classes.ContextCoord import ContextCoord
from poc.classes.ContextCoordList import ContextCoordList
from poc.classes.ContextCorollaryHeader import ContextCorollaryHeader
from poc.classes.ContextCorollarySignature import ContextCorollarySignature
from poc.classes.ContextDefinition import ContextDefinition
from poc.classes.ContextDefinitionContent import ContextDefinitionContent
from poc.classes.ContextDefinitionContentList import ContextDefinitionContentList
from poc.classes.ContextDefinitionFunctionalTerm import ContextDefinitionFunctionalTerm
from poc.classes.ContextDefinitionPredicate import ContextDefinitionPredicate
from poc.classes.ContextDefinitionProperty import ContextDefinitionProperty
from poc.classes.ContextDerivedPredicate import ContextDerivedPredicate
from poc.classes.ContextDisjunction import ContextDisjunction
from poc.classes.ContextDollarDigitList import ContextDollarDigitList
from poc.classes.ContextEBNFFactor import ContextEBNFFactor
from poc.classes.ContextEBNFString import ContextEBNFString
from poc.classes.ContextEBNFTerm import ContextEBNFTerm
from poc.classes.ContextEBNFTransl import ContextEBNFTransl
from poc.classes.ContextEntity import ContextEntity
from poc.classes.ContextEntityWithCoord import ContextEntityWithCoord
from poc.classes.ContextEquivalence import ContextEquivalence
from poc.classes.ContextExclusiveOr import ContextExclusiveOr
from poc.classes.ContextExists import ContextExists
from poc.classes.ContextExtensionBlock import ContextExtensionBlock
from poc.classes.ContextFunctionalTermDefinitionBlock import ContextFunctionalTermDefinitionBlock
from poc.classes.ContextFunctionalTermHeader import ContextFunctionalTermHeader
from poc.classes.ContextFunctionalTermInstance import ContextFunctionalTermInstance
from poc.classes.ContextFunctionalTermSignature import ContextFunctionalTermSignature
from poc.classes.ContextGeneralType import ContextGeneralType
from poc.classes.ContextIdentifier import ContextIdentifier
from poc.classes.ContextImplication import ContextImplication
from poc.classes.ContextIndexHeader import ContextIndexHeader
from poc.classes.ContextIndexValue import ContextIndexValue
from poc.classes.ContextInferenceHeader import ContextInferenceHeader
from poc.classes.ContextJustification import ContextJustification
from poc.classes.ContextLanguageCode import ContextLanguageCode
from poc.classes.ContextLeftBound import ContextLeftBound
from poc.classes.ContextLocalization import ContextLocalization
from poc.classes.ContextLocalizationBlock import ContextLocalizationBlock
from poc.classes.ContextLocalizationHeader import ContextLocalizationHeader
from poc.classes.ContextLongTemplateHeader import ContextLongTemplateHeader
from poc.classes.ContextLoopStatement import ContextLoopStatement
from poc.classes.ContextInstanceBlock import ContextInstanceBlock
from poc.classes.ContextIsOperator import ContextIsOperator
from poc.classes.ContextKeysOfVariadicVariable import ContextKeysOfVariadicVariable
from poc.classes.ContextMapping import ContextMapping
from poc.classes.ContextObjectDefinitionBlock import ContextObjectDefinitionBlock
from poc.classes.ContextNamedVariableDeclaration import ContextNamedVariableDeclaration
from poc.classes.ContextNamespace import ContextNamespace
from poc.classes.ContextNamespaceIdentifier import ContextNamespaceIdentifier
from poc.classes.ContextNegation import ContextNegation
from poc.classes.ContextObjectHeader import ContextObjectHeader
from poc.classes.ContextParamTuple import ContextParamTuple
from poc.classes.ContextParenthesisedGeneralType import ContextParenthesisedGeneralType
from poc.classes.ContextParenthesisedPredicate import ContextParenthesisedPredicate
from poc.classes.ContextPredicate import ContextPredicate
from poc.classes.ContextPredicateHeader import ContextPredicateHeader
from poc.classes.ContextPredicateInstance import ContextPredicateInstance
from poc.classes.ContextPredicateInstanceBlock import ContextPredicateInstanceBlock
from poc.classes.ContextPredicateWithArguments import ContextPredicateWithArguments
from poc.classes.ContextPremiseBlock import ContextPremiseBlock
from poc.classes.ContextPremiseHeader import ContextPremiseHeader
from poc.classes.ContextPremiseConclusionBlock import ContextPremiseConclusionBlock
from poc.classes.ContextPremiseOrOtherPredicate import ContextPremiseOrOtherPredicate
from poc.classes.ContextPredicateDefinitionBlock import ContextPredicateDefinitionBlock
from poc.classes.ContextPredicateIdentifier import ContextPredicateIdentifier
from poc.classes.ContextPredicateList import ContextPredicateList
from poc.classes.ContextPrimePredicate import ContextPrimePredicate
from poc.classes.ContextProof import ContextProof
from poc.classes.ContextProofArgument import ContextProofArgument
from poc.classes.ContextProofBlock import ContextProofBlock
from poc.classes.ContextProofHeader import ContextProofHeader
from poc.classes.ContextProperty import ContextProperty
from poc.classes.ContextPropertyHeader import ContextPropertyHeader
from poc.classes.ContextPythonDelegate import ContextPythonDelegate
from poc.classes.ContextQualifiedIdentifier import ContextQualifiedIdentifier
from poc.classes.ContextRange import ContextRange
from poc.classes.ContextRangeInType import ContextRangeInType
from poc.classes.ContextRangeOrLoopBody import ContextRangeOrLoopBody
from poc.classes.ContextRangeStatement import ContextRangeStatement
from poc.classes.ContextReferencingIdentifier import ContextReferencingIdentifier
from poc.classes.ContextReturnHeader import ContextReturnHeader
from poc.classes.ContextReturnStatement import ContextReturnStatement
from poc.classes.ContextRevoke import ContextRevoke
from poc.classes.ContextRevokeHeader import ContextRevokeHeader
from poc.classes.ContextRightBound import ContextRightBound
from poc.classes.ContextRuleOfInference import ContextRuleOfInference
from poc.classes.ContextRulesOfInferenceBlock import ContextRulesOfInferenceBlock
from poc.classes.ContextSignature import ContextSignature
from poc.classes.ContextStatement import ContextStatement
from poc.classes.ContextStatementList import ContextStatementList
from poc.classes.ContextTemplateHeader import ContextTemplateHeader
from poc.classes.ContextTheoremLikeStatementOrConjecture import ContextTheoremLikeStatementOrConjecture
from poc.classes.ContextTheoremLikeStatementOrConjectureHeader import ContextTheoremLikeStatementOrConjectureHeader
from poc.classes.ContextTheoryBlock import ContextTheoryBlock
from poc.classes.ContextTheoryHeader import ContextTheoryHeader
from poc.classes.ContextTranslation import ContextTranslation
from poc.classes.ContextTrueFalse import ContextTrueFalse
from poc.classes.ContextType import ContextType
from poc.classes.ContextTypeWithCoord import ContextTypeWithCoord
from poc.classes.ContextXid import ContextXid
from poc.classes.ContextUndefinedHeader import ContextUndefinedHeader
from poc.classes.ContextUsesClause import ContextUsesClause
from poc.classes.ContextVariable import ContextVariable
from poc.classes.ContextVariableList import ContextVariableList
from poc.classes.ContextVariableRange import ContextVariableRange
from poc.classes.ContextVariableSpecification import ContextVariableSpecification
from poc.classes.ContextVariableSpecificationList import ContextVariableSpecificationList
from poc.classes.ContextVariableType import ContextVariableType
from poc.classes.ContextWildcardTheoryNamespace import ContextWildcardTheoryNamespace
from poc.fplerror import FplInterpreterMessage
from anytree import AnyNode


class FPLSyntaxAnalyzer:

    def __init__(self, root: AnyNode, theory_name: str, errors: list):
        self.i = AuxISourceAnalyser(errors, root, theory_name)
        self.ast_list = []

        self.switcher = {
            "Alias": self.default_interpretation,
            "alias": self.default_interpretation,
            "AliasedId": self.default_interpretation,
            "All": ContextAll.dispatch,
            "all": self.default_interpretation,
            "and": self.default_interpretation,
            "ArgumentIdentifier": ContextArgumentIdentifier.dispatch,
            "ArgumentInference": ContextArgumentInference.dispatch,
            "ArgumentParam": ContextArgumentParam.dispatch,
            "ass": self.default_interpretation,
            "assert": self.default_interpretation,
            "AssertionStatement": ContextAssertionStatement.dispatch,
            "Assignee": ContextAssignee.dispatch,
            "AssignmentStatement": ContextAssignmentStatement.dispatch,
            "assume": self.default_interpretation,
            "AssumedPredicate": ContextAssumedPredicate.dispatch,
            "AssumeHeader": ContextAssumeHeader.dispatch,
            "At": self.default_interpretation,
            "AtList": self.default_interpretation,
            "ax": self.default_interpretation,
            "Axiom": ContextAxiom.dispatch,
            "axiom": self.default_interpretation,
            "AxiomBlock": ContextAxiomBlock.dispatch,
            "AxiomHeader": ContextAxiomHeader.dispatch,
            "BuildingBlock": ContextBuildingBlock.dispatch,
            "BuildingBlockList": self.default_interpretation,
            "CallModifier": self.default_interpretation,
            "case": self.default_interpretation,
            "cases": self.default_interpretation,
            "CaseStatement": ContextCaseStatement.dispatch,
            "cl": self.default_interpretation,
            "class": self.default_interpretation,
            "ClassHeader": ContextClassHeader.dispatch,
            "ClassInstance": ContextClassInstance.dispatch,
            "ClassSignature": ContextClassSignature.dispatch,
            "ClosedOrOpenRange": ContextClosedOrOpenRange.dispatch,
            "Colon": self.default_interpretation,
            "ColonEqual": self.default_interpretation,
            "Comma": self.default_interpretation,
            "Comment": self.ignore_production,
            "CompoundPredicate": ContextCompoundPredicate.dispatch,
            "con": self.default_interpretation,
            "conclusion": self.default_interpretation,
            "ConclusionBlock": ContextConclusionBlock.dispatch,
            "ConclusionHeader": ContextConclusionHeader.dispatch,
            "ConditionFollowedByResult": ContextConditionFollowedByResult.dispatch,
            "ConditionFollowedByResultList": ContextConditionFollowedByResultList.dispatch,
            "conj": self.default_interpretation,
            "conjecture": self.default_interpretation,
            "Conjunction": ContextConjunction.dispatch,
            "Constructor": ContextConstructor.dispatch,
            "Coord": ContextCoord.dispatch,
            "CoordInType": ContextCoordInType.dispatch,
            "CoordList": ContextCoordList.dispatch,
            "cor": self.default_interpretation,
            "corollary": self.default_interpretation,
            "CorollaryHeader": ContextCorollaryHeader.dispatch,
            "CorollarySignature": ContextCorollarySignature.dispatch,
            "CW": self.ignore_production,
            "DefaultResult": ContextDefaultResult.dispatch,
            "Definition": ContextDefinition.dispatch,
            "DefinitionClass": ContextDefinitionClass.dispatch,
            "DefinitionContent": ContextDefinitionContent.dispatch,
            "DefinitionContentList": ContextDefinitionContentList.dispatch,
            "DefinitionFunctionalTerm": ContextDefinitionFunctionalTerm.dispatch,
            "DefinitionPredicate": ContextDefinitionPredicate.dispatch,
            "DefinitionProperty": ContextDefinitionProperty.dispatch,
            "DerivedPredicate": ContextDerivedPredicate.dispatch,
            "Digit": self.default_interpretation,
            "DigitIdSmallCase": self.default_interpretation,
            "Disjunction": ContextDisjunction.dispatch,
            "Dollar": self.default_interpretation,
            "DollarDigitList": ContextDollarDigitList.dispatch,
            "Dot": self.default_interpretation,
            "EBNFBar": self.default_interpretation,
            "EBNFFactor": ContextEBNFFactor.dispatch,
            "EBNFString": ContextEBNFString.dispatch,
            "EBNFTerm": ContextEBNFTerm.dispatch,
            "EBNFTransl": ContextEBNFTransl.dispatch,
            "else": self.default_interpretation,
            "end": self.default_interpretation,
            "Entity": ContextEntity.dispatch,
            "EntityWithCoord": ContextEntityWithCoord.dispatch,
            "Equivalence": ContextEquivalence.dispatch,
            "ex": self.default_interpretation,
            "ExclamationMark": self.default_interpretation,
            "ExclusiveOr": ContextExclusiveOr.dispatch,
            "Exists": ContextExists.dispatch,
            "ExistsHeader": self.default_interpretation,
            "ExistsTimesN": self.default_interpretation,
            "ext": self.default_interpretation,
            "extDigit": self.default_interpretation,
            "ExtensionBlock": ContextExtensionBlock.dispatch,
            "ExtensionContent": self.default_interpretation,
            "ExtensionHeader": self.default_interpretation,
            "ExtensionTail": self.default_interpretation,
            "false": ContextTrueFalse.dispatch,
            "func": self.default_interpretation,
            "function": self.default_interpretation,
            "FunctionalTermDefinitionBlock": ContextFunctionalTermDefinitionBlock.dispatch,
            "FunctionalTermHeader": ContextFunctionalTermHeader.dispatch,
            "FunctionalTermInstance": ContextFunctionalTermInstance.dispatch,
            "FunctionalTermSignature": ContextFunctionalTermSignature.dispatch,
            "GeneralType": ContextGeneralType.dispatch,
            "Identifier": ContextIdentifier.dispatch,
            "IdStartsWithCap": self.default_interpretation,
            "IdStartsWithSmallCase": self.ignore_production,
            "iif": self.default_interpretation,
            "impl": self.default_interpretation,
            "Implication": ContextImplication.dispatch,
            "ind": self.default_interpretation,
            "index": self.default_interpretation,
            "IndexHeader": ContextIndexHeader.dispatch,
            "IndexValue": ContextIndexValue.dispatch,
            "inf": self.default_interpretation,
            "inference": self.default_interpretation,
            "InferenceHeader": ContextInferenceHeader.dispatch,
            "InstanceBlock": ContextInstanceBlock.dispatch,
            "is": self.default_interpretation,
            "IsOperator": ContextIsOperator.dispatch,
            "IW": self.ignore_production,
            "Justification": ContextJustification.dispatch,
            "KeysOfVariadicVariable": ContextKeysOfVariadicVariable.dispatch,
            "LanguageCode": ContextLanguageCode.dispatch,
            "LeftBound": ContextLeftBound.dispatch,
            "LeftBrace": self.default_interpretation,
            "LeftBracket": self.default_interpretation,
            "LeftParen": self.default_interpretation,
            "lem": self.default_interpretation,
            "lemma": self.default_interpretation,
            "loc": self.default_interpretation,
            "Localization": ContextLocalization.dispatch,
            "localization": self.default_interpretation,
            "LocalizationBlock": ContextLocalizationBlock.dispatch,
            "LocalizationHeader": ContextLocalizationHeader.dispatch,
            "LocalizationList": self.default_interpretation,
            "LongComment": self.ignore_production,
            "LongTemplateHeader": ContextLongTemplateHeader.dispatch,
            "loop": self.default_interpretation,
            "LoopStatement": ContextLoopStatement.dispatch,
            "mand": self.default_interpretation,
            "mandatory": self.default_interpretation,
            "Mapping": ContextMapping.dispatch,
            "NamedVariableDeclaration": ContextNamedVariableDeclaration.dispatch,
            "NamedVariableDeclarationList": self.default_interpretation,
            "Namespace": ContextNamespace.dispatch,
            "NamespaceBlock": self.default_interpretation,
            "NamespaceIdentifier": ContextNamespaceIdentifier.dispatch,
            "NamespaceModifier": self.default_interpretation,
            "Negation": ContextNegation.dispatch,
            "not": self.default_interpretation,
            "obj": self.default_interpretation,
            "object": self.default_interpretation,
            "ObjectDefinitionBlock": ContextObjectDefinitionBlock.dispatch,
            "ObjectHeader": ContextObjectHeader.dispatch,
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
            "pred": self.default_interpretation,
            "predicate": self.default_interpretation,
            "Predicate": ContextPredicate.dispatch,
            "PredicateDefinitionBlock": ContextPredicateDefinitionBlock.dispatch,
            "PredicateHeader": ContextPredicateHeader.dispatch,
            "PredicateIdentifier": ContextPredicateIdentifier.dispatch,
            "PredicateInstance": ContextPredicateInstance.dispatch,
            "PredicateInstanceBlock": ContextPredicateInstanceBlock.dispatch,
            "PredicateList": ContextPredicateList.dispatch,
            "PredicateWithArguments": ContextPredicateWithArguments.dispatch,
            "premise": self.default_interpretation,
            "PremiseBlock": ContextPremiseBlock.dispatch,
            "PremiseConclusionBlock": ContextPremiseConclusionBlock.dispatch,
            "PremiseHeader": ContextPremiseHeader.dispatch,
            "PremiseOrOtherPredicate": ContextPremiseOrOtherPredicate.dispatch,
            "prf": self.default_interpretation,
            "PrimePredicate": ContextPrimePredicate.dispatch,
            "proof": self.default_interpretation,
            "Proof": ContextProof.dispatch,
            "proofArgument": self.default_interpretation,
            "ProofArgument": ContextProofArgument.dispatch,
            "ProofArgumentList": self.default_interpretation,
            "ProofBlock": ContextProofBlock.dispatch,
            "ProofHeader": ContextProofHeader.dispatch,
            "prop": self.default_interpretation,
            "Property": ContextProperty.dispatch,
            "PropertyHeader": ContextPropertyHeader.dispatch,
            "PropertyList": self.default_interpretation,
            "proposition": self.default_interpretation,
            "py": self.default_interpretation,
            "PythonDelegate": ContextPythonDelegate.dispatch,
            "PythonIdentifier": self.default_interpretation,
            "qed": self.default_interpretation,
            "QualifiedIdentifier": ContextQualifiedIdentifier.dispatch,
            "Range": ContextRange.dispatch,
            "range": self.default_interpretation,
            "RangeInType": ContextRangeInType.dispatch,
            "RangeOrLoopBody": ContextRangeOrLoopBody.dispatch,
            "RangeStatement": ContextRangeStatement.dispatch,
            "ReferencingIdentifier": ContextReferencingIdentifier.dispatch,
            "ret": self.default_interpretation,
            "return": self.default_interpretation,
            "ReturnHeader": ContextReturnHeader.dispatch,
            "ReturnStatement": ContextReturnStatement.dispatch,
            "rev": self.default_interpretation,
            "Revoke": ContextRevoke.dispatch,
            "revoke": self.default_interpretation,
            "RevokeHeader": ContextRevokeHeader.dispatch,
            "RightBound": ContextRightBound.dispatch,
            "RightBrace": self.default_interpretation,
            "RightBracket": self.default_interpretation,
            "RightParen": self.default_interpretation,
            "RuleOfInference": ContextRuleOfInference.dispatch,
            "RuleOfInferenceList": self.default_interpretation,
            "RulesOfInferenceBlock": ContextRulesOfInferenceBlock.dispatch,
            "self": self.default_interpretation,
            "SemiColon": self.default_interpretation,
            "Signature": ContextSignature.dispatch,
            "Slash": self.default_interpretation,
            "Star": self.default_interpretation,
            "Statement": ContextStatement.dispatch,
            "StatementList": ContextStatementList.dispatch,
            "SW": self.ignore_production,
            "template": self.default_interpretation,
            "TemplateHeader": ContextTemplateHeader.dispatch,
            "th": self.default_interpretation,
            "theorem": self.default_interpretation,
            "TheoremLikeStatementOrConjecture": ContextTheoremLikeStatementOrConjecture.dispatch,
            "TheoremLikeStatementOrConjectureHeader": ContextTheoremLikeStatementOrConjectureHeader.dispatch,
            "theory": self.default_interpretation,
            "TheoryBlock": ContextTheoryBlock.dispatch,
            "TheoryHeader": ContextTheoryHeader.dispatch,
            "thm": self.default_interpretation,
            "Tilde": self.default_interpretation,
            "To": self.default_interpretation,
            "tpl": self.default_interpretation,
            "Translation": ContextTranslation.dispatch,
            "TranslationList": self.default_interpretation,
            "trivial": self.default_interpretation,
            "true": ContextTrueFalse.dispatch,
            "Type": ContextType.dispatch,
            "TypeWithCoord": ContextTypeWithCoord.dispatch,
            "undef": self.default_interpretation,
            "undefined": self.default_interpretation,
            "UndefinedHeader": ContextUndefinedHeader.dispatch,
            "uses": self.default_interpretation,
            "UsesClause": ContextUsesClause.dispatch,
            "Variable": ContextVariable.dispatch,
            "VariableList": ContextVariableList.dispatch,
            "VariableRange": ContextVariableRange.dispatch,
            "VariableSpecification": ContextVariableSpecification.dispatch,
            "VariableSpecificationList": ContextVariableSpecificationList.dispatch,
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

        ast_info = AuxAstInfo(context, self.i.theory_node.file_name)
        self.ast_list.append(ast_info)
        self.i.set_pos(ast_info)  # remember the last position
        self.i.ast_info = ast_info
        parsing_info = AuxInterpretation(ast_info, self.i.errors)
        if self.i.verbose:
            # when in debug mode, do not catch AssertionErrors
            # We use AssertionErrors to mine the correctness of the FPL transformer
            self.syntax_analysis_switcher(parsing_info)
        else:
            try:
                self.syntax_analysis_switcher(parsing_info)
            except AssertionError as err:
                self.i.errors.append(
                    FplInterpreterMessage(str(err), parsing_info.rule_line(), parsing_info.rule_col(),
                                          self.i.theory_node.theory_name))
        return ast

    def syntax_analysis_switcher(self, parsing_info: AuxInterpretation):
        rule = parsing_info.rule_name()
        func = self.switcher.get(rule, lambda: "Invalid rule")
        if self.i.verbose:
            print("switched " + (str(func)).split(" ")[1] + " for " + str(parsing_info))
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
