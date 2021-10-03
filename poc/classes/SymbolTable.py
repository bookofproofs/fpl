"""
The SymbolTable will have the following structure (attributes in parentheses are mandatory)

AnyNode (outline='root')
├─ AnyNode (outline='theory', theory_name, namespace)
│  ├─ AnyNode (outline='uses')
│  │  ├─ AnyNode (outline='usedNamespace', id, interpretation)
│  │  └─ ...
│  ├─ AnyNode (outline='inferenceRules')
│  │  ├─ AnyNode (outline='inferenceRule', id, interpretation)
│  │  └─ ...
│  ├─ AnyNode (outline='classes')
│  │  ├─ AnyNode (outline='class', id, interpretation, type)
│  │  │  ├─ AnyNode (outline='properties')
│  │  │  │  ├─ AnyNode (outline='property', id, interpretation, type, is_mandatory)
│  │  │  │  └─ ...
│  │  │  └─ AnyNode (outline='constructors')
│  │  │     ├─ AnyNode (outline='constructor', id, overload_id, interpretation)
│  │  │     └─ ...
│  │  └─ ...
│  ├─ AnyNode (outline='predicates')
│  │  ├─ AnyNode (outline='predicate', id, overload_id, interpretation)
│  │  └─ ...
│  ├─ AnyNode (outline='functionalTerms')
│  │  ├─ AnyNode (outline='functionalTerm', id, overload_id, interpretation, image)
│  │  └─ ...
│  ├─ AnyNode (outline='axioms')
│  │  ├─ AnyNode (outline='axiom', id, interpretation)
│  │  └─ ...
│  ├─ AnyNode (outline='theoremLikeStatements')
│  │  ├─ AnyNode (outline='theoremLikeStatement', id, interpretation, statement_type)
│  │  │  ├─ AnyNode (outline='proof', id, interpretation)
│  │  │  └─ ...
│  │  └─ ...
│  └─ AnyNode (outline='conjectures')
│     ├─ AnyNode (outline='conjecture', id, interpretation)
│     └─ ...
└─ ...
"""

import anytree.resolver
from classes.AuxInterpretation import AuxInterpretation
from classes.AuxOutlines import AuxOutlines
from anytree import AnyNode, Resolver
import fplerror


class SymbolTable:

    @staticmethod
    def add_or_get_theory(root: AnyNode, theory_name: str):
        """
        Adds a new theory tree to the symbol table with the root AnyNode.
        If the theory subtree already existed, simply its root node will be returned.
        If the theory subtree did not exist, the function will add a whole subtree with all relevant subsections.
        :param root: root AnyNode of the whole symbol table
        :param theory_name: name of the theory
        :return: node of the theory
        """
        r = Resolver('theory_name')
        try:
            node = r.get(root, theory_name)
            return node
        except anytree.resolver.ChildResolverError:
            # we have to add a whole subtree
            theory_node = AnyNode(parent=root, outline=AuxOutlines.theory, theory_name=theory_name, namespace=None)
            # add all relevant outline sections to the theory node
            AnyNode(parent=theory_node, outline=AuxOutlines.uses)
            AnyNode(parent=theory_node, outline=AuxOutlines.inferenceRules)
            AnyNode(parent=theory_node, outline=AuxOutlines.classes)
            AnyNode(parent=theory_node, outline=AuxOutlines.predicates)
            AnyNode(parent=theory_node, outline=AuxOutlines.functionalTerms)
            AnyNode(parent=theory_node, outline=AuxOutlines.axioms)
            AnyNode(parent=theory_node, outline=AuxOutlines.theoremLikeStatements)
            AnyNode(parent=theory_node, outline=AuxOutlines.conjectures)
            return theory_node

    @staticmethod
    def get_global_identifiers(root: AnyNode):
        return anytree.search.findall_by_attr(root, name="is_global", value=True)

    @staticmethod
    def get_child_by_outline(parent: AnyNode, outline: str):
        r = Resolver('outline')
        return r.get(parent, outline)

    @staticmethod
    def add_usage_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        uses_node = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.uses)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(uses_node, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=uses_node, outline=AuxOutlines.usedNamespace, id=identifier,
                           interpretation=parsing_info)
        return node

    @staticmethod
    def add_inference_rule_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        inference_rules_node = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.inferenceRules)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(inference_rules_node, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            AnyNode(parent=inference_rules_node, outline=AuxOutlines.inferenceRule, id=identifier,
                    interpretation=parsing_info)

    @staticmethod
    def add_class_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        classes_node = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.classes)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(classes_node, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=classes_node, outline=AuxOutlines.classDeclaration, id=identifier,
                           interpretation=parsing_info, type=None)
        return node

    @staticmethod
    def add_predicate_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        predicates_node = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.predicates)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(predicates_node, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=predicates_node, outline=AuxOutlines.predicate, id=identifier,
                           interpretation=parsing_info, overload_id=None)
        return node

    @staticmethod
    def add_functional_term_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        functional_terms_node = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.functionalTerms)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(functional_terms_node, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=functional_terms_node, outline=AuxOutlines.functionalTerm, id=identifier,
                           interpretation=parsing_info, overload_id=None)
        return node

    @staticmethod
    def add_axiom_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        axiom_nodes = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.axioms)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(axiom_nodes, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=axiom_nodes, outline=AuxOutlines.axiom, id=identifier,
                           interpretation=parsing_info)
        return node
