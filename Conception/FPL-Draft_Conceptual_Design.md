# Draft Conceptual Design of FPL

## 1 Introduction

### 1.1 What is FPL?

FPL, the Formal Proving Language, is a planned specification for an artificial language 
that is going to serve as a universal language to formulate
mathematical definitions, theorems, and proofs independently from 
local natural languages. 

While English is currently the de facto standard natural language for
mathematical publications, FPL should further facilitate the dialog between 
mathematicians all over the world, providing a standard notation, a standard 
degree of details needed to write mathematical proofs, and a standard degree of 
details needed to formulate mathematical definitions, axioms, and theorems. 

At the same time, as a formal language, FPL is going to facilitate creating
automated tools serving different additional purposes, in particular:
* parse and translate code written in FPL into an arbitrary human 
local language (as a bridge between FPL, which is a formal language and 
any natural language),
* verify, if a code written in FPL (a mathematical theory) is logically
consistent (i.e. without contradictions), 
* help to find a proof for a theorem, given a theory written 
in FPL,   
* automatically generate theories based on axioms written in FPL,
to mention only some possible applications.

### 1.2 Why FPL?

FPL is not yet another automated prove assistant or yet another automated theorem proving tool. It attempts to set a standard for writing mathematical definitions, theorems, and proofs while encouraging programming automated tools based on FPL. 

The syntax of existing formal systems and automated tools is computer-friendly, i.e. primarily designed to be compiled and processed by automated tools, not by humans. Therefore, the language used by these tools is hard to read and to understand, even by mathematicians. The communities using these tools are small communities of specialists. Despite that, such automated tools provide many advantages. In particular, they help to write correct mathematical proofs and help to avoid errors. 

Therefore, it would be great if there would be tools using a formal language that is readable, catchy, and easy to learn, even for non-programmers. Such Tools could be (ideally) also used for educational purposes to teach mathematics. 

FPL wants to close to this gap. FPL is going to have a human-friendly syntax while being formal enough to develop tools based on it that can assist in writing and developing correct mathematical theories. In particular, FPL should be easy enough to be used in mathematical education. 

Thus, FPL primarily aims at being human-readable and only then at being compiled and processed by computers. By this human-centric approach, FPL should enjoy a better user acceptance, while providing comparable advantages that automated formal language tools provide.
### 1.3 About this Document

This document provides a main draft conceptual design of FPL. 
It may be complemented by additional "DSDDs" (Detailed Conceptual Design 
Documents) for specific areas requiring more specification details. 

This document is open source and published under the CC-BY-4.0 license. 


### 1.4 How to Use This Document

As it is the central draft conceptual document of FPL in its respective 
version at Github, we strongly encourage you to 
use it as a reference for your own, FPL-related projects.

The document is written in markdown. Whenever mathematical formulas are
used in this document, LaTeX notation will be used, 
enclosed by $..$ for inline formulas and by $$..$$ for 
centered formulas. 

## 2 Design Principles of FPL 

To be successful, the FPL specification has to follow some seemingly contradicting principles:

### 2.1 Principle 1: Readability

Code written in FPL should be not only human-readable but also catchy, 
memorable, and easy to learn so that FPL can be learned even by 
non-programmers.

_CLARIFICATION_ 

This principle will be the most difficult to accomplish since a formal 
language can be human-readable but not always easy to learn and memorable. 
A memorable notation and simplicity of syntactical rules will be key for user acceptance.

### 2.2 Principle 2: Richness of Notation

The syntax of FPL should be inspired by modern mathematical notation while 
preserving the readability principle.

_CLARIFICATION_ 

The richness of modern mathematical notation imposes at least two challenges for a specification
of a formal language like FPL: one is its catchy readability, another it's ambiguity. 

The Readability Challenge 
* Modern mathematical notation is very rich. It allows, among others,  indexing of variables (e.g, $x_i,$ $x_{i_j}$, $x^{(k)}_j$, etc.)
enumerations (e.g. $a_1,\ldots,a_n$), matrices (e.g. $\pmatrix{a_{11}&a_{12}\\a_{21}&a_{22}}$), 
short notation for special operation like summation $\sum,$, products $\prod$, 
integrals $\int$, composition of functions (e.g. $f(g(f(x))))$), and a lot of other conventions.  
* At the same time, the LaTeX examples given above demonstrate that coding this notation
is by far not as readable and catchy as its typeset result. Observe that richness of
notation and readability are not necessarily conflicting principles.
If you consider the typeset result of a LaTeX code or mathematical notes
written by hand, using a pencil and a sheet of paper, both are possible
at once: a rich _and_ a catchy notation. A rich notation problem becomes less catchy if
we try to code it in a computer-readable format, like LaTeX or a related formal system. 


Because FPL is intended to be a formal language, its specification has
to resolve the conflict between a notation that is catchy for humans and a notation that is
computer-readable, while preserving the richness of notation. The FPL specification will have to make some concessions in both directions, i.e. keep 
the notation as simple as possible to allow a catchy result, while allowing 
complicated constructs to make it easy for computers to 
parse the code.

The Ambiguity Challenge

* Another feature of modern mathematical notation is its intrinsic ambiguity. There are many examples: 
  * The symbol "1" can mean different things: in some contexts, it would be the natural number 1, 
in some other contexts, the real number 1, or even the complex number 1. It can even mean no number at all, 
when it is used to denote the neutral element of multiplication in the ring of square matrices, 
together with matrix addition and matrix multiplication.
  * The symbols +,* could mean the addition and the multiplication of numbers, but also operations on other objects like 
  vectors or congruence classes.  
  * In some mathematical contexts, it is necessary to use some other symbol for an operand to avoid 
  confusion with other symbols that are used in the same context meaning different things.    
  * Moreover, any numerical constant could be written in decimal, octal, binary,
or other systems but still mean the same real number. 
  * Any irrational number (like the constant 
$Pi=3.1415\ldots$) cannot be represented in its whole precision. Thus, an agreed notation 
(the Greek capital Pi) is used to denote such constants. But in other contexts, the same Greek
capital $Pi$ could mean any variable or element of any arbitrary set or class. 
Things become even more complicated when we try to use these symbols as indices of variables, e.g. $x_\Pi.$ 

A feature of every formal language should be the lack of ambiguities. If a compiler encounters the symbol 1, it should collect
enough information from the context to interpret the symbol in a manner it was meant by the author
of the FPL code. On the other hand, avoiding ambiguities makes the syntax of many formal languages
overloaded so that their readability suffers a lot.   

So, how should FPL deal with notational ambiguities, without overloading the syntax? Again, the FPL 
specification will have to make some concessions in both directions, i.e. keep the notation as unambiguous 
as possible, while allowing context-based re-interpretation of the same symbols.

### 2.3 Principle 3: Axiomatic Method 

FPL should be based on the axiomatic method i.e. every theory written in FPL
should start with some definitions of mathematical concepts, axioms about these concepts 
asserting that they are true, and deriving new theorems based on given logical 
rules of inference while interpreting them also as true when they are derivable using the 
rules of inference.

_CLARIFICATION_ 

While the rules of inference have to be declared in FPL, to keep things simple, 
the semantics (i.e. interpretation) of any theory that was formulated in FPL 
should not have to be explicitly declared. 

Thus, theories written in FPL simplify things by asserting that:
* only two truth values are possible (true, false) but nothing in between 
(no "fuzzy logic" interpretations are allowed),
* and if a theorem is derivable from true axioms using the declared rules of inference, then it 
is automatically valid (i.e. true).

This approach is similar to the approach used in mathematics, in which axioms are variable but both,
the rules of inference and interpretation, are not always explicitly apparent.
The rules of inference are not explicitly given since mathematics is not formulated in
a formal language. Interpretation is also not explicitly defined. There is a common sense 
that if something is "logically correctly derived from axioms" then it "is also true". 
However, we should be aware that this is only one of many different possible interpretations and thus
the theories of contemporary mathematics are not the only possible ones. They might even be
false under different interpretations. 

### 2.4 Principle 4: Theory Independence

While using the axiomatic method, FPL should not stick to a pre-defined set of axioms 
and rules of inference. Its meta syntax and semantics should allow developing any theory using
the axiomatic method.

_CLARIFICATION_ 

FPL should allow formulating any new theory starting with a new set of axioms
and rules of interference. This way, the scalability and extensibility of FPL should be
ensured to anticipate future developments in mathematics and its evolution as a science.

### 2.5 Principle 5: Theory Standardization and Extensibility

The FPL framework should encourage using some standard sets of axioms and rules of inference 
that were written in FPL to promote standard notation for widely agreed mathematical concepts 
and a common sense of what is currently perceived as a consistent mathematical theory. 
To facilitate using these standards, the FPL syntax should establish an explicit notation 
(or namespaces) for these standards, allowing to easily distinguish between 
a standard and non-standard FPL notation for widely agreed mathematical concepts. 

_CLARIFICATION_ 

The "FPL framework", in comparison to "FPL" itself as a pure language specification,
should provide a public, open and freely accessible repository of pre-formulated
theories in FPL with commonly agreed axioms and rules of inference, as well as notation 
that can be re-used for further purposes.

The usage of such pre-formulated theories can be compared to "including" the code of these
theories as modules of own theories.

If a notation of an extended theory based on a standard module becomes commonly accepted
by the community, the repository authorities may decide whether to add the extended theory
as another module that can be re-used by others as a standard module.

The distinction between standard and non-standard modules of FPL should be made explicit, using
reserved namespaces for standard modules.  

### 2.6 Principle 6: Formalism

The syntax and semantics of FPL should enable the creation of automated aids and tools.

_CLARIFICATION_ 

While human readability remains important (see Principle 1), FPL should be
formal enough to facilitate a rigid and unambiguous notation. 

The syntax of FPL should be formal enough to develop 
automated tools capable to verify the correctness of FPL theories.
Integrated Development Environments (IDEs) for FPL should assist users in writing 
correct mathematical proofs and in formulating mathematical definitions 
that meet modern standards. 

Also, the syntax should make it possible to program automated tools translating 
a theory written in FPL into a given natural human language (possibly including LaTeX notation
for mathematical formulae). With this respect, FPL should provide a means to formulate the 
same content independently from a given natural human language, while still enabling people
to read the content even if they do not use or know FPL. 

## 3 Approach for the Specification

The main result of this specification is a syntax of FPL in the Extended Backus Naur Form (EBNF).

The above principles show a high complexity of reaching all of them at once by a language. 
The specification has to be developed using an agile method to be able to adapt to future requirements. 
The principles define high-level requirements that will be complemented by _additional requirements_
 of the language resulting from the following iterative agile process:
 
1. (Re-)-Defining the syntax of FPL in a current version.
2. (Re-)-Creating a parser for FPL for the current FPL syntax
3. Enhancing and testing a repository of test cases using the current FPL parser
4. Assessing, to which extend the 6 principles are fulfilled 
5. Assessing, if the _"Additional Requirements"_ are fulfilled
6. Enhancing, refining the _"Additional Requirements"_, if required
7. Repeating the agile process until all 6 principles have been met according to a pre-defined 
quality gate and until all _"Additional Requirements"_ are fulfilled.

Ad Step 1.

The definition of the syntax should be done in EBNF or a variation of it. It makes
sense to use a dialect of EBNF that can be used as the input for a tool generating a parser
 out of the grammar. Such a tool is, for instance, https://tatsu.readthedocs.io/en/stable/.
 
Ad Step 2.

If the parser can be recreated, the EBNF code is formally correct. Otherwise, the EBNF has to 
be corrected until the parser can be recreated.

Ad Step 3. 

A repository of test cases is required for the agile process. A test case is a file containing code 
written in FPL (obviously with the file extension "*.fpl"). A test case addresses features of the 
FPL language that it has to fulfill. These features have to be defined in a list of
_Additional Requirements_.

Some of the features might address not the syntax but also the semantics of the FPL language. 
Therefore, apart from the parser, also a compiler of FPL has to be implemented that addresses 
all requirements regarding the semantics. This compiler plays a role in step 5.

Ad Step 4. 

The assessment of how FPL reaches the 6 pre-defined principles can be made only qualitatively. This will be
accomplished using a qualitative ordinal scale. An ordinal scale has the advantage that it is possible
to assess what's is more important and significant, but the exact differences between each ordinal 
are not known. 

A possible scale for assessing reaching each of the principles can be

1. Not fulfilled
2. Somewhat Unfulfilled
3. Neutral
4. Somewhat Fulfilled
5. Fulfilled

Ad Step 5. 

The _Additional Requirements_ are a list of additional features FPL has to fulfill to 
meet the 6 pre-defined principles to a satisfactory degree ("quality gate"). 
In each iteration, in step 5 the _Additional Requirements_ from the but-last iteration are used.


Ad Step 6.

Unlike the pre-defined principles, the _Additional Requirements_ can be changed,
enhanced, or adjusted in each iteration. Only 
those _Additional Requirements_ should be added that help to meet the 6 pre-defined principles.

Initially, no _Additional Requirements_ are defined. It should be documented, 
at which iteration an additional requirement was added and how meeting this requirement
helps to meet the 6 pre-defined principles.

Ad Step 6.

A quality gate has to be defined to decide whether further repetitions of the 
agile process are required to improve the FPL specification. As of now, the quality gate  
consists of the following criteria:

1. An EBNF of the FPL syntax exists.
2. There is a parser capable to parse arbitrary FPL code, including a compiler.
3. Both, the parser and the compiler meet the _Additional Requirements_. In particular, 
the compiler meets the semantics of FPL that are defined in the _Additional Requirements_.
4. The parser and compiler correctly deal with all test cases in the test repository. 
5. All principles are met to at least the degree 4. 

## 4 Additional Requirements

to be created

## 5 Iterations of the Process

to be documented 

