# FPL Proof of Concept

This is an experimental implementation (still work-in-progress) of the   
["FPL High-level Design"](https://www.bookofproofs.org/FPLHighLevelDesign.pdf). The implementation consists of 
* a [grammar](https://github.com/bookofproofs/fpl/tree/master/grammar/),
* a parser (based on the [TatSu package](https://tatsu.readthedocs.io/en/stable), only in-memory, no python file required),
* an [interpreter](https://github.com/bookofproofs/fpl/tree/master/poc/fplinterpreter.py) (initial, still work-in-progress), and
* [FPL demo theories ](https://github.com/bookofproofs/fpl/tree/master/poc/theories/)

### Getting Started
#### Installation process:
Install the package TatSu (tested with the 5.5.0 stable version) in your environment. Use python 3.8 (at least). 

#### Software dependencies
The software uses the packages TatSu (parser) and tkinter (IDE only).
Also, the following packages should be installed: anytree, parameterized.

#### Latest releases
see [CHANGES.md](https://github.com/bookofproofs/fpl/blob/master/poc/CHANGES.md)

#### API references
TBD

### Build and Test
To see everything is working, you can start the demo.py file. It parses some demo theories and minifies their code, 
or lists the parser or interpreter errors.

If you want to work to test the fpl parser and interpreter, we recommend using the 
[FPLIDE](https://github.com/bookofproofs/fpl/tree/master/ide), a custom integrated development environment for FPL. 
Just run fplide.py and open a file in the poc/theories folder.

### Contribute
Your contributions are welcome! The work on the proof of concept includes, but is not limited to, developing an 
FPL interpreter. The corresponding [project](https://github.com/bookofproofs/fpl/projects/1/) describes the tasks and 
their details.

### Known Issues
* There are only a few semantical errors implemented so far.
