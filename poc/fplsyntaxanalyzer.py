from poc.fplerror import FplErrorManager
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
from poc.classes.ContextComment import ContextComment
from poc.classes.ContextConclusionHeader import ContextConclusionHeader
from poc.classes.ContextConstructor import ContextConstructor
from poc.classes.ContextConstructorBlock import ContextConstructorBlock
from poc.classes.ContextCoordInType import ContextCoordInType
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
from poc.classes.ContextDefaultResult import ContextDefaultResult
from poc.classes.ContextDefinition import ContextDefinition
from poc.classes.ContextDefinitionClass import ContextDefinitionClass
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
from poc.classes.ContextKeyword import ContextKeyword
from poc.classes.ContextLanguageCode import ContextLanguageCode
from poc.classes.ContextLeftBound import ContextLeftBound
from poc.classes.ContextLocalization import ContextLocalization
from poc.classes.ContextLocalizationBlock import ContextLocalizationBlock
from poc.classes.ContextLocalizationHeader import ContextLocalizationHeader
from poc.classes.ContextLongComment import ContextLongComment
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

    def __init__(self, root: AnyNode, theory_name: str, error_mgr: FplErrorManager, namespace: str):
        self.i = AuxISourceAnalyser(error_mgr, root, theory_name, namespace)
        self.ast_list = []

        self.switcher = {
            "Alias": self.default_interpretation,
            "alias": ContextKeyword.dispatch,
            "AliasedId": self.default_interpretation,
            "All": ContextAll.dispatch,
            "all": ContextKeyword.dispatch,
            "and": ContextKeyword.dispatch,
            "ArgumentIdentifier": ContextArgumentIdentifier.dispatch,
            "ArgumentInference": ContextArgumentInference.dispatch,
            "ArgumentParam": ContextArgumentParam.dispatch,
            "ass": ContextKeyword.dispatch,
            "assert": ContextKeyword.dispatch,
            "AssertionStatement": ContextAssertionStatement.dispatch,
            "Assignee": ContextAssignee.dispatch,
            "AssignmentStatement": ContextAssignmentStatement.dispatch,
            "assume": ContextKeyword.dispatch,
            "AssumedPredicate": ContextAssumedPredicate.dispatch,
            "AssumeHeader": ContextAssumeHeader.dispatch,
            "At": self.default_interpretation,
            "AtList": self.default_interpretation,
            "ax": ContextKeyword.dispatch,
            "Axiom": ContextAxiom.dispatch,
            "axiom": ContextKeyword.dispatch,
            "AxiomBlock": ContextAxiomBlock.dispatch,
            "AxiomHeader": ContextAxiomHeader.dispatch,
            "BuildingBlock": ContextBuildingBlock.dispatch,
            "BuildingBlockList": self.default_interpretation,
            "CallModifier": self.default_interpretation,
            "case": ContextKeyword.dispatch,
            "cases": ContextKeyword.dispatch,
            "CaseStatement": ContextCaseStatement.dispatch,
            "cl": ContextKeyword.dispatch,
            "class": ContextKeyword.dispatch,
            "ClassHeader": ContextClassHeader.dispatch,
            "ClassInstance": ContextClassInstance.dispatch,
            "ClassSignature": ContextClassSignature.dispatch,
            "ClosedOrOpenRange": ContextClosedOrOpenRange.dispatch,
            "Colon": self.default_interpretation,
            "ColonEqual": self.default_interpretation,
            "Comma": self.default_interpretation,
            "Comment": ContextComment.dispatch,
            "CompoundPredicate": ContextCompoundPredicate.dispatch,
            "con": ContextKeyword.dispatch,
            "conclusion": ContextKeyword.dispatch,
            "ConclusionBlock": ContextConclusionBlock.dispatch,
            "ConclusionHeader": ContextConclusionHeader.dispatch,
            "ConditionFollowedByResult": ContextConditionFollowedByResult.dispatch,
            "ConditionFollowedByResultList": ContextConditionFollowedByResultList.dispatch,
            "conj": ContextKeyword.dispatch,
            "conjecture": ContextKeyword.dispatch,
            "Conjunction": ContextConjunction.dispatch,
            "Constructor": ContextConstructor.dispatch,
            "ConstructorBlock": ContextConstructorBlock.dispatch,
            "Coord": ContextCoord.dispatch,
            "CoordInType": ContextCoordInType.dispatch,
            "CoordList": ContextCoordList.dispatch,
            "cor": ContextKeyword.dispatch,
            "corollary": ContextKeyword.dispatch,
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
            "DollarDigitList": ContextDollarDigitList.dispatch,
            "Dollar": self.default_interpretation,
            "Dot": self.default_interpretation,
            "EBNFBar": self.default_interpretation,
            "EBNFFactor": ContextEBNFFactor.dispatch,
            "EBNFString": ContextEBNFString.dispatch,
            "EBNFTerm": ContextEBNFTerm.dispatch,
            "EBNFTransl": ContextEBNFTransl.dispatch,
            "else": ContextKeyword.dispatch,
            "end": ContextKeyword.dispatch,
            "Entity": ContextEntity.dispatch,
            "EntityWithCoord": ContextEntityWithCoord.dispatch,
            "Equivalence": ContextEquivalence.dispatch,
            "ex": ContextKeyword.dispatch,
            "ExclamationMark": self.default_interpretation,
            "ExclusiveOr": ContextExclusiveOr.dispatch,
            "Exists": ContextExists.dispatch,
            "ExistsHeader": self.default_interpretation,
            "ExistsTimesN": self.default_interpretation,
            "ext": ContextKeyword.dispatch,
            "extDigits": self.default_interpretation,
            "ExtensionBlock": ContextExtensionBlock.dispatch,
            "ExtensionContent": self.default_interpretation,
            "ExtensionHeader": self.default_interpretation,
            "ExtensionName": self.default_interpretation,
            "ExtensionTail": self.default_interpretation,
            "ExtensionRegex": self.default_interpretation,
            "false": ContextTrueFalse.dispatch,
            "func": ContextKeyword.dispatch,
            "function": ContextKeyword.dispatch,
            "FunctionalTermDefinitionBlock": ContextFunctionalTermDefinitionBlock.dispatch,
            "FunctionalTermHeader": ContextFunctionalTermHeader.dispatch,
            "FunctionalTermInstance": ContextFunctionalTermInstance.dispatch,
            "FunctionalTermSignature": ContextFunctionalTermSignature.dispatch,
            "GeneralType": ContextGeneralType.dispatch,
            "Identifier": ContextIdentifier.dispatch,
            "IdStartsWithCap": self.default_interpretation,
            "IdStartsWithSmallCase": self.ignore_production,
            "iif": ContextKeyword.dispatch,
            "impl": ContextKeyword.dispatch,
            "Implication": ContextImplication.dispatch,
            "ind": ContextKeyword.dispatch,
            "index": ContextKeyword.dispatch,
            "IndexHeader": ContextIndexHeader.dispatch,
            "IndexValue": ContextIndexValue.dispatch,
            "inf": ContextKeyword.dispatch,
            "inference": ContextKeyword.dispatch,
            "InferenceHeader": ContextInferenceHeader.dispatch,
            "InstanceBlock": ContextInstanceBlock.dispatch,
            "is": ContextKeyword.dispatch,
            "IsOperator": ContextIsOperator.dispatch,
            "IW": self.ignore_production,
            "Justification": ContextJustification.dispatch,
            "KeysOfVariadicVariable": ContextKeysOfVariadicVariable.dispatch,
            "LanguageCode": ContextLanguageCode.dispatch,
            "LeftBound": ContextLeftBound.dispatch,
            "LeftBrace": self.default_interpretation,
            "LeftBracket": self.default_interpretation,
            "LeftParen": self.default_interpretation,
            "lem": ContextKeyword.dispatch,
            "lemma": ContextKeyword.dispatch,
            "loc": ContextKeyword.dispatch,
            "Localization": ContextLocalization.dispatch,
            "localization": self.default_interpretation,
            "LocalizationBlock": ContextLocalizationBlock.dispatch,
            "LocalizationHeader": ContextLocalizationHeader.dispatch,
            "LocalizationList": self.default_interpretation,
            "LongComment": ContextLongComment.dispatch,
            "LongTemplateHeader": ContextLongTemplateHeader.dispatch,
            "loop": ContextKeyword.dispatch,
            "LoopStatement": ContextLoopStatement.dispatch,
            "mand": ContextKeyword.dispatch,
            "mandatory": ContextKeyword.dispatch,
            "Mapping": ContextMapping.dispatch,
            "NamedVariableDeclaration": ContextNamedVariableDeclaration.dispatch,
            "NamedVariableDeclarationList": self.default_interpretation,
            "Namespace": ContextNamespace.dispatch,
            "NamespaceBlock": self.default_interpretation,
            "NamespaceIdentifier": ContextNamespaceIdentifier.dispatch,
            "NamespaceModifier": self.default_interpretation,
            "Negation": ContextNegation.dispatch,
            "not": ContextKeyword.dispatch,
            "obj": ContextKeyword.dispatch,
            "object": ContextKeyword.dispatch,
            "ObjectDefinitionBlock": ContextObjectDefinitionBlock.dispatch,
            "ObjectHeader": ContextObjectHeader.dispatch,
            "opt": ContextKeyword.dispatch,
            "optional": ContextKeyword.dispatch,
            "or": ContextKeyword.dispatch,
            "ParamTuple": ContextParamTuple.dispatch,
            "ParenthesisedGeneralType": ContextParenthesisedGeneralType.dispatch,
            "ParenthesisedPredicate": ContextParenthesisedPredicate.dispatch,
            "Plus": self.default_interpretation,
            "post": ContextKeyword.dispatch,
            "postulate": ContextKeyword.dispatch,
            "pre": ContextKeyword.dispatch,
            "pred": ContextKeyword.dispatch,
            "predicate": ContextKeyword.dispatch,
            "Predicate": ContextPredicate.dispatch,
            "PredicateDefinitionBlock": ContextPredicateDefinitionBlock.dispatch,
            "PredicateHeader": ContextPredicateHeader.dispatch,
            "PredicateIdentifier": ContextPredicateIdentifier.dispatch,
            "PredicateInstance": ContextPredicateInstance.dispatch,
            "PredicateInstanceBlock": ContextPredicateInstanceBlock.dispatch,
            "PredicateList": ContextPredicateList.dispatch,
            "PredicateWithArguments": ContextPredicateWithArguments.dispatch,
            "premise": ContextKeyword.dispatch,
            "PremiseBlock": ContextPremiseBlock.dispatch,
            "PremiseConclusionBlock": ContextPremiseConclusionBlock.dispatch,
            "PremiseHeader": ContextPremiseHeader.dispatch,
            "PremiseOrOtherPredicate": ContextPremiseOrOtherPredicate.dispatch,
            "prf": ContextKeyword.dispatch,
            "PrimePredicate": ContextPrimePredicate.dispatch,
            "proof": ContextKeyword.dispatch,
            "Proof": ContextProof.dispatch,
            "ProofArgument": ContextProofArgument.dispatch,
            "ProofArgumentList": self.default_interpretation,
            "ProofBlock": ContextProofBlock.dispatch,
            "ProofHeader": ContextProofHeader.dispatch,
            "prop": ContextKeyword.dispatch,
            "Property": ContextProperty.dispatch,
            "PropertyHeader": ContextPropertyHeader.dispatch,
            "PropertyList": self.default_interpretation,
            "proposition": ContextKeyword.dispatch,
            "py": ContextKeyword.dispatch,
            "PythonDelegate": ContextPythonDelegate.dispatch,
            "PythonIdentifier": self.default_interpretation,
            "qed": ContextKeyword.dispatch,
            "QualifiedIdentifier": ContextQualifiedIdentifier.dispatch,
            "Range": ContextRange.dispatch,
            "range": ContextKeyword.dispatch,
            "RangeInType": ContextRangeInType.dispatch,
            "RangeOrLoopBody": ContextRangeOrLoopBody.dispatch,
            "RangeStatement": ContextRangeStatement.dispatch,
            "ReferencingIdentifier": ContextReferencingIdentifier.dispatch,
            "ret": ContextKeyword.dispatch,
            "return": ContextKeyword.dispatch,
            "ReturnHeader": ContextReturnHeader.dispatch,
            "ReturnStatement": ContextReturnStatement.dispatch,
            "rev": ContextKeyword.dispatch,
            "Revoke": ContextRevoke.dispatch,
            "revoke": ContextKeyword.dispatch,
            "RevokeHeader": ContextRevokeHeader.dispatch,
            "RightBound": ContextRightBound.dispatch,
            "RightBrace": self.default_interpretation,
            "RightBracket": self.default_interpretation,
            "RightParen": self.default_interpretation,
            "RuleOfInference": ContextRuleOfInference.dispatch,
            "RuleOfInferenceList": self.default_interpretation,
            "RulesOfInferenceBlock": ContextRulesOfInferenceBlock.dispatch,
            "self": ContextKeyword.dispatch,
            "SemiColon": self.default_interpretation,
            "Signature": ContextSignature.dispatch,
            "Slash": self.default_interpretation,
            "Star": self.default_interpretation,
            "Statement": ContextStatement.dispatch,
            "StatementList": ContextStatementList.dispatch,
            "SW": self.ignore_production,
            "template": ContextKeyword.dispatch,
            "TemplateHeader": ContextTemplateHeader.dispatch,
            "th": ContextKeyword.dispatch,
            "theorem": ContextKeyword.dispatch,
            "TheoremLikeStatementOrConjecture": ContextTheoremLikeStatementOrConjecture.dispatch,
            "TheoremLikeStatementOrConjectureHeader": ContextTheoremLikeStatementOrConjectureHeader.dispatch,
            "theory": ContextKeyword.dispatch,
            "TheoryBlock": ContextTheoryBlock.dispatch,
            "TheoryHeader": ContextTheoryHeader.dispatch,
            "thm": ContextKeyword.dispatch,
            "Tilde": self.default_interpretation,
            "To": self.default_interpretation,
            "tpl": ContextKeyword.dispatch,
            "Translation": ContextTranslation.dispatch,
            "TranslationList": self.default_interpretation,
            "trivial": ContextKeyword.dispatch,
            "true": ContextTrueFalse.dispatch,
            "Type": ContextType.dispatch,
            "TypeWithCoord": ContextTypeWithCoord.dispatch,
            "undef": ContextKeyword.dispatch,
            "undefined": ContextKeyword.dispatch,
            "UndefinedHeader": ContextUndefinedHeader.dispatch,
            "uses": ContextKeyword.dispatch,
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
            "xor": ContextKeyword.dispatch,
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
                self.i.error_mgr.add_error(
                    FplInterpreterMessage(str(err), parsing_info.rule_line(), parsing_info.rule_col(),
                                          self.i.theory_node.theory_name))
        return ast

    def syntax_analysis_switcher(self, parsing_info: AuxInterpretation):
        rule = parsing_info.rule_name()
        func = self.switcher.get(rule, lambda: "Invalid rule")
        """
        if self.i.verbose:
            print("switched " + (str(func)).split(" ")[1] + " for " + str(parsing_info))
        """
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
