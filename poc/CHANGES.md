# Important Note
This Fpl Parser and FPL Interpreter branch is discontinued. For a continuation, check out the new 
[fpl.net](https://github.com/bookofproofs/fpl.net) repository.

# Changes in the FPL Parser and Interpreter
## 1.11.1
* A new class AuxETNode added
## 1.11.0
* Refactoring
  * Basic classes for auxiliary nodes of the Evaluation Tree (AuxET* classes) added 
## 1.10.18
* Bugfixes FplTypeMismatch 
  * Corrected the recognition of identifiers containing a PascalCase that require the search for matching overrides. 
## 1.10.17
* Bugfixes FplWrongArguments
  * Corrected handling of anonymous building blocks (when  predicate or functional types have themselves arguments)
  * Amended and added some test cases 
## 1.10.16
* Refactoring (resolving further code inspection issues)
## 1.10.15
* Refactoring (resolving further code inspection issues)
## 1.10.14
* Refactoring (resolving further code inspection issues)
* changing author's email address in the FPL High Level Design
## 1.10.13
* Refactoring (resolving code inspection issues)
  * Correcting some gramar errors and types
  * Correcting some unresolved references to class attributes
## 1.10.12
* Refactoring
  * Renaming class names with "integer" into "index" to better align with the FPL syntax 
    * AuxSTInt -> AuxSTIndex
    * InbuiltInt -> InbuiltIndex
    * AuxBits.integer -> AuxBits.index
    * AuxSTType._accepts_any_int() -> AuxSTType._accepts_any_index()
    * AuxInterfaceSTTypePattern.is_integer() -> AuxInterfaceSTTypePattern.is_index()
  * YAGNI: Getting rid of the types InbuiltGeneric, InbuiltExtension, InbuiltClassInstance
* Bugfix
  * Initial implementation of the evaluate methods in AuxSTStatementLoop, AuxSTRange (previously NotImplementedError)
  * Additional robustness test cases inside errors_evaluate folder 
## 1.10.11
* Bugfix
  * Initial implementation of the evaluate methods in AuxSTStatementLoop, AuxSTRange (previously NotImplementedError)
## 1.10.10
* Bugfix
  * Initial implementation of the AuxSTExt evaluate method (previously NotImplementedError)
## 1.10.9
* Bugfix
  * Correcting the evaluation in AuxSTTheoremLikeStatementOrConjecture
  * Reflecting the FPL grammar changes 1.2.1, including affected test cases
* Features:
  * Enabling a proper extension handling
  * New Errors FplExtensionExists, FplExtensionMissingClass, FplExtensionUndeclared, FplExtensionUnknown, FplExtensionMalformed including some related unit tests
## 1.10.8
* Bugfix
  * Correcting FplIllegalRecursion test case (expected values only)
  * Correcting FplVariableNotInitialized false positive error when variables are bound inside a quantor and used as 'calling' arguments. 
## 1.10.7
* Refactoring
  * Replacing AuxSTPredicate outlined as 'extDigit' with the new node type AuxSTExt in the symbol table
  * Adjusting all affected test cases
* Bugfix
  * In AuxSTNodeWithReference: Variables with arity < -1 evaluate to InbuiltValueAtRuntime (bug was to InbuiltValueUndefined) 
## 1.10.6
* Refactoring
  * Continuing to unify some features of AuxSTIdentifier, AuxSTVariable, and AuxSTSelf
  * Replacing deriving AuxSTIdentifier, AuxSTVariable, and AuxSTSelf from AuxInterfaceSTHasReference by a common base class AuxSTNodeWithReference. 
  * Deprecating the arg_type_list and check_args as parameters of the EvaluateParams.evaluate_recursion method and replacing them by storing the input arguments into the instance of the called FPL building block 
  * Deriving all three classes from a new class AuxSTNodeWithReference implementing a unified approach to the evaluate method.
  * Centralizing type compatibility checks at one place via the unified AuxSTType 'accepts' method 
  * Renamed FplPredicateRecursion error into FplIllegalRecursion since it is also applicable to non-predicates
* Debug:
  * AuxSTConstructor was evaluating to InbuiltValueUndefined  
  * AuxSTConstructor calling the constructor of a base class was evaluating to the type of the base class instead of its own class
## 1.10.5
* Refactoring:
  * Continuing to unify some features of AuxSTIdentifier, AuxSTVariable, and AuxSTSelf
    * Replacing AuxSTPredicateWithArgs by AuxSTIdentifier in the whole symbol table 
    * Deleting AuxSTPredicateWithArgs.py
    * Implementing the calculation of the arity of all classes derived from AuxInterfaceSTHasReference, including AuxSTIdentifier
    * Adjusting the evaluate method of AuxSTIdentifier to handle the case with arity >=1, arity=0 (no arguments) or arity=-1 (even no empty parentheses for arguments) 
## 1.10.4
* Refactoring:
  * Trying to unify some features of AuxSTPredicateWithArgs, AuxSTVariable, AuxSTIdentifier and AuxSTSelf by deriving them from a new class AuxInterfaceSTHasReference 
## 1.10.3
* Refactoring:
  * Adding the attribute 'reference' to the AuxSTVariable node in the symbol table
  * Replacing AuxSTPredicateWithArgs outlined as 'var' with AuxSTVariable in the symbol table
  * Replacing AuxSTPredicate outlined as 'undefined' with the new node type AuxSTUndefined in the symbol table
  * Replacing AuxSTPredicate outlined as 'id' with a new node type AuxSTIdentifier in the symbol table
  * Replacing AuxSTPredicate outlined as 'indexValue' and 'variadicVar' (nested into each other) with new node class AuxSTVariableVariadic and AuxSTInt
  * Initial implementation of AuxSTUndefined, AuxSTIdentifier, AuxSTVariableVariadic, and AuxSTInt
  * Renaming InbuiltIndex type to InbuiltVariableVariadic
  * Adjusting the affected test cases of the symbol table
## 1.10.2
* Bugfix:
  * Fixing infinite recursion in AuxSTSelf evaluation
  * Adding new unit tests to identify howe robust and complete the current implementation of the evaluate method in all classes is
* Refactoring
  * Moving the private attribute _declared_type from derived AuxSTOutline to AuxInterfaceSTType 
  * Proper calls of the AuxInterfaceSTType constructor in derived classes
## 1.10.1
* Bugfix
  * Initial implementation of the evaluate method in AuxSTStatementCase, AuxSTStatementCaseDefault, and AuxSTStatementCaseSome
## 1.10.0
* Feature
  * Initial implementation of the evaluate method in AuxSTStatementAssert and AuxSTStatementIsOp
  * AuxSTBuildingBlockInstanceHandler now stores all asserted predicates in the instance.   
* Bugfix
  * Deriving AuxSTAxiom and AuxSTClass from the missing AuxSTTypeInterface
## 1.9.14
* Feature
  * Enhancing the fplsyntaxanalyzer to handle the new grammar rule ConstructorBlock according to the updated FPL grammar 1.2.0
  * This new grammar rule will enable to us to 'call' the constructor of a superclass.  
* Bugfix
  * Correcting a false positive FplTypeMismatch error (expected 'predicate', received 'pred')
  * Replacing the dependency on type_pattern==-1 while cloning a type and initializing type_pattern with 0
  * Correcting the parsing of Variable Lists 
* Refactoring
  * Removing code duplication between the classes AuxSTType and ContextType by creating a common new class AuxInterfaceSTTypePattern
  * Renaming AuxSTTypeInterface into AuxInterfaceSTType
## 1.9.13
* Refactoring
  * Creating a new class AuxEvaluationPredicate to share code between AuxSTPredicate and AuxSTProof
  * Initial implementation of the evaluate method in AuxSTProof
  * Completed missing (initial) implementation of get_long_id and evaluate of AuxSTProof and AuxSTProofArguments
  * Moving the abstract evaluate method from AuxSTBuildingBlock back to AuxOutline to enforce its implementation by all derived classes  
* Bugfix
  * Completed missing zfrom and zto attributes of nodes typed 'AuxSTProofArgument' in the symbol table 
  * Changed the outline of AuxSTProof nodes in the symbol table from "proofArgument" into "proof" 
  * Eliminating unnecessary nested AuxSTProofArgument nodes in the symbol table
  * Eliminating unnecessary nodes with outlines 'corollaries' and 'proofs' inside theorem-like statements in the symbol table 
## 1.9.12
* Bugfix
  * Children of AuxSTVarSpecList with predefined types will be evaluated with the corresponding expected type.
  * Completed missing predefined type (which is InbuiltPredicate) in AuxSTStatementCase, AuxStatementCaseDefault, and AuxSTStatementCaseSome
  * Completed missing (initial) implementations of the evaluate method in AuxSTStatementCase and AuxSTStatementReturn
  * Removed deriving AuxSTVarDec from AuxSTTypeInterface, so it does not mess up the evaluation process.
  * Removing the unnecessary setting the declared type of AuxSTVarDec to InbuiltUndefined instances in SemCheckIdentifiers and AuxSTBuildingBlock
  * Added deriving AuxSTSelf and AuxInbuiltValue from AuxSTTypeInterface
  * Completed missing NotImplemented logic in the evaluation of AuxSTVariable 
* Refactoring
  * Unifying handling registers in AuxSTBuildingBlockInstanceHandler
## 1.9.11
* Refactoring:
  * Abandoning the classes AusPredicateState and SemPredicateAnalyzer and replacing it by a z3-based implementation in AuxInbuiltValue
  * Simplifying the code of the EvaluateParams class 
  * Removing is_of_type methods from AuxSTClass and AuxSTGlobal
## 1.9.10
* Bugfix
  * Completed the missing declared_type of InbuiltValueNamedUndefined
  * Initial implementation of the assignment statement (NotImplementedError)
## 1.9.9
* Refactoring:
  * Replacing the concept of internal representation of a type by wrapper classes AuxInbuiltValue* that will "have" this type
  * By this replacement, we no more misuse inbuilt types to be 'values' of their own.
  * Implementing set_declared_type and get_declared_type only for those nodes in the symbol table where it is necessary
## 1.9.8
* Refactoring:
  * Making get_long_id() in AuxSTOutline abstract to force implementing it in all classes inheriting from AuxSTOutline
  * Implementing the get_long_id() methods in all affected classes
  * Making EvaluateParams class a pure static class by separating a new class AuxEvaluationRegister
  * Renaming local variables named 'eval_params' to 'register' to make their meaning more explicit 
  * Making evaluate() in AuxSTStatement abstract to force implementing it in all inheriting classes. However, those implementations will raise the NotImplementedError  
## 1.9.7
* Refactoring: 
  * Single python files for the classes AuxNodeInstanceHandler, AuxInstanceVariable and AuxNodeInstanceHandlers (originally all in AuxSTBuildingBlock.py) 
  * Renaming these classes into AuxSTBuildingBlockInstanceHandler, AuxSTBuildingBlockInstanceVariable and AuxSTBuildingBlockInstanceHandlers 
  * Cloning instance handlers in AuxSTPredicateWithArgs whenever a 'call' is established to separate the scope of variables for each call
  * Simplified calls of EvaluateParams.evaluate_recursion
## 1.9.6
* Bugfix:
  * Corrected declared type of the return statement, depending on the type of functional term it is in. 
  * Initial evaluation method of AuxSTClass corrected to include the children of AuxSTClass in the symbol table
* Feature: 
  * New FplInvalidUseReturnStmt error + some test cases added 
* Refactoring:
  * Getting rid of the attributes current_* in the SemanticAnalyser class 
## 1.9.5
* Refactoring:
  * The outline of all statements in the symbol table become more specific, replacing the old "type" attribute that was removed in 1.9.4.
  * Adjustments of all affected test-cases of the symbol table
## 1.9.4
* Bugfix:
  * NameError in symbol table robustness tests
  * Minify method when parsing long comments
* Refactoring
  * Providing separate classes for each statement type in the symbol table, adjusting the test cases accordingly.
## 1.9.3
* Refactoring
  * Eliminating the difference between returned_value and value attributes in the AuxEvaluation class
## 1.9.2
* Bugfixes:
  * Some FplVariableBound fixed
* Refactoring
  * Separating the class AuxSTOutline from AuxST.py into a separate AuxSTOutline.py file
* Feature:
  * Minor scope method of all AuxSTOutline-type nodes inside the symbol table
  * A new error FplUnusedBoundVariable + some test cases added 
  * Some test cases added to isolate remaining still occurring FplTypeMismatch errors
## 1.9.1
* Bugfixes:
  * Some FplTypeMismatch errors fixed
## 1.9.0
* Features
  * New class SemPredicateAnalyzer to preprocess all compound and prime predicates, among other to be able to check their satisfiability
  * New class AuxPredicateState to store the state of a predicate (both a compound or a prime)
  * Using the z3 library to check satisfiability of predicates
  * new method get_long_id to better identify predicates with arguments (and their reoccurrences) inside a block
  * new method get_scope to identify the building block each node in the symbol table resists in
* Refactoring
  * Enhancing AuxNodeInstanceHandler to AuxBlockInstanceHandlers as a dictionary of AuxInstanceHandler objects
  * Moving all constants from AuxSymbolTable to AuxSTConstants
  * Moving add_vars_to_node from AuxSymbolTable to new class AuxSymbolTableHelpers
* Bugfixes:
  * Failing FplPremiseNotSatisfiable unit test fixed
  * Failing FplWrongArguments for different generic types unit test fixed 
  * Index error (run-time) while reporting some FplTypeMismatch errors
  * Missing zfrom and zto attributes in inherited properties
* Known Bugs
  * (Still) many false positives with respect to the FplTypeMismatch error
## 1.8.11
* Refactoring
  * Move evaluate method and related attributes from SemCheckIdentifiers to SemanticAnalyser
  * Simplification of affected method callers in the source code of different classes   
* Bugfixes
  * Some additional test cases to help localize false positives of FplWrongArguments, FplIdentifierNotDeclared and FplTypeMismatch errors
## 1.8.10
* Bugfix
  * Index error when trying to log FplTypeMismatch errors based on some inbuilt type from the AuxInbuiltTypes.py
  * Explicit initialization of the declared_type of nodes in the symbol table
  * Adjusted AuxRuldDependencies and ContextEntityWithCoord to reflect the FPL grammar fix version 1.1.9.
  * Fixed test cases related to ranges to reflect the FPL grammar fix version 1.1.9
## 1.8.9
* Bugfix
  * Matching generic types with objects corrected
  * Evaluation of 'self' with a qualified id corrected
  * Evaluation of variables with a qualified id corrected
* Feature
  * Initial implementation of the evaluate method in AuxSTQualified
  * Some additional syntax tree unit tests for qualified identifiers added
  * Some additional syntax tree unit tests for ranges and coordinates added
## 1.8.8
* Refactoring:
  * Saving code by using AuxEvaluationBlockFunctionalTerm in AuxSTDefinitionFunctionalTerm and AuxSTFunctionalTermInstance
  * Saving code by using AuxEvaluationBlockPredicate in AuxSTDefinitionPredicate and AuxSTPredicateInstance
  * Deriving AusSTPredicateWithArgs not from AuxSTBlock but instead from its base class AuxST, because AuxSTBlock is reserved to be a common base class of all FPL building blocks. AusSTPredicateWithArgs is not an FPL building block.
  * Renaming AuxSTBlock to AuxSTBuildingBlock to reflect the fact that it is the base class of all FPL building blocks. 
* Feature / Bugfix:
  * Implemented bounding variables inside quantor blocks, bugfixing related test cases
* Bugfix
  * Preventing re-evaluation of AuxSTPredicateWithArgs whose reference has been established to InbuiltUndefined
  * Adding variables declared in the outer scope of inner building blocks to their main distance to prevent Key index errors during the evaluation process.
## 1.8.7
* Bugfixes:
  * Duplicate dispatching of qualified_identifiers in SemCheckerAnalysis._check_uniqueness_identifiers method caused by incorrect looping variable.
  * Subnodes corollaries and proofs of theorem-like statements were wrongly skipped during the evaluation 
  * Available testcases for FplWrongArguments are now successful
  * Avoiding Circular Reference when evaluating predicates referring to themselves
  * Nodes get the correct representation instead of lists of possible overrides 
* Feature:
  * New error FplCircularReference with some related test cases
  * Initial implementation of checking if parent classes have compatible types to classes derived from them.
## 1.8.6
* Feature:
  * New class AuxSelfContainment
  * New class AuxParamsArgsMatcher
  * Initial type matching algorithm for arguments matching parameters
* Bugfixes:
  * Some missing FplWrongArguments recognitions fixed
## 1.8.5
* Refactoring:
  * Removing get_required_signature() and replacing string-based type recognition in evaluation methods by a AuxSTType-based recognition
* Feature:
  * New error FplVariableBound and some first related test cases
  * Initial implementation of the evaluate method of different symbol table node subtypes 
  * Default constructors inherit the position as the class declaration (affected expected test cases of symbol table adjusted accordingly)
  * Initial implementation of FplWrongArguments recognition
## 1.8.4
* Refactoring / Feature:
  * New class AuxEvaluation added
  * Some simple evaluations on the predicate level added.
  * New errors FplAxiomNotSatisfiable and FplTypeMismatch added.
## 1.8.3
* Refactoring:
  * Introducing the 'evaluate' concept - a method to be implemented by (almost) each of the members of the symbol table that will implement the full semantics of each FPL language construct. 
## 1.8.2
* Feature:
  * New error FplWrongArguments and some first related test cases (all will currently fail).
## 1.8.1
* Refactoring:
  * Preparations for implementing a check if a AuxSTPredicateWithArgs arguments correspond to any given available overrides
* Feature:
  * New class AuxInbuiltTypes providing standard implementations of inbuilt types
## 1.8.0
* Feature: 
  * Class inheritance of properties & semantical recognition of identifiers (still open: signature-conform "calling" of parent properties)
  * New semantical error introduced: FplTypeNotAllowed
  * Qualified identifiers extended to self and variables (qualified AuxSTPredicateWithArgs still open)
  * Some new unit tests
## 1.7.2
* Refactoring
  * Semantical analysis simplified
* Bugfixes: 
  * Populate global nodes after (and not during) the recursive syntax_analysis
  * Qualified identifiers were not correctly established for signatures containing one of the characters '[,*+]', causing false positives of some errors.
## 1.7.1
* Bugfixes:
  * The FplForbiddenOverride error was not recognized in all cases correctly.
  * The column position in the message of the FplForbiddenOverride and FplAmbiguousSignatures errors were not correct.
  * Messages of FplForbiddenOverride and FplAmbiguousSignatures adjusted, including test cases.
* Refactoring:
  * Common code of unit tests was centralized in UtilTestCase.py
## 1.7.0
* Features:
  * New semantical warning FplMissingProof (indicates that there is theorem-like statement, i.e. theorem, proposition, lemma or corollary without a corresponding proof)
  * New semantical error FplProvedConjecture (indicates a proof referencing to a conjecture)
  * New semantical error FplProofMissingTheoremLikeStatement (indicates a proof of a non-existing theorem-like statement)
  * New semantical error FplCorollaryMissingTheoremLikeStatement (indicates a corollary of a non-existing theorem-like statement)
  * New semantical error FplAmbiguousSignatures (indicates the use the same signatures with different building block types)
  * New semantical error FplForbiddenOverride (indicates a forbidden override of special types of building blocks like axioms, conjectures, theorem-like statements, and conjectures)
  * Respective tests added
* Bugfixes
  * Undo last ReferencingIdentifier simplifications since we need proofs of corollaries.
  * The global nodes of proofs and corollaries in test cases were wrong (test utilities updated)
* Refactoring
  * Checks related to identifiers moved to from fplsementicanalyzer.py to a separate new class SemCheckIdentifiers.py  
## 1.6.6
* Bugfixes:
  * The symbol table of proofs follows now the overall convention to list variable specifications before the block definition.
  * The variables declared in the theorem-like statement of the proof are now automatically part of the variable declarations of the corresponding proof. 
  * Sortkey of errors corrected to show syntax errors prior to semantic errors
## 1.6.5
* Refactoring:
  * Printing the symbol table moved from the interpreter class to the IdeModel class where it is printed together with the library.
  * Which is the main fpl file is now stored as an attribute in the IdeModel instead of being an attribute of some file in the loaded library.
* Bugfixes:
  * "Forgetting" which was the main fpl file when re-verifying the theory corrected. 
## 1.6.4
* Feature:
  * New semantical error FplTemplateMisused recognizing the (syntactically possible) misuse of variables named like templates (except the keyword "tpl") + related test cases.   
* Bugfixes:
  * False positives of FplUnusedVariable errors corrected when variables are declared in outer scopes but used in sub-nodes like constructors or properties.
  * Corrected highlighting of variables named like templates (now highlighted like types, not like variables).
* Refactoring:
  * Corrected naming for error_manager variables in different positions of code (instead of just "errors")
  * Error test cases can now print all errors found with verbose mode == True   
## 1.6.3
* Bugfixes:
  * The parsed position of more variables listed in one declaration is now more specific to the variable (instead of the whole list)  
  * Unused variables do not lead to the FplUnusedVariable error anymore if they were declared in the signature of an intrinsic definition. 
## 1.6.2
* Bugfix
  * The parsed position of PredicateIdentifiers was corrected in the symbol table + affected test cases were adjusted.
  * The parsed position of DefinitionPredicate was corrected in the symbol table + affected test cases were adjusted.
  * The parsed position of Signatures was corrected in the symbol table + affected test cases were adjusted.
* Refactoring
  * Printing during the parsing process in verbose mode is no more needed in general and was commented out to run tests faster.  
## 1.6.1
* Refactoring
  * New class FplErrorManager providing basic functionality for collecting FPL errors (replaces a list-based implementation)
## 1.6.0
* Feature:
  * FplIdentifierNotDeclared errors added to the semantical analysis + related unit tests
  * FplUnusedVariable errors added to the semantical analysis + related unit tests
  * FplMisspelledConstructor errors added to the semantical analysis + related unit tests
  * Test cases no more have to be specific when it comes to test a specific error. It suffices that the use case causes that error (among other possible errors). This simplifies the creation process of test cases as the FPL interpreter becomes more powerful in recognizing new error types.
* Bugfixes:
  * FplUndeclaredVariable was not at all working (undetected by unit tests). Now resolved + correct unit tests. 
  * Wording of error messages more standardized
  * FplMalformedGlobalId was not at all working (undetected by unit tests). Now resolved + correct unit tests.
  * FplMisspelledConstructor was not at all working (undetected by unit tests). Now resolved + correct unit tests.
* Refactoring:
  * SemAnalyser class deprecated (everything is now encapsulated in the interpreter.semantical_analysis() method)
## 1.5.2
* Bugfix:
  * The starting position of predicate definitions was shifted to the last parsed "predicate" keyword INSIDE the definition, not the position of the beginning of the definition.
  * Upgrade to the newest TatSu Version 5.8.0.
## 1.5.1
* Bugfix: 
  * Handling other errors except parsing and semantic errors in the error list
  * File name added to the error list of parsing errors. 
## 1.5.0
* Feature: Unloading an FPL file from the FPL interpreter's internal representation.
* Refactoring: fplerror in terms of correctly calling super() in constructors
* Minor bug-fixes
## 1.4.12
* Refactoring: Reading the library from the root theory is now part of the Utils class (and not part of the FPL interpreter).
## 1.4.11
* Feature: 
  * FplMalformedNamespace + test cases
* Refactoring:
  * Globals in the symbol table now contain references to the respective theory nodes in which they are defined, allowing referencing errors to respective FPL files in which they occur. 
  * All affected test cases adjusted accordingly
## 1.4.10
* Feature: 
  * FplIdentifierAlreadyDeclared + test cases
## 1.4.9
* Minor bugfixes: 
  * fplerror not found when importing poc.fplerror
  * string/int concatenation of error position in fplmessage
## 1.4.8
* Bugfixes for checking variable declarations and whether all variables are used in their scope:
  * AuxBlock contains standard methods to initialize and read declared and used variables of building blocks that might be overridden in derived classes by specific implementations.
  * Refactoring unnecessary implementations (removed) from AuxSTProof, AuxSTConstructor, AuxSTBlockWithSignature
  * Individual implementations overriding the standard ones in AuxSTClass, AuxSTConstructor, AuxSTInstance, AuxSTDefinitionFunctionalTerm, AuxSTDefinitionPredicate 
  * Calling the declared and used variables initializations of all blocks when populating globals in AuxSymbolTable
  * New methods initialize_scope and has_in_scope variable declarations (class AuxSTVarDec)  
* Bugfixes symbol table for cases when variables are used like predicates:
  * The outline of these nodes in the symbol table change from 'predicateWithArgs' to 'var'
  * Added missing id (with the variable name) in these nodes
  * Expected values in affected unit cases amended 
* Diagnose_id tests attached to the existing tests FplVariableDuplicateInVariableList, FplVariableAlreadyDeclared, and FplUndeclaredVariable
## 1.4.7
* The symbol table now supports:
  * loading multiply FPL files with the same namespace (i.e. allowing partial FPL code of a single mathematical theory spread across multiple FPL files),
  * recursive reloading of further theories referenced in theories that have already been loaded into the symbol table.
* New semantic error FplNamespaceNotFound including a unit test
* Every FPL error gets assigned a unique ID (diagnosis ID) that can be used in the error list when FPL code is interpreted.
## 1.4.6
* Reflected bug-fixed syntax highlighting of the patched IDE version 1.2.8.
* Changed the convention "line:column:position" in the *zfrom* and *zto* values in the symbol table to represent the start and end indices common in tk.Frame.
* Bug-fixed the *zfrom* values of AuxSTVariable in the symbol table.
* Adjusted the expected values for the affected symbol table unit tests. 
## 1.4.5
* Obfuscation tests added for axioms, classes, constructors, functional terms, inference rules, proofs, properties, statements and theorem-like building blocks
* Maximum recursion limit increased to 3500
* Bugfixes: 
  * "zfrom", "zto" values in AuxSTType corrected and refactored, relevant unit tests replaced.
  * "zfrom", "zto" values in AuxSTPredicate corrected and refactored, relevant unit tests replaced.
  * "zfrom", "zto" values in AuxSTRange corrected and refactored, relevant unit tests replaced.
  * "zfrom", "zto" values in AuxSTConstructor corrected and refactored, relevant unit tests replaced.
  * "checksum" error in syntax_analysis as a symptom of incompletely consumed parse_list at the Namespace rule corrected
## 1.4.4
* Bug fixes: 
  * Make subtrees for complex types explicit in the symbol table
  * Include argument tree nodes in the symbol table when types contain parameters
  * The syntax of FPL allows semantically incomplete functional terms (e.g. missing images). Enforce producing a correct symbol table (see bugfix ContexClassInstance.py).
* Utility poc/util/rr_converer.py run for updating the input for the Railroad Diagram Generator to reflect the current FPL grammar.
## 1.4.3
* Bug fixes: 
  * More robustness of the syntax analyzer using random derivations of FPL grammar, test cases include:
     * random predicate derivations
     * random types in variable declarations (both in a signature or in a block)
     * random types of classes
     * random types of properties
     * random types of images of functional terms
* Types in the symbol table are now listed separately (AuxSTType) and not inline because they can have complex own structures. 
* Corrected expected values of all relevant test use cases according to the above redesign
* Arguments of PredicateWithArguments summarized in a separate node AuxSTArgs 
* Coordinates of EntityWithCoords summarized in a separate node AuxSTCoords 
## 1.4.2
* Bugfix zfrom index, including all affected testcases 
* Bugfix def_type property of instances changed from (class / predicate / functional term) "declarations" to "instances"
* Identification of declared variables in different scopes
* Added checks for FplVariableAlreadyDeclared errors and corresponding tests
* Implemented ContextRevokeHeader and ContextRevoke
* Implemented zfrom and zto positions of two additional predicate types: preReferenced and arg_id
## 1.4.1
* Corrected misplaced localization node in the symbol table
* Node stack functionality in AuxISourceAnalyser discontinued
* Replaced AuxAstInfo objects by public attributes of the nodes to prepare the symbol table for being serializable
  * adjusted all related test cases
* Separated FplSourceTransformer from the FplInterpreter
* Discontinued tree-sitter conversion support
* Loading of more than one theory based on a root directory and the 'uses' clause.
## 1.4.0
* Symbol table functionality (cont.)
  * representation of premisses and conclusions in theorem-like statements
  * representation of predicates with variable arguments
  * order of bound variables according to the natural order in the source code (and not to the order of being parsed)
  * representation of localizations
  * representation of proofs
  * representation of definitions corrected (functional terms, classes, and predicates)
  * bug-fixes 
## 1.3.0
* Symbol table functionality (cont.)
  * representation and evaluation of predicates (initial)
    * compound predicates (and, or, xor, iif, impl, not)
    * variable predicates
  * Entity (self, @self, ...)
  * representation of statements (initial)
  * more tests
  * adjustments of the FPL interpreter according to FPL grammar changed to version 1.1.2
* Known issues: this version of the interpreter's syntax analysis will run into errors when you try to open, parse and interpret FPL theories from the poc.
## 1.2.4
* Symbol table functionality (cont.)
  * undeclared variables (initial)
  * more tests, some bug-fixes
  * adjustments of the FPL interpreter according to FPL grammar changed to version 1.1.1, in particular, ranges in types.
## 1.2.3
* Symbol table functionality (cont.)
  * bug-fix properties of classes, additional tests added
  * bug-fix multi-identifier alias for used namespaces, additional tests added
  * AuxRuleDependencies class added (autogenerated)
* Licence changed from 'GNU GP' to MIT
## 1.2.2
* Symbol table functionality (cont.)
  * types for building blocks of FPL (type_pattern) added
  * AuxBits.py added for handling type patterns
  * global Ids now include names that distinguish between different signatures (will allow overloading in FPL)
  * Signature interpretation class added
  * expected values for some test cases adjusted
* simplified test code and test classes
* AuxInterpretation __repr__() added
## 1.2.1
* Class AuxOutline was removed. It mixed up the symbols used for the outline of the symbol table (now in the class AuxSymbolTable) with the symbols used for contexts (now in the class AuxContext). 
* Symbol table functionality variable declarations (cont.)
* New tests added
* parameterized tests
## 1.2.0
* Symbol table functionality (cont.)
  * variable declarations
  * used types (initial)
  * first draft representation of (complex) types
* Bugfix relative folders for importing package files
* Bugfix instance namespaces for variables of auxiliary classes
* Separation of syntax transforming (minify/prettify) and syntax analysis
* Redesign and simplification of the FPLSyntaxAnalyzer class while moving context handling to individual classes named Contex<Something>
## 1.1.1
* Basic symbol table functionality (cont.) 
  * identifiers of properties of classes and functional terms
  * identifiers of images of functional terms
  * identifiers of theorems, propositions, lemmas, corollaries, and conjunctions 
* Refactoring 
* Handling of parentheses contexts
* Some additional unit tests
* Known issues: 
  * No overloading of name declarations 
  * handling of parentheses in nested signatures
## 1.1.0
* Basic symbol table functionality added
  * namespace identifiers 
  * class names and types 
  * axiom names 
  * names of functional terms
  * names of predicates
* Adjusted fplinterpreter to handle more than one theory
* Some additional unit tests
* Known issues: No overloading of name declarations implemented yet
## 1.0.2
* Minify and Prettify functionality removed from interpreter into a separate class
## 1.0.1
* Exceptions added 
* Some basic interpretations added
## 1.0.0 
Initial interpreter
