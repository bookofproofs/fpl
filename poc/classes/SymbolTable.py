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
│  │  │  ├─ AnyNode (outline='variables')
│  │  │  │  ├─ AnyNode (outline='var', id, type, value, in_signature)
│  │  │  │  └─ ...
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
            AnyNode(parent=theory_node, outline=AuxOutlines.theoremLikeStmts)
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
            node = AnyNode(parent=inference_rules_node, outline=AuxOutlines.inferenceRule, id=identifier,
                           interpretation=parsing_info)
            AnyNode(parent=node, outline=AuxOutlines.variables)
        return node

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
            # add properties and constructors subnodes to this node
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.classConstructors)
            AnyNode(parent=node, outline=AuxOutlines.properties)
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
            node = AnyNode(parent=predicates_node, outline=AuxOutlines.predicateDeclaration, id=identifier,
                           interpretation=parsing_info, overload_id=None)
            AnyNode(parent=node, outline=AuxOutlines.variables)
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
            AnyNode(parent=node, outline=AuxOutlines.functionalTermImage)
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.properties)
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
            AnyNode(parent=node, outline=AuxOutlines.variables)
        return node

    @staticmethod
    def add_theorem_like_stmt(theory_node: AnyNode, parsing_info: AuxInterpretation, statement_type: str):
        theorem_like_nodes = SymbolTable.get_child_by_outline(theory_node, AuxOutlines.theoremLikeStmts)
        identifier = parsing_info.get_interpretation()
        r = Resolver("id")
        try:
            node = r.get(theorem_like_nodes, identifier)
            parsing_info.all_errors().append(fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=theorem_like_nodes, outline=AuxOutlines.theoremLikeStmt, id=identifier,
                           interpretation=parsing_info, statement_type=statement_type)
            AnyNode(parent=node, outline=AuxOutlines.variables)
        return node

    @staticmethod
    def add_constructor_to_class(class_node: AnyNode, parsing_info: AuxInterpretation):
        identifier = parsing_info.get_interpretation()
        if class_node.id != identifier:
            # the name of the constructor must not be different from the class name. If it is, th
            parsing_info.all_errors().append(fplerror.FplMisspelledConstructor(parsing_info, class_node.id))
            return None
        else:
            r = Resolver("outline")
            constructors_node = r.get(class_node, AuxOutlines.classConstructors)
            try:
                r = Resolver("id")
                node = r.get(constructors_node, identifier)
                parsing_info.all_errors().append(
                    fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
            except anytree.resolver.ChildResolverError:
                node = AnyNode(parent=constructors_node, outline=AuxOutlines.classConstructor, id=identifier,
                               interpretation=parsing_info)
                AnyNode(parent=node, outline=AuxOutlines.variables)
            return node

    @staticmethod
    def add_property_to_node(parent: AnyNode, parsing_info: AuxInterpretation, is_mandatory: bool, property_type: str):
        """
        Adds a property to a node that can be either a class node or a functional term node.
        In FPL, classes and functional terms can have a property
        :param parent: class or functional term node
        :param parsing_info: the interpretation of the predicate identifier to be added
        :param is_mandatory: indicates if the property is mandatory
        :param property_type: type of the property
        :return:
        """
        identifier = parsing_info.get_interpretation()
        if parent.id == identifier:
            # the name of the property must be different from the name of the parent node.
            parsing_info.all_errors().append(fplerror.FplWrongPropertyName(parsing_info, parent.id))
            return None
        else:
            r = Resolver("outline")
            properties_node = r.get(parent, AuxOutlines.properties)
            try:
                r = Resolver("id")
                node = r.get(properties_node, identifier)
                parsing_info.all_errors().append(
                    fplerror.FplIdentifierAlreadyDeclared(parsing_info, node.interpretation))
            except anytree.resolver.ChildResolverError:
                node = AnyNode(parent=properties_node, outline=AuxOutlines.property, id=identifier,
                               interpretation=parsing_info, is_mandatory=is_mandatory, type=property_type,
                               overload_id=None)
                if property_type == AuxOutlines.functionalTerm:
                    AnyNode(parent=node, outline=AuxOutlines.functionalTermImage)
                AnyNode(parent=node, outline=AuxOutlines.variables)
            return node

    @staticmethod
    def get_image_node(func_node: AnyNode):
        r = Resolver('outline')
        return r.get(func_node, AuxOutlines.functionalTermImage)

    @staticmethod
    def add_param_to_image_node(image_node: AnyNode, parsing_info: AuxInterpretation):
        identifier = parsing_info.typeRepresentation
        param_no = str(len(image_node.children) + 1)
        AnyNode(parent=image_node, interpretation=parsing_info, id=identifier, outline=AuxOutlines.param + param_no)
