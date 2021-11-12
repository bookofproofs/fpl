/* THIS IS AN AUTOMATICALLY GENERATED FILE VIA THE tree_sitter_converter.py UTILITY */
/* IT CONTAINS THE CURRENT FPL GRAMMAR TO BE USED WITH tree-sitter */


module.exports = grammar({
  name: 'fpl',
  conflicts: $ => [
    [$.NamespaceBlock],
    [$.NamespaceIdentifier],
    [$.WildcardTheoryNamespace],
    [$.WildcardTheoryNamespaceList],
    [$.RuleOfInferenceList],
    [$.BuildingBlockList],
    [$.AliasedId, $.PredicateIdentifier],
    [$.PredicateWithArguments, $.PrimePredicate],
    [$.AssignmentStatement, $.Identifier],
    [$.LocalizationList],
    [$.TheoryBlock],
    [$.AliasedId],
    [$.VariableList],
    [$.VariableList, $.Entity],
    [$.VariableSpecificationList],
    [$.PropertyList],
    [$.PredicateList],
    [$.ConditionFollowedByResultList],
    [$.Range],
    [$.CoordList, $.Range],
    [$.Coord, $.Identifier],
    [$.Coord, $.Identifier, $.AssignmentStatement],
    [$.TranslationList],
    [$.PremiseBlock],
    [$.PremiseConclusionBlock],
    [$.FunctionalTermDefinitionBlock, $.Property, $.VariableSpecificationList],
    [$.FunctionalTermDefinitionBlock, $.Property],
    [$.CoordList],
    [$.RangeInSignature],
    [$.Type, $.Identifier],
    [$.Property],
    [$.FunctionalTermDefinitionBlock],
    [$.DefinitionPredicate, $.Type],
    [$.FunctionalTermSignature, $.Type],
    [$.VariableSpecification, $.PrimePredicate],
    [$.PredicateDefinitionBlock, $.VariableSpecificationList],
    [$.ProofArgumentList],
    [$.PredicateDefinitionBlock],
    [$.AxiomBlock, $.VariableSpecificationList],
    [$.AxiomBlock],
    [$.ProofBlock],
    [$.StatementList],
    [$.EBNFTransl],
    [$.EBNFTerm],
    [$.DefinitionContentList],
    [$.ObjectDefinitionBlock, $.Property, $.VariableSpecificationList],
    [$.ObjectDefinitionBlock, $.Property],
    [$.Justification],
    [$.ObjectDefinitionBlock],
  ],
  rules: {
    Namespace: $ => seq(repeat($.CW), $.NamespaceIdentifier, repeat($.CW), $.NamespaceBlock, repeat($.CW)), 
    NamespaceBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.ExtensionBlock), repeat($.CW), optional($.UsesClause), repeat($.CW), optional($.RulesOfInferenceBlock), repeat($.CW), $.TheoryBlock, repeat($.CW), optional($.LocalizationBlock), repeat($.CW), $.RightBrace), 
    WildcardTheoryNamespaceList: $ => seq($.WildcardTheoryNamespace, repeat(seq(optional($.IW), $.Comma, optional($.IW), $.WildcardTheoryNamespace))), 
    ExtensionBlock: $ => seq($.ExtensionHeader, $.SW, $.ExtensionContent, optional($.IW), $.ExtensionTail), 
    ExtensionHeader: $ => seq($.Colon, $.ext), 
    ExtensionContent: $ => /.*/, 
    ExtensionTail: $ => seq($.Colon, $.end, $.SW), 
    ext: $ => "ext", 
    end: $ => "end", 
    UsesClause: $ => seq($.uses, $.SW, $.WildcardTheoryNamespaceList, $.SW), 
    TheoryBlock: $ => seq($.TheoryHeader, repeat($.CW), $.LeftBrace, repeat($.CW), optional($.BuildingBlockList), repeat($.CW), $.RightBrace), 
    RulesOfInferenceBlock: $ => seq($.InferenceHeader, repeat($.CW), $.LeftBrace, repeat($.CW), $.RuleOfInferenceList, repeat($.CW), $.RightBrace), 
    InferenceHeader: $ => choice($.inference, $.inf), 
    inference: $ => "inference", 
    inf: $ => "inf", 
    PremiseHeader: $ => choice($.premise, $.pre), 
    premise: $ => "premise", 
    pre: $ => "pre", 
    ConclusionHeader: $ => choice($.conclusion, $.con), 
    conclusion: $ => "conclusion", 
    con: $ => "con", 
    RuleOfInferenceList: $ => seq($.RuleOfInference, repeat(seq(repeat($.CW), $.RuleOfInference))), 
    RuleOfInference: $ => seq($.Signature, optional($.IW), $.PremiseConclusionBlock), 
    PremiseConclusionBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.VariableSpecificationList), repeat($.CW), $.PremiseBlock, repeat($.CW), $.ConclusionBlock, repeat($.CW), $.RightBrace), 
    PremiseBlock: $ => seq($.PremiseHeader, optional($.IW), $.Colon, repeat($.CW), optional($.Predicate)), 
    ConclusionBlock: $ => seq($.ConclusionHeader, optional($.IW), $.Colon, repeat($.CW), $.Predicate), 
    TheoryHeader: $ => choice($.theory, $.th), 
    theory: $ => "theory", 
    th: $ => "th", 
    BuildingBlockList: $ => seq($.BuildingBlock, repeat(seq(repeat($.CW), $.BuildingBlock))), 
    BuildingBlock: $ => choice($.Definition, $.Axiom, $.TheoremLikeStatementOrConjecture, $.Proof), 
    uses: $ => "uses", 
    Definition: $ => choice($.DefinitionClass, $.DefinitionPredicate, $.DefinitionFunctionalTerm), 
    DefinitionClass: $ => seq($.ClassHeader, $.SW, $.PredicateIdentifier, optional($.IW), $.Colon, optional($.IW), $.Type, repeat($.CW), $.ObjectDefinitionBlock), 
    ObjectDefinitionBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.VariableSpecificationList), repeat($.CW), optional($.DefinitionContentList), repeat($.CW), $.RightBrace), 
    FunctionalTermDefinitionBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.VariableSpecificationList), repeat($.CW), optional($.PropertyList), repeat($.CW), $.RightBrace), 
    DefinitionContentList: $ => seq($.DefinitionContent, repeat(seq(repeat($.CW), $.DefinitionContent))), 
    DefinitionContent: $ => choice($.Property, $.Constructor), 
    DefinitionFunctionalTerm: $ => seq($.FunctionalTermSignature, repeat($.CW), $.FunctionalTermDefinitionBlock), 
    FunctionalTermSignature: $ => seq($.FunctionalTermHeader, $.SW, $.Signature, optional($.IW), $.Mapping), 
    Mapping: $ => seq($.To, optional($.IW), $.VariableType), 
    VariableSpecificationList: $ => repeat1(seq(repeat($.CW), $.VariableSpecification, $.SW)), 
    VariableSpecification: $ => choice($.Statement, $.NamedVariableDeclaration), 
    AssertionStatement: $ => seq($.assert, $.SW, $.Predicate), 
    assert: $ => "assert", 
    NamedVariableDeclaration: $ => seq($.VariableList, optional($.IW), $.Colon, optional($.IW), $.VariableType), 
    VariableType: $ => choice($.ParenthesisedGeneralType, $.GeneralType), 
    GeneralType: $ => seq(optional($.CallModifier), choice($.TypeWithCoord, $.Type, $.IndexHeader)), 
    IndexHeader: $ => choice($.index, $.ind), 
    index: $ => "index", 
    ind: $ => "ind", 
    Type: $ => choice($.PredicateIdentifier, $.XId, $.PredicateHeader, $.FunctionalTermHeader, $.ObjectHeader), 
    VariableList: $ => seq($.Variable, repeat(seq(optional($.IW), $.Comma, optional($.IW), $.Variable))), 
    DefinitionPredicate: $ => seq($.PredicateHeader, $.SW, $.Signature, repeat($.CW), $.PredicateDefinitionBlock), 
    PredicateHeader: $ => choice($.predicate, $.pred), 
    FunctionalTermHeader: $ => choice($.function, $.func), 
    PredicateDefinitionBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.VariableSpecificationList), repeat($.CW), optional($.Predicate), repeat($.CW), $.RightBrace), 
    PredicateIdentifier: $ => choice($.AliasedId, $.IdStartsWithCap), 
    AliasedId: $ => seq($.IdStartsWithCap, repeat1(seq($.Dot, $.IdStartsWithCap))), 
    ClassHeader: $ => choice($.class, $.cl), 
    class: $ => "class", 
    cl: $ => "cl", 
    predicate: $ => "predicate", 
    pred: $ => "pred", 
    function: $ => "function", 
    func: $ => "func", 
    To: $ => "->", 
    ObjectHeader: $ => choice($.object, $.obj, $.LongTemplateHeader, $.TemplateHeader), 
    LongTemplateHeader: $ => seq($.TemplateHeader, choice($.IdStartsWithCap, $.Digit)), 
    TemplateHeader: $ => choice($.template, $.tpl), 
    object: $ => "object", 
    obj: $ => "obj", 
    template: $ => "template", 
    tpl: $ => "tpl", 
    Axiom: $ => seq($.AxiomHeader, $.SW, $.Signature, repeat($.CW), $.AxiomBlock), 
    AxiomHeader: $ => choice($.axiom, $.ax, $.postulate, $.post), 
    AxiomBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.VariableSpecificationList), repeat($.CW), $.Predicate, repeat($.CW), $.RightBrace), 
    axiom: $ => "axiom", 
    ax: $ => "ax", 
    postulate: $ => "postulate", 
    post: $ => "post", 
    PropertyList: $ => repeat1($.Property), 
    Property: $ => seq(repeat($.CW), $.PropertyHeader, $.SW, $.DefinitionProperty), 
    DefinitionProperty: $ => choice($.ClassInstance, $.DefinitionPredicate, $.FunctionalTermInstance), 
    ClassInstance: $ => seq($.GeneralType, $.SW, $.Signature, repeat($.CW), $.InstanceBlock), 
    FunctionalTermInstance: $ => seq($.FunctionalTermSignature, repeat($.CW), $.InstanceBlock), 
    PropertyHeader: $ => choice($.mandatory, $.mand, $.optional, $.opt), 
    mandatory: $ => "mandatory", 
    mand: $ => "mand", 
    optional: $ => "optional", 
    opt: $ => "opt", 
    Constructor: $ => seq($.Signature, repeat($.CW), $.InstanceBlock), 
    InstanceBlock: $ => seq($.LeftBrace, repeat($.CW), $.VariableSpecificationList, repeat($.CW), $.RightBrace), 
    Signature: $ => seq($.PredicateIdentifier, optional($.IW), $.ParamTuple), 
    ParenthesisedGeneralType: $ => seq($.GeneralType, optional($.IW), $.ParamTuple), 
    ParamTuple: $ => seq($.LeftParen, optional($.IW), optional($.NamedVariableDeclarationList), optional($.IW), $.RightParen), 
    ArgumentParam: $ => seq($.Slash, $.ArgumentIdentifier), 
    NamedVariableDeclarationList: $ => seq($.NamedVariableDeclaration, repeat(seq(optional($.IW), $.Comma, optional($.IW), $.NamedVariableDeclaration))), 
    TypeWithCoord: $ => seq($.Type, $.LeftBound, optional($.IW), choice($.RangeInType, $.CoordInType), optional($.IW), $.RightBound), 
    RangeInType: $ => seq(optional($.CoordInType), optional($.IW), $.Tilde, optional($.IW), optional($.CoordInType)), 
    CoordInType: $ => choice($.PredicateWithArguments, $.Variable), 
    EntityWithCoord: $ => seq($.Entity, $.LeftBracket, optional($.IW), choice($.Range, $.CoordList), optional($.IW), $.RightBracket), 
    CoordList: $ => seq($.Coord, repeat(seq(optional($.IW), $.Comma, optional($.IW), $.Coord))), 
    Entity: $ => choice($.Variable, seq($.AtList, $.self), $.self), 
    AtList: $ => repeat1($.At), 
    Coord: $ => choice($.Assignee, $.PrimePredicate), 
    Range: $ => seq(optional($.Coord), optional($.IW), $.Tilde, optional($.IW), optional($.Coord)), 
    CallModifier: $ => choice($.Star, $.Plus), 
    Plus: $ => "+", 
    ConditionFollowedByResultList: $ => seq($.ConditionFollowedByResult, repeat(seq(repeat($.CW), $.ConditionFollowedByResult))), 
    ConditionFollowedByResult: $ => seq($.Predicate, repeat($.CW), $.Colon, repeat($.CW), $.StatementList), 
    At: $ => "@", 
    TheoremLikeStatementOrConjecture: $ => seq($.TheoremLikeStatementOrConjectureHeader, $.SW, $.Signature, optional($.IW), $.PremiseConclusionBlock), 
    TheoremLikeStatementOrConjectureHeader: $ => choice($.theorem, $.thm, $.conjecture, $.conj, $.proposition, $.prop, $.lemma, $.lem, $.corollary, $.cor), 
    theorem: $ => "theorem", 
    thm: $ => "thm", 
    proposition: $ => "proposition", 
    prop: $ => "prop", 
    lemma: $ => "lemma", 
    lem: $ => "lem", 
    corollary: $ => "corollary", 
    cor: $ => "cor", 
    conjecture: $ => "conjecture", 
    conj: $ => "conj", 
    Proof: $ => seq($.ProofHeadHeader, $.SW, $.ProofIdentifier, optional($.IW), $.ProofBlock), 
    ProofIdentifier: $ => seq($.PredicateIdentifier, $.Dollar, $.Digit), 
    ProofHeadHeader: $ => choice($.proof, $.prf), 
    ProofBlock: $ => seq($.LeftBrace, repeat($.CW), optional($.VariableSpecificationList), repeat($.CW), $.ProofArgumentList, repeat($.CW), $.RightBrace), 
    ProofArgumentList: $ => seq($.ProofArgument, repeat(seq(repeat($.CW), $.ProofArgument))), 
    ProofArgument: $ => seq($.ArgumentIdentifier, $.Dot, $.SW, optional(seq($.Justification, $.SW)), $.ArgumentInference, $.SW), 
    VDash: $ => "|-", 
    AssumeHeader: $ => choice($.assume, $.ass), 
    AssumedPredicate: $ => seq($.AssumeHeader, $.SW, $.PremiseOrOtherPredicate), 
    DerivedPredicate: $ => seq($.VDash, $.SW, choice($.Predicate, $.qed, $.trivial)), 
    qed: $ => "qed", 
    trivial: $ => "trivial", 
    PremiseOrOtherPredicate: $ => choice($.PremiseHeader, $.Predicate), 
    ArgumentInference: $ => choice($.AssumedPredicate, $.DerivedPredicate, $.Revoke), 
    Revoke: $ => seq($.RevokeHeader, $.SW, $.ArgumentParam), 
    RevokeHeader: $ => choice($.revoke, $.rev), 
    Justification: $ => seq($.Slash, $.PrimePredicate, repeat(seq(optional($.IW), $.Comma, optional($.IW), $.Slash, $.PrimePredicate))), 
    Slash: $ => "/", 
    proof: $ => "proof", 
    prf: $ => "prf", 
    assume: $ => "assume", 
    ass: $ => "ass", 
    revoke: $ => "revoke", 
    rev: $ => "rev", 
    true: $ => "true", 
    false: $ => "false", 
    not: $ => "not", 
    and: $ => "and", 
    or: $ => "or", 
    impl: $ => "impl", 
    iif: $ => "iif", 
    xor: $ => "xor", 
    is: $ => "is", 
    Predicate: $ => choice($.CompoundPredicate, $.PrimePredicate), 
    PrimePredicate: $ => choice($.PredicateWithArguments, $.QualifiedIdentifier, $.Statement, $.Identifier, $.IsOperator, $.true, $.false, $.UndefinedHeader, $.ArgumentParam, $.extDigit), 
    QualifiedIdentifier: $ => seq($.Identifier, repeat1(seq($.Dot, $.PredicateWithArguments))), 
    PredicateWithArguments: $ => seq($.Identifier, optional($.IW), $.LeftParen, optional($.IW), optional($.PredicateList), optional($.IW), $.RightParen), 
    Identifier: $ => choice($.PredicateIdentifier, $.AmpersandVariable, $.IndexValue, $.Assignee), 
    AmpersandVariable: $ => seq($.Ampersand, $.Variable), 
    IndexValue: $ => seq($.Variable, $.Dollar, choice($.Digit, $.Variable)), 
    Ampersand: $ => "&", 
    self: $ => "self", 
    PredicateList: $ => seq($.Predicate, repeat(seq(repeat($.CW), $.Comma, repeat($.CW), $.Predicate))), 
    CompoundPredicate: $ => choice($.Conjunction, $.Disjunction, $.Implication, $.Equivalence, $.ExclusiveOr, $.Negation, $.All, $.Exists), 
    IsOperator: $ => seq($.is, optional($.IW), $.LeftParen, repeat($.CW), $.Identifier, repeat($.CW), $.Comma, optional($.IW), $.VariableType, optional($.IW), $.RightParen), 
    Negation: $ => seq($.not, optional($.IW), $.ParenthesisedPredicate), 
    Conjunction: $ => seq($.and, repeat($.CW), $.LeftParen, repeat($.CW), $.PredicateList, repeat($.CW), $.RightParen), 
    Disjunction: $ => seq($.or, repeat($.CW), $.LeftParen, repeat($.CW), $.PredicateList, repeat($.CW), $.RightParen), 
    Implication: $ => seq($.impl, optional($.CW), $.LeftParen, repeat($.CW), $.Predicate, repeat($.CW), $.Comma, repeat($.CW), $.Predicate, repeat($.CW), $.RightParen), 
    Equivalence: $ => seq($.iif, optional($.CW), $.LeftParen, repeat($.CW), $.Predicate, repeat($.CW), $.Comma, repeat($.CW), $.Predicate, repeat($.CW), $.RightParen), 
    ExclusiveOr: $ => seq($.xor, optional($.CW), $.LeftParen, repeat($.CW), $.Predicate, repeat($.CW), $.Comma, repeat($.CW), $.Predicate, repeat($.CW), $.RightParen), 
    ParenthesisedPredicate: $ => seq($.LeftParen, repeat($.CW), $.Predicate, repeat($.CW), $.RightParen), 
    All: $ => seq($.all, $.SW, $.VariableList, optional($.CW), $.ParenthesisedPredicate), 
    all: $ => "all", 
    Exists: $ => seq($.ExistsHeader, $.SW, $.VariableList, optional($.CW), $.ParenthesisedPredicate), 
    ex: $ => "ex", 
    ExistsHeader: $ => choice($.ExistsTimesN, $.ex), 
    ExistsTimesN: $ => seq($.ex, $.Dollar, $.Digit), 
    Dollar: $ => "$", 
    PythonDelegate: $ => seq($.py, $.Dot, $.PythonIdentifier, optional($.IW), $.LeftParen, optional($.IW), $.VariableList, optional($.IW), $.RightParen), 
    PythonIdentifier: $ => /[a-z_]+/, 
    py: $ => "py", 
    LeftBracket: $ => "[", 
    RightBracket: $ => "]", 
    StatementList: $ => seq($.Statement, $.SW, repeat(seq(repeat($.CW), $.Statement, $.SW))), 
    Statement: $ => choice($.PythonDelegate, $.CaseStatement, $.AssertionStatement, $.AssignmentStatement, $.RangeStatement, $.LoopStatement, $.ReturnStatement), 
    ReturnStatement: $ => seq($.ReturnHeader, $.SW, $.Predicate), 
    CaseStatement: $ => seq($.case, repeat($.CW), $.LeftParen, repeat($.CW), $.ConditionFollowedByResultList, repeat($.CW), $.DefaultResult, repeat($.CW), $.RightParen), 
    LoopStatement: $ => seq($.loop, $.SW, $.RangeOrLoopBody), 
    RangeStatement: $ => seq($.range, $.SW, $.RangeOrLoopBody), 
    RangeOrLoopBody: $ => seq($.Assignee, $.SW, choice($.KeysOfVariadicVariable, $.ClosedOrOpenRange, $.Assignee), repeat($.CW), $.LeftParen, repeat($.CW), $.StatementList, repeat($.CW), $.RightParen), 
    KeysOfVariadicVariable: $ => seq($.Variable, $.Dollar), 
    ClosedOrOpenRange: $ => seq($.LeftBound, optional($.IW), $.Range, optional($.IW), $.RightBound), 
    LeftBound: $ => seq($.LeftBracket, optional($.ExclamationMark)), 
    RightBound: $ => seq(optional($.ExclamationMark), $.RightBracket), 
    ExclamationMark: $ => "!", 
    range: $ => "range", 
    loop: $ => "loop", 
    DefaultResult: $ => seq($.else, optional($.IW), $.Colon, repeat($.CW), $.StatementList), 
    AssignmentStatement: $ => seq($.Assignee, optional($.IW), $.ColonEqual, optional($.IW), $.Predicate), 
    Assignee: $ => choice($.EntityWithCoord, $.Entity), 
    ReturnHeader: $ => choice($.return, $.ret), 
    UndefinedHeader: $ => choice($.undefined, $.undef), 
    return: $ => "return", 
    ret: $ => "ret", 
    undefined: $ => "undefined", 
    undef: $ => "undef", 
    ColonEqual: $ => ":=", 
    else: $ => "else", 
    case: $ => "case", 
    Dot: $ => ".", 
    LeftBrace: $ => "{", 
    RightBrace: $ => "}", 
    LeftParen: $ => "(", 
    RightParen: $ => ")", 
    Comma: $ => ",", 
    Star: $ => "*", 
    Colon: $ => ":", 
    NamespaceIdentifier: $ => seq($.IdStartsWithCap, repeat(seq($.Dot, $.IdStartsWithCap))), 
    ArgumentIdentifier: $ => choice(seq($.Digit, $.IdStartsWithSmallCase), $.Digit), 
    WildcardTheoryNamespace: $ => seq($.NamespaceIdentifier, optional($.NamespaceModifier)), 
    NamespaceModifier: $ => choice(seq($.Dot, $.Star), $.Alias), 
    Alias: $ => seq($.SW, $.alias, $.SW, $.IdStartsWithCap), 
    alias: $ => "alias", 
    IdStartsWithCap: $ => /[A-Z][a-z0-9A-Z_]*/, 
    IdStartsWithSmallCase: $ => /[a-z][a-z0-9A-Z_]*/, 
    SW: $ => $.IW, 
    CW: $ => choice($.IW, $.Comment, $.LongComment), 
    Comment: $ => /\/\/[^\n]*/, 
    LongComment: $ => /\/\*((?:.|\n)*?)\*\//, 
    IW: $ => /[ \r\n\t]+/, 
    XId: $ => seq($.At, $.ext, $.IdStartsWithCap), 
    Variable: $ => $.IdStartsWithSmallCase, 
    Digit: $ => /\d+/, 
    LocalizationBlock: $ => seq($.LocalizationHeader, repeat($.CW), $.LeftBrace, repeat($.CW), $.LocalizationList, repeat($.CW), $.RightBrace), 
    LocalizationList: $ => seq($.Localization, repeat(seq(repeat($.CW), $.Localization))), 
    Localization: $ => seq($.Predicate, optional($.IW), $.ColonEqual, optional($.IW), $.TranslationList, optional($.IW), $.SemiColon), 
    SemiColon: $ => ";",
    Tilde: $ => "~", 
    TranslationList: $ => seq($.Translation, repeat(seq($.SW, $.Translation))), 
    Translation: $ => seq($.Tilde, $.LanguageCode, optional($.IW), $.Colon, optional($.IW), $.EBNFTransl), 
    LanguageCode: $ => /[a-z]{3}/, 
    EBNFTransl: $ => seq($.EBNFTerm, repeat(seq(optional($.IW), $.EBNFBar, optional($.IW), $.EBNFTerm))), 
    EBNFTerm: $ => seq($.EBNFFactor, repeat(seq(optional($.IW), $.EBNFFactor))), 
    EBNFFactor: $ => choice($.Variable, $.EBNFString, seq($.LeftParen, optional($.IW), $.EBNFTransl, optional($.IW), $.RightParen)), 
    EBNFString: $ => /\"[^\"]*\"/, 
    EBNFBar: $ => "|", 
    LocalizationHeader: $ => choice($.localization, $.loc), 
    localization: $ => "localization", 
    loc: $ => "loc", 
    extDigit: $ => /\d+/, 
      }
});
