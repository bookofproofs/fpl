# Changes in the FPL Parser and Interpreter
## 1.0.0 
Initial interpreter
## 1.0.1
* Exceptions added 
* Some basic interpretations added
## 1.0.2
* Minify and Prettify functionality removed from interpreter into a separate class
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
## 1.2.0
* Symbol table functionality (cont.)
  * variable declarations
  * used types (initial)
  * first draft representation of (complex) types
* Bugfix relative folders for importing package files
* Bugfix instance namespaces for variables of auxiliary classes
* Separation of syntax transforming (minify/prettify) and syntax analysis
* Redesign and simplification of the FPLSourceAnalyser class while moving context handling to individual classes named Contex<Something>
## 1.2.1
* Class AuxOutline was removed. It mixed up the symbols used for the outline of the symbol table (now in the class AuxSymbolTable) with the symbols used for contexts (now in the class AuxContext). 
* Symbol table functionality variable declarations (cont.)
* New tests added
* paremetrised tests