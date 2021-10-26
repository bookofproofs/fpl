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
