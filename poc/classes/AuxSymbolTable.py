"""
The AuxSymbolTable class provides static methods to create and maintain the symbol table of the FPL interpreter.
It separates the scopes of the corresponding FPL language elements like theorems, predicates, and their variables.
By design of the FPL interpreter, there is only one FPL SymbolTable for all theories that are imported
via the 'uses' keyword.
"""

import anytree.resolver
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxOutlines import AuxOutlines
from poc.classes.GeneralType import GeneralType
from poc.classes.VariableType import VariableType
from anytree import AnyNode, Resolver
import poc.fplerror


class AuxSymbolTable:

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
        uses_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.uses)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(uses_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=uses_node, outline=AuxOutlines.usedNamespace, id=identifier,
                           info=parsing_info.get_ast_info())
        return node

    @staticmethod
    def add_inference_rule_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        inference_rules_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.inferenceRules)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(inference_rules_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=inference_rules_node, outline=AuxOutlines.inferenceRule, id=identifier,
                           info=parsing_info.get_ast_info())
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.usedTypes)
        return node

    @staticmethod
    def add_class_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        classes_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.classes)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(classes_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=classes_node, outline=AuxOutlines.classDeclaration, id=identifier,
                           info=parsing_info.get_ast_info(), type=None)
            # add properties and constructors subnodes to this node
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.usedTypes)
            AnyNode(parent=node, outline=AuxOutlines.classConstructors)
            AnyNode(parent=node, outline=AuxOutlines.properties)
        return node

    @staticmethod
    def add_predicate_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        predicates_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.predicates)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(predicates_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=predicates_node, outline=AuxOutlines.predicateDeclaration, id=identifier,
                           info=parsing_info.get_ast_info(), overload_id=None)
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.usedTypes)
        return node

    @staticmethod
    def add_functional_term_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        functional_terms_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.functionalTerms)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(functional_terms_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=functional_terms_node, outline=AuxOutlines.functionalTerm, id=identifier,
                           info=parsing_info.get_ast_info(), overload_id=None)
            AnyNode(parent=node, outline=AuxOutlines.functionalTermImage)
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.usedTypes)
            AnyNode(parent=node, outline=AuxOutlines.properties)
        return node

    @staticmethod
    def add_axiom_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        """
        Adds an axiom to the theory node
        :param theory_node: the theory node
        :param parsing_info: an interpretation of the axiom identifier to be added
        :return: Node of the newly added axiom
        """
        axiom_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.axioms)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(axiom_nodes, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=axiom_nodes, outline=AuxOutlines.axiom, id=identifier,
                           info=parsing_info.get_ast_info())
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.usedTypes)
        return node

    @staticmethod
    def add_theorem_like_stmt(theory_node: AnyNode, parsing_info: AuxInterpretation, statement_type: str):
        theorem_like_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxOutlines.theoremLikeStmts)
        identifier = parsing_info.id
        r = Resolver("id")
        try:
            node = r.get(theorem_like_nodes, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=theorem_like_nodes, outline=AuxOutlines.theoremLikeStmt, id=identifier,
                           info=parsing_info.get_ast_info(), statement_type=statement_type)
            AnyNode(parent=node, outline=AuxOutlines.variables)
            AnyNode(parent=node, outline=AuxOutlines.usedTypes)
        return node

    @staticmethod
    def add_constructor_to_class(class_node: AnyNode, parsing_info: AuxInterpretation):
        identifier = parsing_info.id
        if class_node.id != identifier:
            # the name of the constructor must not be different from the class name. If it is, th
            parsing_info.all_errors().append(
                poc.fplerror.FplMisspelledConstructor(parsing_info.get_ast_info(), class_node.id, parsing_info.id))
            return None
        else:
            r = Resolver("outline")
            constructors_node = r.get(class_node, AuxOutlines.classConstructors)
            try:
                r = Resolver("id")
                node = r.get(constructors_node, identifier)
                parsing_info.all_errors().append(
                    poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
            except anytree.resolver.ChildResolverError:
                node = AnyNode(parent=constructors_node, outline=AuxOutlines.classConstructor, id=identifier,
                               info=parsing_info.get_ast_info())
                AnyNode(parent=node, outline=AuxOutlines.variables)
                AnyNode(parent=node, outline=AuxOutlines.usedTypes)
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
        identifier = parsing_info.id
        if parent.id == identifier:
            # the name of the property must be different from the name of the parent node.
            parsing_info.all_errors().append(
                poc.fplerror.FplWrongPropertyName(parsing_info.get_ast_info(), parent.id, parsing_info.id))
            return None
        else:
            r = Resolver("outline")
            properties_node = r.get(parent, AuxOutlines.properties)
            try:
                r = Resolver("id")
                node = r.get(properties_node, identifier)
                parsing_info.all_errors().append(
                    poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
            except anytree.resolver.ChildResolverError:
                node = AnyNode(parent=properties_node, outline=AuxOutlines.property, id=identifier,
                               info=parsing_info.get_ast_info(), is_mandatory=is_mandatory, type=property_type,
                               overload_id=None)
                if property_type == AuxOutlines.functionalTerm:
                    AnyNode(parent=node, outline=AuxOutlines.functionalTermImage)
                AnyNode(parent=node, outline=AuxOutlines.variables)
                AnyNode(parent=node, outline=AuxOutlines.usedTypes)
        return node

    @staticmethod
    def add_variables_to_node(parent: AnyNode, parsing_info: AuxInterpretation, var_list: list, is_signature: bool):
        """
        Adds variables to a node in the symbol table.
        :param parent: A node of the symbol table
        :param parsing_info: parsing_info of the GeneralType, with which the var list are declared.
        :param var_list: list of Variable rule interpretations
        :param is_signature: True iif the variable is declared inside the signature
        :return: None
        """
        r = Resolver('outline')
        variables_node = r.get(parent, AuxOutlines.variables)
        r = Resolver('id')
        while len(var_list) > 0:
            var = var_list.pop()
            var_name = var.id
            try:
                var_node = r.get(variables_node, var_name)
                parsing_info.all_errors().append(
                    poc.fplerror.FplVariableDuplicateInVariableList(var_node.info, var_name))
            except anytree.resolver.ChildResolverError:
                AnyNode(parent=variables_node,
                        id=var_name,
                        outline=AuxOutlines.var,
                        type=parsing_info.generalType.id,
                        info=var.get_ast_info(),
                        is_signature=is_signature
                        )
        return None

    @staticmethod
    def register_used_type_of_node(parent: AnyNode, parsing_info: AuxInterpretation):
        """
        Registers a type in the subnoded usedTypes of some node in the symbol table that contains the outline
        AuxOutlines.usedTypes.
        :param parent: node, to which the type should be added
        :param parsing_info: parsing info of the type
        :return: None
        """
        r = Resolver('outline')
        used_types_node = r.get(parent, AuxOutlines.usedTypes)
        r = Resolver('id')
        identifier = ""
        if type(parsing_info) is GeneralType:
            identifier = parsing_info.id
        elif type(parsing_info) is VariableType:
            identifier = parsing_info.generalType.id
        else:
            raise TypeError(parsing_info)
        inbuilt = False
        generic = False
        if identifier == "obj" or identifier == "object":
            inbuilt = True
            generic = False
        elif identifier == "pred" or identifier == "predicate":
            inbuilt = True
            generic = False
        elif identifier == "func" or identifier == "function":
            inbuilt = True
            generic = False
        elif identifier.startswith("tpl"):
            inbuilt = False
            generic = True
        try:
            r.get(used_types_node, identifier)
        except anytree.resolver.ChildResolverError:
            AnyNode(parent=used_types_node,
                    id=identifier,
                    outline=AuxOutlines.type,
                    inbuilt=inbuilt,
                    generic=generic,
                    info=parsing_info.get_ast_info()
                    )
        return None

    @staticmethod
    def get_image_node(func_node: AnyNode):
        r = Resolver('outline')
        return r.get(func_node, AuxOutlines.functionalTermImage)

    @staticmethod
    def add_param_to_image_node(image_node: AnyNode, parsing_info: AuxInterpretation):
        identifier = parsing_info.id
        param_no = str(len(image_node.children) + 1)
        AnyNode(parent=image_node, info=parsing_info.get_ast_info(), id=identifier,
                outline=AuxOutlines.param + param_no)

    @staticmethod
    def _add_attributes(node: AnyNode, parsing_info: AuxInterpretation):
        """
        Iterates through the attributes of parsing_info and adds its attributes to node if they are not
        python standard and not callable. As a result, node will get a copy of all user-defined attributes
        of parsing_info.
        :param node: a node in the symbol tree
        :param parsing_info: An object with attributes
        :return: None
        """
        attributes = [a for a in dir(parsing_info) if not a.startswith('__') and not callable(getattr(parsing_info, a))]
        for a in attributes:
            setattr(node, a, getattr(parsing_info, a))
