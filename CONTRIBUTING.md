# What is this project about?
The FPL Interpreter python project is part of a greater Proof of Concept project ("poc"), covering the development of the FPL grammar, the FPL parser, the FPL interpreter, and writing mathematical theories in FPL. The concept for the poc can be found [here](https://www.bookofproofs.org/FPLHighLevelDesign.pdf). The FPL parser is based on the [tatsu package](https://tatsu.readthedocs.io/en/stable/).

# In which areas can you contribute?

At the current stage of the project (as of January 2022), you can contribute in the following areas:
* Improving the existing Integrated Development Environment (IDE) based on tkinter that reflects the special needs of the FPL language ([fpl/ide](https://github.com/bookofproofs/fpl/tree/master/ide)),
* Addressing "To Do" list items (see [FPL Interpreter project](https://github.com/bookofproofs/fpl/projects/1)), including the stages "In Progress" and "Test,"
* Identifying and specifying additional "To Do" items,
* Writing new unit tests
* Bug-fixing existing implementation
* Writing or correcting a Wiki page.

# How to contribute?
It is important to coordinate the project FPL Interpreter among the team.
* In the beginning, get in touch with the team via [Discussions](https://github.com/bookofproofs/fpl/discussions). 
* Please propose the work items you would like to focus on in the Discussions section. Please also describe your anticipated solution, and be sufficiently specific. 
* Next, agree with the team upon the work items you will get assigned to cover.
* Implement the work items.
* If necessary, create unit tests related to the new code. 
* Test your repository against your new and the existing unit tests.
* Before creating a pull request, verify if the number of failed unit test got greater than the number you got before you implemented the change. Ideally, no unit tests should fail before creating the pull request. 
* Create a pull request.

# Conventions for your pull-requests
* Never push your repository directly into the master branch.
* Instead, create pull requests after pushing repositories using the following naming conventions:
* ```bugfix/<descriptive_repository_name>```
* ```feature/<descriptive_repository_name>```
* ```refactoring/<descriptive_repository_name>```

# Release management
There are separate CHANGES.md files with release notes for the [grammar](https://github.com/bookofproofs/fpl/blob/master/grammar/CHANGES.md), the [interpreter](https://github.com/bookofproofs/fpl/blob/master/poc/CHANGES.md), and the [ide](https://github.com/bookofproofs/fpl/blob/master/ide/CHANGES.md). The version numbers follow the semantic versioning MAJOR.MINOR.PATCH convention. Please change the version number in CHANGES.md and describe your specific changes and amendments to the code base accordingly before pushing your repository for a change request. 








