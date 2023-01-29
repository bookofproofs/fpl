# 1 Introduction

## 1.1 What is FPL?

FPL, the Formal Proving Language, is a specification for an artificial language 
that is going to serve as a universal language to formulate
mathematical definitions, theorems, and proofs independently of 
local natural languages. 

Watch the video:

[![Watch the video](https://img.youtube.com/vi/ROCNCDRiBp0/0.jpg)](https://www.youtube.com/watch?v=ROCNCDRiBp0)

While English is currently the de facto standard natural language for
mathematical publications, FPL should further facilitate the dialog between 
mathematicians worldwide, providing a standard for notation, and the  
degree of details of mathematical proofs, definitions, axioms, and theorems. 

At the same time, as a formal language, FPL aims to facilitate 
the automation of:
* parsing and translating the code written in FPL into an arbitrary human 
local language (as a bridge between FPL, which is a formal language and 
any natural language),
* verifying, if a code written in FPL (a mathematical theory) is logically
consistent (i.e. without contradictions), 
* helping to find a proof for a theorem, given a theory written 
in FPL,   
* generating theories based on axioms written in FPL,

to mention only some possible applications.

## 1.2 Why FPL?

FPL is not yet another automated proof assistant or yet another automated theorem proving tool. It attempts to set a standard for writing mathematical definitions, theorems, and proofs while encouraging automated programming tools based on FPL. 

The syntax of existing formal systems and automated tools is computer-friendly, i.e., primarily designed to be interpreted by computers, not humans. Therefore, the language used by these tools is hard to read and to understand, even by mathematicians. The communities using these tools are small communities of specialists. Despite that, such automated tools provide many advantages. In particular, they help to write correct mathematical proofs and help to avoid errors. 

Therefore, it would be great to use a formal language that is readable, catchy, and easy to learn, even for non-programmers. Such tools could be (ideally) also used for educational purposes to teach mathematics. 

FPL wants to close this gap. FPL will have a human-friendly syntax while being formal enough to develop tools based on it that can assist in writing and developing correct mathematical theories. In particular, FPL should be easy enough to be used in mathematical education. 

Thus, FPL primarily aims at being human-readable and only then at being compiled and processed by computers. FPL should enjoy better user acceptance by this human-centric approach while providing comparable advantages that automated formal language tools provide.

## 1.3 Design Principles of FPL

The FPL specification has to follow some seemingly contradicting principles:

### 1.3.1 Principle 1: Readability

> "Code written in FPL should be not only human-readable but also catchy, memorable, and easy to learn so that FPL can be learned even by non-programmers."

This principle will be difficult to accomplish since a formal language can be human-readable but not always easy to learn and memorable. A memorable notation and simplicity of syntactical rules will be key for user acceptance.

### 1.3.2 Principle 2: Richness of Notation

> "The syntax of FPL should be inspired by modern mathematical notation while preserving the readability principle."

The richness of modern mathematical notation imposes at least two challenges for a formal language specification like FPL: one is its catchy readability, another it's ambiguity. 

#### The Readability Challenge 

* Modern mathematical notation is very rich (we use here LaTeX notation):
   * indexing of variables (e.g, `$x_i,$` `$x_{i_j}$`, `$x^{(k)}_j$`, etc.) 
   * enumerations (e.g. `$a_1,\ldots,a_n$`)
   * matrices (e.g. `$\pmatrix{a_{11}&a_{12}\\a_{21}&a_{22}}$`) 
   * short notation for special operations like summation `$\sum,$`, products `$\prod$`, integrals `$\int$`, composition of functions `$f(g(f(x))))$`,
   * and a lot of other notational conventions.  
* At the same time, the LaTeX examples given above demonstrate that coding this notation is by far not as readable and catchy as its typeset result. Observe that richness of notation and readability are not necessarily conflicting principles. If you consider the typeset result of a LaTeX code or mathematical notes written by hand, using a pencil and a sheet of paper, both are possible at once: a rich _and_ a catchy notation. A rich notation becomes less catchy if we try to code it in a computer-readable format, like LaTeX or a related formal system. 

Because FPL is intended to be a formal language, its specification has to resolve the conflict between a notation that is catchy for humans and a computer-readable notation while preserving the richness of notation. Consequently, the FPL specification will have to make some concessions in both directions, i.e., keep the notation as simple as possible to allow a catchy result while allowing complicated constructs to make it easy for computers to parse the code.

#### The Ambiguity Challenge

* Another feature of modern mathematical notation is its intrinsic ambiguity. There are many examples: 
   * The symbol "1" can mean different things: in some contexts, it would be the natural number `$1$`, in some other contexts, the real number `$1$`, or even the complex number `$1$`. It can even mean no number when used to denote the neutral element of multiplication in the ring of square matrices, together with matrix addition and matrix multiplication.
   * The symbols "`$+$`", "`$\cdot$`" could mean the addition and the multiplication of numbers, but also operations on other objects, e.g., vectors or congruence classes. If FPL would be used to write a theory introducing the addition and the multiplication, should it also be possible to re-define such symbols?
   * In some mathematical contexts, it is necessary to use some other symbol for an operand to avoid confusion with other symbols that are used in the same context meaning different things.  
   * Moreover, any numerical constant could be written in decimal, octal, binary, or other systems but still mean the same real number. 
   * We cannot represent any irrational number (like the constant `$\Pi=3.1415\ldots$`) in its whole precision. Thus, an agreed notation (the Greek capital `$\Pi$`) is used to denote such constants. But in other contexts, the same Greek capital `$\Pi$` could mean any variable or element of any arbitrary set or class. Things become even more complicated when we try to use these symbols as indices of variables, e.g., `$A_\Pi.$` 

A feature of every formal language should be the lack of ambiguities. For example, if a compiler encounters the symbol "1", it should collect enough information from the context to interpret the symbol in a manner meant by the author of the FPL code. On the other hand, avoiding ambiguities makes the syntax of many formal languages overloaded so that their readability suffers a lot.   

So, how should FPL deal with notational ambiguities without overloading the syntax? Again, the FPL specification will have to make some concessions in both directions, i.e., keep the notation as unambiguous as possible while allowing context-based re-interpretation of the same symbols.

### 1.3.3 Principle 3: Axiomatic Method 

> "FPL should incorporate the axiomatic method. Every theory written in FPL should start with definitions of mathematical concepts, axioms about these concepts asserting that they are true, and deriving new theorems based on these axioms and logical inference rules."

While the rules of inference have to be declared in FPL, to keep things simple, the semantics (i.e., interpretation) of any theory written in FPL should not have to be explicitly declared. 

Thus, theories written in FPL simplify things by asserting that:
* Only two truth values are possible (true, false) but nothing in between (no "fuzzy logic" interpretations are allowed).
* If a theorem is derivable from true axioms using the declared rules of inference, it is automatically valid (i.e., true).

This approach is similar to the approach used in mathematics, in which axioms are variable, but both, the rules of inference and interpretation, are not always explicitly apparent. The rules of inference are not explicitly given since mathematics is not formulated in a formal language. Interpretation is also not explicitly defined. Common sense is that if something is "logically correctly derived from axioms," then it "is also true". However, we should be aware that this is only one of many different possible interpretations, and thus the theories of contemporary mathematics are not the only possible ones. They might even be false under different interpretations. 

### 1.3.4 Principle 4: Theory Independence

> "While using the axiomatic method, FPL should not stick to a pre-defined set of axioms and rules of inference. Instead, its meta syntax and semantics should allow developing any theory using the axiomatic method."

FPL should allow formulating any new theory starting with a new set of axioms and rules of interference. This way, we should ensure the scalability and extensibility of FPL to anticipate future developments in mathematics and its evolution as a science.

### 1.3.5 Principle 5: Theory Standardization and Extensibility

> "The FPL framework should encourage using some standard set of axioms and inference rules written in FPL to promote normative notation for widely agreed mathematical concepts and a shared sense of mathematical theories. In addition, the FPL syntax should establish an explicit notation and namespaces for these theories to distinguish and re-use widely agreed mathematical concepts." 

The "FPL framework", in comparison to "FPL" itself as a pure language specification, should provide a public, open, and freely accessible repository of pre-formulated theories in FPL with commonly agreed axioms and rules of inference, as well as notation that can be re-used for further purposes.

We can compare using pre-formulated theories with "including" the code of these theories as modules of our theories.

Suppose a notation of an extended theory based on a standard module becomes commonly accepted by the community. In that case, the repository authorities may decide whether to add the extended theory as another module that others can re-use as a standard module.

The distinction between standard and non-standard modules of FPL should be made explicit, using reserved namespaces for standard modules.  

### 1.3.6 Principle 6: Formalism

> "The syntax and semantics of FPL should enable the creation of automated aids and tools."

While human readability remains important (see Principle 1), FPL should be formal enough to facilitate a rigid and unambiguous notation. 

The syntax of FPL should be formal enough to develop automated tools capable of verifying the correctness of FPL theories. In addition, integrated Development Environments (IDEs) for FPL should assist users in writing correct mathematical proofs and formulate mathematical definitions that meet modern standards. 

Also, the syntax should make it possible to program automated tools translating a theory that we formulated in FPL into a given natural human language (possibly including LaTeX notation for mathematical formulae). With this respect, FPL should provide a means to formulate the same content independently from a given natural human language while still enabling people to read the content even if they do not use or know FPL. 

# 2 High-Level Conceptual Design

The project to develop FPL started June 14, 2020, as described in at [https://www.bookofproofs.org/branches/fpl-formal-proving-language/](https://www.bookofproofs.org/branches/fpl-formal-proving-language/).
Originally, developing the specification was planned as a collaborative project. Unfortunately, and probably due to the pandemic,
no community formed to work on it. Meanwhile, I could work on the project I initiated on my own. 
I identified the following High-Level Requirements for the FPL language:

| No.        | Requirement for FPL         | Level  |
| :-------------: |-------------| :-----:|
|1 |Express proof-based mathematics (PBM) only, nothing else.|MUST|
|2 |Support a clear separation of the concepts of truth and accuracy.|MUST|
|3 |Express PBM in a structured code to distinguish it from text passages written in prose.|MUST|
|4 |Support eight building blocks of PBM: definitions, theorems, propositions, lemmas, corollaries, axioms, proofs, and conjectures.|MUST|
|5 |Allow embedding FPL code into surrounding text that might contain non-PBM contents.|MUST|
|6 |Support localization|SHOULD|
|7 |Allow distinguishing four theorem-like building blocks: theorems, propositions, lemmas, and corollaries.|SHOULD|
|8 |Allow zero to many proofs of theorem-like building blocks and distinguish them syntactically from unproven conjectures.|MUST|
|9 |Disambiguate FPL code on a syntactical level using appropriate parentheses rules.|MUST|
|10 |Allow only deterministic interpreters to disambiguate FPL code on a semantical level.|MUST|
|11 |Incorporate the syntax of predicate logic (at least PL2).|MUST|
|12 |Allow referring to (unproven) conjectures in mathematical proofs and interpret such proofs accordingly.|MUST|
|13 |Support nesting and linking different logical steps and proofs into more complex ones.|MUST|
|14 |Use definitions as a meta-language to introduce new syntax and new domains of discourses allowing to interpret the formulas.|MUST|
|15 |Definitions introduce new types that can be used to declare FPL variables.|MUST|
|16 |Support for asserting and checking a type of a variable (`is` operator)|MUST|
|17 |Support flexible notation while defining new predicates, functional terms, or mathematical objects.|MUST|
|18 |Allow a free configuration of axioms and inference rules.|MUST|
|19 |Look&feel of notation, possibly similar modern notation. Ideally, exploit the possibilities of LaTeX.|SHOULD| 
|20 |Accept different levels of detail in mathematical proofs. If requested, provide additional details for validated proofs.|SHOULD|
|21 |Independence from foundations: No built-in axiomatic system of PBM in the syntax of FPL.|MUST|
|22 |Support both intuitionistic and non-intuitionistic arguments and mathematical objects.|SHOULD|
|23|Support definitions with compound parameters having implicit properties.|MUST|
|24|Support for relative definitions|MUST|
|25|Support for intrinsic definitions|MUST|
|26|Syntax independent from notation|MUST|
|27|Allow ranges of variables, including *countable* or *uncountable*, *ordered* or *unordered*, *finite*, or *infinite*.|SHOULD|
|28|Support inheritance and overriding of properties of parent classes when defining new *types*.|MUST|
|29|Determining the type (`is` operator) reflects the inheritance tree.|MUST|
|30|Stating axioms inside a definition as mandatory properties or as separate building blocks.|SHOULD|
|31|Support of definitions of functional terms|MUST|
|32|Support of definitions of predicates|MUST|
|33|Clear scope of variables in which they are declared.|MUST|
|34|Support to declare variables in the defined types, including support for at least PL2|MUST|
|35|Support assignment of values or expressions to variables|MUST|
|36|Support to delegate the interpretation of intrinsic definitions|MUST|
|37|FPL to allow identification by providing means of casting different data types to each other.|SHOULD|
|38|Allow recursive linguistic constructs|MUST|
|39|Allow loops|MUST|
|40|Allow self-reference in definitions.|MUST|
|41|Support generic types.|MUST| 
|42|Check the self-containment (FPL interpreter)|MUST|

When I started identifying these requirements, I quickly realized that it would not suffice to publish them and create a proof of concept. During my analysis, it turned out that many expert views on this subject may deviate from what I'm proposing. Therefore, I decided to publish my analysis in a 
separate paper that *justifies* all these requirements. You can find the paper at ["Formal Proving Language (FPL)
A Proposal How To Write and Read Proof-Based Mathematics (PBM)"](https://www.bookofproofs.org/FPLHighLevelDesign.pdf).

The paper also contains a description of a proof of concept that is based on some first FPL code examples you can
find in this repository as well as the syntax diagrams of the FPL grammar (version 1.0.0).

# 3 Proof of Concept (Current State)

There is a proof of concept (POC) based on the above requirements. It currently consists of the following pieces:

1. The FPL grammar in an EBNF. 
  * [Current syntax diagrams](https://www.bookofproofs.org/FPLSyntaxDiagrams.xhtml)
  * [EBNF definition](https://github.com/bookofproofs/fpl/tree/master/grammar/)
2. [FPL demo theories ](https://github.com/bookofproofs/fpl/tree/master/poc/theories/)
3. A demo python project consisting of a parser generated using the [TatSu package](https://tatsu.readthedocs.io/en/stable/).

# 4 Project 

The project is still ongoing, and you are invited to collaborate. The possible open tasks are, for instance:

1. Along with the existing FPL **parser**, we need an appropriate FPL **interpreter** that would fulfill the semantic requirements of this specification and the PoC.
1. We need to continue the PoC by translating real use cases of mathematics into FPL to ensure that its syntax and semantics cover all features of proof-based mathematics (PBM) we need.
1. We need localization sections for every PoC theory.
1. We have to implement translators from FPL to LaTeX and natural languages based on localization.
1. We need IDEs with code completion and debugging capabilities.
1. We have to enhance FPL interpreters to check the correctness of mathematical proofs written in FPL or auto-generate proofs in FPL.
1. We need a conception of a byte code to pre-compile FPL theories and include libraries without having to parse and interpret them again; also, we need the corresponding FPL compilers.
1. We need a conception of a byte code to pre-compile FPL theories and include libraries without having to parse and interpret them again; also, we need the corresponding FPL compilers.

# 5 Contributing to the Project

The project is still ongoing, and you are invited to collaborate. Please refer to the [contributing section](https://github.com/bookofproofs/fpl/blob/master/CONTRIBUTING.md) for details.

# 6 Getting Started

## 6.1 Software dependencies
* Use python (tested with 3.10 or higher).
* Install the following packages:
  * pytest (7.1.3 or higher) 
  * parameterized (0.8.1 or higher)
  * tatsu (5.8.3 or higher) 
  * anytree (2.8.0 or higher)
  * z3-solver (4.11.2 or higher)
## 6.2 Testing
* Run the [poc tests](https://github.com/bookofproofs/fpl/tree/master/poc/tests) using pytest. (Note: In many python IDEs, there is a shortcut for doing it. For instance, in PyCharm you can just right-click the fpl/poc/tests folder and select 'Run pytest in tests'). 
* If the tests are runnable, your repository is all set.
## 6.3 Trying out the IDE
* Run fpl/ide/fplide.py and open one of the FPL files in the folder [fpl/poc/theories](https://github.com/bookofproofs/fpl/tree/master/poc/theories).





