# Changes in the FPL Parser and Interpreter
## 1.0.0 
Initial interpreter
## 1.0.1
* Exceptions added 
* Some basic intepretations added
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
* some additional unit tests
* Known issues: No overloading of name declarations implemented yet