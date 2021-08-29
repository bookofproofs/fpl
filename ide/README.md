# FPLIDE
### The Formal Proving Language Integrated Development Environment

The FPLIDE is a small IDE for working with *.fpl files. It integrates the current versions of the FPL parser and the FPL interpreter. Every open FPL is highlighted, parsed, and interpreted according to its syntax tree. The error list and highlighting change dynamically with the user input. Double-clicking on errors or syntax rules in the syntax tree will position the cursor in the file correspondingly.   

### Getting Started
#### Installation process:
Install TatSu 5.6.1 (stable) in your environment. Use python (at least 3.8).
#### Software dependencies
The software uses the packages TatSu and tkinter. 
#### Latest releases
see [CHANGES.md](https://github.com/bookofproofs/fpl/blob/master/ide/CHANGES.md)
#### API references
TBD

### Build and Test
Run fplide.py and open a file in the poc/theories folder.

### Contribute
Your contributions are welcome! FPLIDE is based on tkinter. Please focus on adding new practical functions, 
improving user experience, adding unit tests, or bug-fixing. 

### Known Issues
* The FPL parser does not support error recovery. Proper syntax highlighting and listing semantical errors will work until the first syntax error arises.
* There are only a few semantical errors implemented so far.
* For performance purposes, the IDE does not support highlighting and updated syntax tree on the fly as you type. You have to refresh them by demand.

