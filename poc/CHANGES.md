# Changes in the FPL Parser and Interpreter
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
* Loading of more than one theory based on a root directory and the uses clause.
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
* Licence changed from GNU General Public to MIT
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
