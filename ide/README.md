# FPLIDE
### The Formal Proving Language Integrated Development Environment

The FPLIDE is a small IDE for working with *.fpl files. It integrates the current versions of the FPL parser and the FPL interpreter. Every open FPL is highlighted, parsed, and interpreted according to its syntax tree. The error list and highlighting change dynamically with the user input. Double-clicking on errors or syntax rules in the syntax tree will position the cursor in the file correspondingly.   

### Known Issues
* The FPL parser does not support error recovery. Proper syntax highlighting and listing semantical errors will work until the first syntax error arises.
* There are only a few semantical errors implemented so far.
* For performance purposes, the IDE does not display an updated syntax tree on the fly as you type. You have to refresh it by demand.

