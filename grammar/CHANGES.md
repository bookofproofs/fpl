# Changes in the FPL grammar
## 1.0.0 
Initial grammar
## 1.0.1
* Insignificant whitespaces replaced by significant ones in ProofArgument
## 1.0.2
* DerivedPredicate replaced by Predicate in PremiseOrOtherPredicate to prevent not meaningful productions like "assume qed"
## 1.0.3
* SW in Alias instead of IW
## 1.0.4
* VariableType replaced by Type in CoordInSignature to simplify the syntax
## 1.1.0
* Grouping of some existing rules to new rules ArgumentParam and ArgumentParamList
* Simplification of CoordInSignature by replacing Coord with Variable | extDigit
* Removal of rule ReferencedResultIdentifier and replacement by PrimePredicate
* Option ArgumentParam added to PrimePredicate to reflect the previous change
* Removed ArgumentParamList since it is now covered by PrimePredicate
* Removed ParamList since it now consist only of one option NamedVariableDeclarationList
* Replaced ParamList by NamedVariableDeclarationList in ParamTuple
* Removed AnonymousDeclaration of variables because they would be otherwise ambiguous when handling their instantiation
* Removed VariableDeclaration because its option rule simplified to only one rule NamedVariableDeclaration
* Replaced VariableDeclaration by NamedVariableDeclaration in VariableDeclarationList
* Renamed VariableDeclarationList to NamedVariableDeclarationList
* Renamed AnonymousSignature to ParenthesisedGeneralType
* Removed TupleOfTypes since replaced by a more general ParamTuple
* Removed TypeOrTupleOfTypes since its option rules simplified to only one rule VariableType
## 1.1.1
* Removed extDigit from CoordInSignature, so that special types (like natural numbers) have to be disambiguated by declaring/initializing them as variables previously
* Moved extDigit from Identifier to PrimePredicate to allow calling the more disambiguated Nat(100) instead of 100 and to prevent derivations of PredicateWithArgument starting with a extDigit. 
* Replaced GeneralType by Type in DefinitionClass, since the complexity of the type of a class consistently and fully described by its constructors.
* Replaced Type in CoordInSignature by PredicateWithArguments to enable using calls of constructors instead of types (disambiguation).
* Renamed CoordInSignature by CoordInType.
* Renamed RangeInSignature by RangeInType.
## 1.1.2
* Simplified syntax of the is operator by replacing VariableType by GeneralType according to changes made in 1.1.1
* Removed rules AmpersandVariable and Ampersand (no use cases in proof-based mathematics identified that could not be covered by the remaining FPL syntax)
## 1.1.3
* Added rule VariableRange to simplify the implementation of RangeOrLoopBody
* Replaced sequence "Variable Dollar" by the existing rule KeysOfVariadicVariable (with the same sequence) in IndexValue
* Added optional PropertyList to PredicateDefinitionBlock, since predicates might have also properties in PBM.
* Created new rule PredicateInstance replacing DefinitionPredicate in DefinitionProperty to prevent more than one nesting of predicates and their properties.
* Create new rule PredicateInstanceBlock as a copy of original PredicateDefinitionBlock without PropertyList.
* Replaced GeneralType by VariableType in ClassInstance to enable parameterized types using inner variables of a definition.
* Changed the order of options in DefinitionProperty to disambiguate GeneralType from FunctionalTermHeader / PredicateHeader that it contains. 
* Renamed ProofHeadHeader to ProofHeader
* Renamed ProofIdentifier to ReferencingIdentifier (a generalization since it will be used in CorollarySignature)
* Added rule CorollarySignature to distinguish it from other Signatures
* Separated a new rule CorollaryHeader from TheoremLikeStatementOrConjectureHeader
* Added rule DollarDigitList to enable nesting of corollaries.
* Replaced VariableList by PredicateList in PythonDelegate (generalization)
* ## 1.1.4
* Added intermediate rule ClassSignature in DefinitionClass
