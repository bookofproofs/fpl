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

# 4 Contributing to the Project

The project is still ongoing, and you are invited to collaborate. Please refer to the [contributing section](https://github.com/bookofproofs/fpl/blob/master/CONTRIBUTING.md) for details.

# 5 Getting Started

## Software dependencies
* Use python (tested with 3.10 or higher).
* Install the following packages:
  * pytest (7.1.3 or higher) 
  * parameterized (0.8.1 or higher)
  * tatsu (5.8.3 or higher) 
  * anytree (2.8.0 or higher)
  * z3-solver (4.11.2 or higher)
## Testing
* Run the [poc tests](https://github.com/bookofproofs/fpl/tree/master/poc/tests) using pytest. (Note: In many python IDEs, there is a shortcut for doing it. For instance, in PyCharm you can just right-click the fpl/poc/tests folder and select 'Run pytest in tests'). 
* If the tests are runnable, your repository is all set.
## Trying out the IDE
* Run fpl/ide/fplide.py and open one of the FPL files in the folder [fpl/poc/theories](https://github.com/bookofproofs/fpl/tree/master/poc/theories).





