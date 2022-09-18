"""
The AuxSymbolTable class provides static methods to create and maintain the symbol table of the FPL transformer.
It separates the scopes of the corresponding FPL language elements like theorems, predicates, and their variables.
By design of the FPL transformer, there is only one FPL SymbolTable for all theories that are imported
via the 'uses' keyword.
"""
import anytree
from anytree import Resolver
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTGlobal import AuxSTGlobal
from poc.fplerror import FplErrorManager
from anytree import AnyNode, search

"""
from poc.classes.AuxInterpretation import AuxInterpretation
"""


class AuxSymbolTable:

    @staticmethod
    def get_child_by_outline(parent: AuxSTOutline, outline: str):
        r = Resolver(AuxSTConstants.outline)
        try:
            found_node = r.get(parent, outline)
            return found_node
        except anytree.resolver.ChildResolverError:
            return None

    @staticmethod
    def add_localization(locals_node: AuxSTOutline, localization):
        localization.parent = locals_node

    @staticmethod
    def add_axiom_to_theory(theory_node: AuxSTOutline, block):
        """
        Adds an axiom to the theory node
        :param theory_node: the theory node
        :param block: an interpretation of the axiom identifier to be added
        :return: Node of the newly added axiom
        """
        axiom_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_axiom_root)
        block.parent = axiom_nodes

    @staticmethod
    def add_inference_rule_to_theory(theory_node: AuxSTOutline, ir):
        inference_rules = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_ir_root)
        ir.parent = inference_rules

    @staticmethod
    def add_theorem_to_theory(theory_node: AuxSTOutline, block):
        theorems_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_thm_root)
        block.parent = theorems_node
        AuxSTOutline(outline=AuxSTConstants.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSTConstants.block_proof_root, parent=block)

    @staticmethod
    def add_proposition_to_theory(theory_node: AuxSTOutline, block):
        propositions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_prop_root)
        block.parent = propositions_node
        AuxSTOutline(outline=AuxSTConstants.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSTConstants.block_proof_root, parent=block)

    @staticmethod
    def add_lemma_to_theory(theory_node: AuxSTOutline, block):
        lemmas_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_lem_root)
        block.parent = lemmas_node
        AuxSTOutline(outline=AuxSTConstants.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSTConstants.block_proof_root, parent=block)

    @staticmethod
    def add_corollary_to_theory(theory_node: AuxSTOutline, block):
        corollary_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_cor_root)
        block.parent = corollary_node
        # we allow creating corollaries of corollaries
        AuxSTOutline(outline=AuxSTConstants.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSTConstants.block_proof_root, parent=block)

    @staticmethod
    def add_proof_to_theory(theory_node: AuxSTOutline, block):
        proof_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_proof_root)
        block.parent = proof_node

    @staticmethod
    def add_conjecture_to_theory(theory_node: AuxSTOutline, block):
        conjectures_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_conj_root)
        block.parent = conjectures_node
        AuxSTOutline(outline=AuxSTConstants.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSTConstants.block_proof_root, parent=block)

    @staticmethod
    def add_class_to_theory(theory_node: AuxSTOutline, block):
        definitions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_def_root)
        block.parent = definitions_node

    @staticmethod
    def add_predicate_to_theory(theory_node: AuxSTOutline, block):
        definitions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_def_root)
        block.parent = definitions_node

    @staticmethod
    def add_functional_term_to_theory(theory_node: AuxSTOutline, block):
        definitions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_def_root)
        block.parent = definitions_node

    @staticmethod
    def populate_global_nodes(theory_node: AuxSTOutline, error_mgr: FplErrorManager):
        all_globally_registered = tuple()
        def_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxSTConstants.block_def_root).children
        for def_node in def_nodes:
            def_node.set_relative_id("")
            def_node.initialize_vars(theory_node.file_name, error_mgr)
            all_globally_registered += (def_node,)
            if def_node.def_type == AuxSTConstants.classDeclaration:
                # add all constructors of class
                constructors = AuxSymbolTable.get_child_by_outline(def_node, AuxSTConstants.classConstructors).children
                for constructor in constructors:
                    constructor.set_relative_id("")
                    constructor.initialize_vars(theory_node.file_name, error_mgr)
                    all_globally_registered += (constructor,)
                # add all properties of class (if any)
                properties = AuxSymbolTable.get_child_by_outline(def_node, AuxSTConstants.properties).children
                for prop in properties:
                    prop.set_relative_id(def_node.id)
                    prop.initialize_vars(theory_node.file_name, error_mgr)
                    all_globally_registered += (prop,)
            elif def_node.def_type == AuxSTConstants.functionalTerm:
                # add all properties of functional term (if any)
                properties = AuxSymbolTable.get_child_by_outline(def_node, AuxSTConstants.properties).children
                for prop in properties:
                    prop.set_relative_id(def_node.id)
                    prop.initialize_vars(theory_node.file_name, error_mgr)
                    all_globally_registered += (prop,)
            elif def_node.def_type == AuxSTConstants.predicateDeclaration:
                # add all properties of predicate (if any)
                properties = AuxSymbolTable.get_child_by_outline(def_node, AuxSTConstants.properties).children
                for prop in properties:
                    prop.set_relative_id(def_node.id)
                    prop.initialize_vars(theory_node.file_name, error_mgr)
                    all_globally_registered += (prop,)

        other_blocks = AuxSymbolTable.get_child_by_outline(theory_node,
                                                           AuxSTConstants.block_axiom_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_ir_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_thm_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_lem_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_prop_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_conj_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_cor_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSTConstants.block_proof_root).children
        for block in other_blocks:
            block.set_relative_id("")
            if block.outline != AuxSTConstants.block_proof:
                # Postpone initialize vars of proofs since we have to identify its reference theorem-like statement
                # first to be able to run this method properly.
                # In all other cases, calling initialize_vars at this stage is fine.
                block.initialize_vars(theory_node.file_name, error_mgr)
            all_globally_registered += (block,)

        global_references = AuxSymbolTable.get_child_by_outline(theory_node.parent, AuxSTConstants.globals)
        for block in all_globally_registered:
            gid = '.'.join([theory_node.namespace, block.get_relative_id()])  # noqa
            AuxSTGlobal(global_references, gid, block, theory_node)

    @staticmethod
    def get_library_by_filename(library_node: AnyNode, theory_file_name: str):
        return search.find(library_node, lambda node: hasattr(node, "file_name") and node.file_name == theory_file_name)

    @staticmethod
    def get_library_by_namespace(library_node: AnyNode, namespace: str, modifier: str):
        if modifier == "*":
            # for the '*' modifier return all nodes whose namespace starts with the searched namespace
            return search.findall(library_node,
                                  lambda node: hasattr(node, "namespace") and node.namespace.startswith(
                                      namespace + "."))
        else:
            # for no (or other modifier) return all nodes whose namespace equals the searched namespace
            return search.findall(library_node, lambda node: hasattr(node, "namespace") and node.namespace == namespace)

    @staticmethod
    def get_theory_by_namespace_and_file_name(root: AnyNode, theory_namespace: str, theory_file_name: str):
        result = AuxSymbolTable.get_theories(root)
        found_theory_node = None
        for node in result:
            if node.namespace == theory_namespace and node.file_name == theory_file_name:
                found_theory_node = node
                break
        return found_theory_node

    @staticmethod
    def get_theories(root: AnyNode):
        result = search.findall_by_attr(root, AuxSTConstants.theory, AuxSTConstants.outline)
        result = sorted(result, key=lambda obj: obj.namespace)
        return result

    @staticmethod
    def remove_file_from_symbol_table(symbol_table_root, file_name: str):
        """
        Implements a garbage collector, removing all contents of an FPL file from the symbol table.
        :param symbol_table_root: root of the symbol table
        :param file_name: file name to be removed
        :return:
        """
        globals_node = AuxSymbolTable.get_child_by_outline(symbol_table_root, AuxSTConstants.globals)
        theory_node = None
        namespace = None
        for child in globals_node.children:
            if child.theory.file_name == file_name:
                theory_node = child.theory
                namespace = theory_node.namespace
                child.parent = None
                del child
        if theory_node is not None:
            AuxSymbolTable.remove_node_recursively(theory_node)
        else:
            # in case there was a syntax error last time, there was no global node.
            # therefore, try to find the corresponding theory_node of the file directly in the symbol table
            theories = AuxSymbolTable.get_theories(symbol_table_root)
            for theory_node in theories:
                if theory_node.file_name == file_name:
                    namespace = theory_node.namespace
                    AuxSymbolTable.remove_node_recursively(theory_node)
        return namespace

    @staticmethod
    def remove_node_recursively(node):
        for child in node.children:
            AuxSymbolTable.remove_node_recursively(child)
        if len(node.children) == 0:
            node.parent = None
            del node


