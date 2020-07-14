# fpl
fpl is a project to create FPL (the "Formal Proving Language") - a universal, 
human-readable, easy to learn and read formal language for writing 
mathematical definitions, theorems, and proofs 
independently from any natural language. 

These is the main goal of the project and you are invited to collaborate on
conception and design.

FPL is not (!)
* yet another automated prove assistant 
* yet another automated theorem proving tool.

In fact, it is not a tool at all! It is more a specification for a 
human-readable language that can be used by mathematicians all over the world
regardless their origin and native language so that a theory written in FPL
can be read and understood by everyone who also knows FPL.

At the same time, FPL should be formal enough to enable programmers to 
implement FPL tools that are able to:
* parse and translate code written in FPL into an arbitrary human 
local language,
* verify, if code written in FPL is logically
consistent (i.e. without contradictions), 
* help to find a proof for a theorem written in FPL, given a theory written 
in FPL, i.e. other theorems, definitions, and axioms written in FPL, and  
* generate theories based on axioms written in FPL.

The FPL specification follows some seemingly contradicting principles:

### Principle 1: Readability

Code written in FPL should be not only human-readable but also catchy, memorable, and easy to learn so that FPL can be learned even by non-programmers.

### Principle 2: Richness of Notation

The syntax of FPL should be inspired by modern mathematical notation while preserving the readability principle.

### Principle 3: Axiomatic Method 

FPL should be based on the axiomatic method i.e. every theory written in FPL should start with some definitions of mathematical concepts, axioms about these concepts asserting that they are true, and deriving new theorems based on given logical rules of inference while interpreting them also as true when they are derivable using the rules of inference.

### Principle 4: Theory Independence

While using the axiomatic method, FPL should not stick to a pre-defined set of axioms and rules of inference. Its meta syntax and semantics should allow developing any theory using the axiomatic method.

### Principle 5: Theory Standardization

The FPL framework should encourage using some standard sets of axioms and rules of inference that were written in FPL to promote standard notation for widely agreed mathematical concepts and a common sense of what is currently perceived as a consistent mathematical theory. To facilitate using these standards, the FPL syntax should establish an explicit notation (or namespaces) for these standards, allowing to easily distinguish between a standard and non-standard FPL notation for widely agreed mathematical concepts 

### Principle 6: Formalism

The syntax and semantics of FPL should enable the creation of automated aids and tools.
   

   
 