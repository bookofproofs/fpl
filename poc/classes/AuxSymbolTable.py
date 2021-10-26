"""
The AuxSymbolTable class provides static methods to create and maintain the symbol table of the FPL interpreter.
It separates the scopes of the corresponding FPL language elements like theorems, predicates, and their variables.
By design of the FPL interpreter, there is only one FPL SymbolTable for all theories that are imported
via the 'uses' keyword.
"""

import anytree.resolver
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.NamedVariableDeclaration import NamedVariableDeclaration
from anytree import AnyNode, Resolver
import poc.fplerror
import copy


class AuxSymbolTable:
    aliasId = "aliasid"
    axiom = "axiom"
    axioms = "axioms"
    classConstructors = "constructors"
    classes = "classes"
    classConstructor = "constructor"
    classDeclaration = "class"
    classProperty = "property"
    conjectures = "conjectures"
    functionalTerm = "functionalTerm"
    functionalTermImage = "image"
    functionalTerms = "functionalTerms"
    gid = "gid"
    globalLookup = "global"
    ids = "id"
    inferenceRule = "inferenceRule"
    inferenceRules = "inferenceRules"
    mandatory = "mandatory"
    namespace = "namespace"
    param = "param"
    predicates = "predicates"
    predicateDeclaration = "predicateDeclaration"
    properties = "properties"
    proof = "proof"
    optional = "optional"
    outline = "outline"
    property = "property"
    root = "root"
    theoremLikeStmts = "theoremLikeStatements"
    theoremLikeStmt = "theoremLikeStmt"
    theory = "theory"
    theoryName = "theory_name"
    type = "type"
    usedNamespace = "usedNamespace"
    uses = "uses"
    var = "var"
    variables = "variables"

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
        r = Resolver(AuxSymbolTable.theoryName)
        try:
            node = r.get(root, theory_name)
            return node
        except anytree.resolver.ChildResolverError:
            # we have to add a whole subtree
            theory_node = AnyNode(parent=root, outline=AuxSymbolTable.theory, theory_name=theory_name, namespace=None)
            # add all relevant outline sections to the theory node
            AnyNode(parent=theory_node, outline=AuxSymbolTable.uses)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.inferenceRules)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.classes)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.predicates)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.functionalTerms)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.axioms)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.theoremLikeStmts)
            AnyNode(parent=theory_node, outline=AuxSymbolTable.conjectures)
            return theory_node

    @staticmethod
    def get_global_identifiers(root: AnyNode):
        return anytree.search.findall_by_attr(root, name="is_global", value=True)

    @staticmethod
    def get_child_by_outline(parent: AnyNode, outline: str):
        r = Resolver(AuxSymbolTable.outline)
        return r.get(parent, outline)

    @staticmethod
    def _register_global_reference(theory_node: AnyNode, global_id: str, node: AnyNode, errors: list):
        root = theory_node.parent
        global_references_node = AuxSymbolTable.get_child_by_outline(root, AuxSymbolTable.globalLookup)
        # there can be nodes with the same global id in the symbol table. This can happen if the
        r = Resolver(AuxSymbolTable.gid)
        try:
            # There cannot be nodes with the same global id in the symbol table. If this happens, we have some bug
            # in the proceeding steps.
            node = r.get(global_references_node, global_id)
            raise AssertionError("Name conflict was not discovered for " + global_id + " and " + str(node.info))
        except anytree.resolver.ChildResolverError:
            at_least_one_error = False
            significant_name = global_id.split(".")[-1]
            # It can happen that the significant name is the same as some part other of the gid (for instance,
            # an FPL class could be named the same as the namespace or the same as its property). In this case, we
            # have another error.
            names = global_id.split(".")
            for name in names[:-1]:
                if significant_name == name:
                    # Note that the constructor's name of a class is an exception from this rule:
                    # it MUST be named the same as the class name.
                    if node.outline == AuxSymbolTable.classConstructor and name == names[-2]:
                        # ok
                        pass
                    else:
                        errors.append(poc.fplerror.FplMalformedGlobalId(node.info, global_id))
                        at_least_one_error = True

            if not at_least_one_error:
                # if there were no errors, we can register the new node
                AnyNode(parent=global_references_node, outline=node.outline, gid=global_id, node=node)

    @staticmethod
    def add_usage_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        uses_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.uses)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(uses_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=uses_node, outline=AuxSymbolTable.usedNamespace, id=identifier,
                           info=parsing_info.get_ast_info())
        return node

    @staticmethod
    def add_inference_rule_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        inference_rules_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.inferenceRules)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(inference_rules_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=inference_rules_node, outline=AuxSymbolTable.inferenceRule, id=identifier,
                           info=parsing_info.get_ast_info())
            # register the node globally
            gid = '.'.join([theory_node.namespace, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
        return node

    @staticmethod
    def add_class_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        classes_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.classes)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(classes_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=classes_node, outline=AuxSymbolTable.classDeclaration, id=identifier,
                           info=parsing_info.get_ast_info(), type=None)
            # register the node globally
            gid = '.'.join([theory_node.namespace, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add properties and constructors subnodes to this node
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
            AnyNode(parent=node, outline=AuxSymbolTable.classConstructors)
            AnyNode(parent=node, outline=AuxSymbolTable.properties)
        return node

    @staticmethod
    def add_predicate_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        predicates_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.predicates)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(predicates_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=predicates_node, outline=AuxSymbolTable.predicateDeclaration, id=identifier,
                           info=parsing_info.get_ast_info(), overload_id=None)
            # register the node globally
            gid = '.'.join([theory_node.namespace, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
        return node

    @staticmethod
    def add_functional_term_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        functional_terms_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.functionalTerms)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(functional_terms_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=functional_terms_node, outline=AuxSymbolTable.functionalTerm, id=identifier,
                           info=parsing_info.get_ast_info(), overload_id=None)
            # register the node globally
            gid = '.'.join([theory_node.namespace, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.functionalTermImage)
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
            AnyNode(parent=node, outline=AuxSymbolTable.properties)
        return node

    @staticmethod
    def add_axiom_to_theory(theory_node: AnyNode, parsing_info: AuxInterpretation):
        """
        Adds an axiom to the theory node
        :param theory_node: the theory node
        :param parsing_info: an interpretation of the axiom identifier to be added
        :return: Node of the newly added axiom
        """
        axiom_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.axioms)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(axiom_nodes, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=axiom_nodes, outline=AuxSymbolTable.axiom, id=identifier,
                           info=parsing_info.get_ast_info())
            # register the node globally
            gid = '.'.join([theory_node.namespace, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
        return node

    @staticmethod
    def add_theorem_like_stmt(theory_node: AnyNode, parsing_info: AuxInterpretation, statement_type: str):
        theorem_like_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.theoremLikeStmts)
        identifier = parsing_info.id
        r = Resolver(AuxSymbolTable.ids)
        try:
            node = r.get(theorem_like_nodes, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=theorem_like_nodes, outline=AuxSymbolTable.theoremLikeStmt, id=identifier,
                           info=parsing_info.get_ast_info(), statement_type=statement_type)
            # register the node globally
            gid = '.'.join([theory_node.namespace, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
        return node

    @staticmethod
    def add_constructor_to_class(class_node: AnyNode, parsing_info: AuxInterpretation):
        identifier = parsing_info.id
        if class_node.id != identifier:
            # the name of the constructor must not be different from the class name. If it is, th
            parsing_info.all_errors().append(
                poc.fplerror.FplMisspelledConstructor(parsing_info.get_ast_info(), class_node.id, parsing_info.id))

        r = Resolver(AuxSymbolTable.outline)
        constructors_node = r.get(class_node, AuxSymbolTable.classConstructors)
        try:
            r = Resolver(AuxSymbolTable.ids)
            node = r.get(constructors_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=constructors_node, outline=AuxSymbolTable.classConstructor, id=identifier,
                           info=parsing_info.get_ast_info())
            # register the node globally
            theory_node = class_node.parent.parent
            gid = '.'.join([theory_node.namespace, class_node.id, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
        return node

    @staticmethod
    def add_property_to_node(parent: AnyNode, parsing_info: AuxInterpretation, is_mandatory: bool,
                             property_type: AuxInterpretation):
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
        r = Resolver(AuxSymbolTable.outline)
        properties_node = r.get(parent, AuxSymbolTable.properties)
        try:
            r = Resolver(AuxSymbolTable.ids)
            node = r.get(properties_node, identifier)
            parsing_info.all_errors().append(
                poc.fplerror.FplIdentifierAlreadyDeclared(parsing_info.id, parsing_info.get_ast_info(), node.info))
        except anytree.resolver.ChildResolverError:
            node = AnyNode(parent=properties_node, outline=AuxSymbolTable.property, id=identifier,
                           info=parsing_info.get_ast_info(), is_mandatory=is_mandatory, type=property_type.id,
                           overload_id=None)

            # register the node globally
            theory_node = parent.parent.parent
            gid = '.'.join([theory_node.namespace, parent.id, node.id])
            AuxSymbolTable._register_global_reference(theory_node, gid, node, parsing_info.all_errors())
            # in case of functional term nodes, add image as a subnode
            if property_type.id in ["func", "function"]:
                AnyNode(parent=node, outline=AuxSymbolTable.functionalTermImage)
            # add specific subnodes
            AnyNode(parent=node, outline=AuxSymbolTable.variables)
        return node

    @staticmethod
    def get_image_node(func_node: AnyNode):
        r = Resolver(AuxSymbolTable.outline)
        return r.get(func_node, AuxSymbolTable.functionalTermImage)

    @staticmethod
    def add_param_to_image_node(image_node: AnyNode, parsing_info: AuxInterpretation):
        identifier = parsing_info.id
        param_no = str(len(image_node.children) + 1)
        AnyNode(parent=image_node, info=parsing_info.get_ast_info(), id=identifier,
                outline=AuxSymbolTable.param + param_no)

    @staticmethod
    def clone_tree(source: AnyNode):
        """
        Clones a node and attaches recursively all its cloned children
        :param source: AnyNode object
        :param target: AnyNode object
        :return: a clone of source
        """
        target = AnyNode()
        for attr_name in [a for a in dir(source) if
                          not a.startswith('__') and a != "children" and a != "parent" and
                          not callable(getattr(source, a))]:
            setattr(target, attr_name, getattr(source, attr_name))

        for child in source.children:
            child_clone = AuxSymbolTable.clone_tree(child)
            child_clone.parent = target
        return target

    @staticmethod
    def add_vars_to_nodes(parent: AnyNode, named_var_decl: NamedVariableDeclaration, is_signature: bool):
        distinct_vars = dict()
        for var in reversed(named_var_decl.var_list):
            if var.id in distinct_vars:
                named_var_decl.all_errors().append(
                    poc.fplerror.FplVariableDuplicateInVariableList(var, distinct_vars[var.id]))
            else:
                distinct_vars[var.id] = var
            var_node = AnyNode(parent=None,
                               id=var.id,
                               outline=AuxSymbolTable.var,
                               type=named_var_decl.var_type.generalType.id,
                               type_modifier=named_var_decl.var_type.generalType.callModifier,
                               type_inBuilt=named_var_decl.var_type.generalType.inBuilt,
                               type_generic=named_var_decl.var_type.generalType.generic,
                               type_isIndex=named_var_decl.var_type.generalType.isIndex,
                               type_isSyntaxExtension=named_var_decl.var_type.generalType.isSyntaxExtension,
                               info=var.get_ast_info(),
                               is_signature=is_signature
                               )
            if named_var_decl.var_type.paramTuple is not None:
                for next_var_decl in reversed(named_var_decl.var_type.paramTuple.tuple):
                    AuxSymbolTable.add_vars_to_nodes(var_node, next_var_decl, is_signature)
            var_node.parent = parent
