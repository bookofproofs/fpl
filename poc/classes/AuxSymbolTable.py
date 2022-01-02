"""
The AuxSymbolTable class provides static methods to create and maintain the symbol table of the FPL transformer.
It separates the scopes of the corresponding FPL language elements like theorems, predicates, and their variables.
By design of the FPL transformer, there is only one FPL SymbolTable for all theories that are imported
via the 'uses' keyword.
"""

from anytree import Resolver
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTGlobal import AuxSTGlobal
from poc.classes.AuxSTVarDec import AuxSTVarDec
import poc.fplerror
from anytree import AnyNode, search

"""
from poc.classes.AuxInterpretation import AuxInterpretation
"""


class AuxSymbolTable:
    aliasId = "aliasid"  # noqa
    block_def = "definition"
    block_def_root = "definitions"
    block_thm = "theorem"
    block_thm_root = "theorems"
    block_axiom = "axiom"
    block_axiom_root = "axioms"
    block_ir = "inferenceRule"
    block_ir_root = "inferenceRules"
    block_lem = "lemma"
    block_lem_root = "lemmas"
    block_prop = "proposition"
    block_prop_root = "propositions"
    block_cor = "corollary"
    block_cor_root = "corollaries"
    block_proof = "proofArgument"
    block_proof_root = "proofs"
    block_conj = "conjecture"
    block_conj_root = "conjectures"
    cases = "cases"
    case = "case"
    case_default = "else"
    classConstructors = "constructors"
    classConstructor = "constructor"
    classDefaultConstructor = "defaultConstructor"
    classDeclaration = "class"
    classInstance = "classInstance"
    con = "con"
    content = "content"
    coord_list = "coordinates"
    digit = "digit"
    ebnf_factor = "EBNFFactor"
    ebnf_string = "EBNFString"
    ebnf_term = "EBNFTerm"
    ebnf_transl = "EBNFTransl"
    entity_with_coord = "entity[]"
    entity = "entity"
    extDigit = "extDigit"
    file = "file"
    functionalTerm = "functionalTerm"
    functionalTermInstance = "functionalTermInstance"
    functionalTermImage = "image"
    globals = "globals"
    ids = "id"
    arg_id = "argID"
    intrinsic = "intrinsic"
    image = "image"
    index_value = "indexValue"
    statement_is = "is"
    justification = "justification"
    library = "library"
    localization = "localization"
    localization_root = "localizations"
    mandatory = "mandatory"
    namespace = "namespace"
    param = "param"
    pre = "pre"
    preReferenced = "referencedPre"
    predicate_all = "all"
    predicate_conjunction = "and"
    predicate_disjunction = "or"
    predicate_equivalence = "<=>"
    predicate_exists = "ex"
    predicate_exclusiveOr = "xor"
    predicate_false = "false"
    predicate_implication = "=>"
    predicate_negation = "not"
    predicate_true = "true"
    predicate_identifier = "predicateIdentifier"
    predicate_with_arguments = "predicateWithArgs"
    predicateDeclaration = "predicateDeclaration"
    predicateInstance = "predicateInstance"
    properties = "properties"
    proofArgument = "argument"
    proofArgument_root = "arguments"
    optional = "optional"
    outline = "outline"
    property = "property"
    rng = "range"
    root = "root"
    selfInstance = "self"
    signature = "signature"
    signature_class = "signature_class"
    statements = "statements"
    statement = "statement"
    statement_list = "stmtList"
    statement_py = "py"
    statement_cases = "cases"
    statement_assert = "assert"
    statement_assign = ":="
    statement_range = "range"
    statement_loop = "loop"
    statement_return = "return"
    theoremLikeStmt = "theoremLikeStmt"
    theory = "theory"
    theoryName = "theory_file_name"
    translation = "translation"
    translation_list = "translationList"
    type = "type"
    undefined = "undefined"
    used = "used"
    uses = "uses"
    var = "var"
    var_decl = "var_decl"  # noqa
    var_spec = "specificationList"
    variadic_var = "variadicVar"

    @staticmethod
    def get_child_by_outline(parent: AuxSTOutline, outline: str):
        r = Resolver(AuxSymbolTable.outline)
        return r.get(parent, outline)

    @staticmethod
    def add_namespace(root: AnyNode, fpl_file):
        library_node = AuxSymbolTable.get_child_by_outline(root, AuxSymbolTable.library)
        fpl_file.parent = library_node

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
        axiom_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_axiom_root)
        block.parent = axiom_nodes

    @staticmethod
    def add_inference_rule_to_theory(theory_node: AuxSTOutline, ir):
        inference_rules = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_ir_root)
        ir.parent = inference_rules

    @staticmethod
    def add_theorem_to_theory(theory_node: AuxSTOutline, block):
        theorems_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_thm_root)
        block.parent = theorems_node
        AuxSTOutline(outline=AuxSymbolTable.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSymbolTable.block_proof_root, parent=block)

    @staticmethod
    def add_proposition_to_theory(theory_node: AuxSTOutline, block):
        propositions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_prop_root)
        block.parent = propositions_node
        AuxSTOutline(outline=AuxSymbolTable.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSymbolTable.block_proof_root, parent=block)

    @staticmethod
    def add_lemma_to_theory(theory_node: AuxSTOutline, block):
        lemmas_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_lem_root)
        block.parent = lemmas_node
        AuxSTOutline(outline=AuxSymbolTable.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSymbolTable.block_proof_root, parent=block)

    @staticmethod
    def add_corollary_to_theory(theory_node: AuxSTOutline, block):
        corollary_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_cor_root)
        block.parent = corollary_node
        # we allow creating corollaries of corollaries
        AuxSTOutline(outline=AuxSymbolTable.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSymbolTable.block_proof_root, parent=block)

    @staticmethod
    def add_proof_to_theory(theory_node: AuxSTOutline, block):
        proof_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_proof_root)
        block.parent = proof_node

    @staticmethod
    def add_conjecture_to_theory(theory_node: AuxSTOutline, block):
        conjectures_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_conj_root)
        block.parent = conjectures_node
        AuxSTOutline(outline=AuxSymbolTable.block_cor_root, parent=block)
        AuxSTOutline(outline=AuxSymbolTable.block_proof_root, parent=block)

    @staticmethod
    def add_class_to_theory(theory_node: AuxSTOutline, block):
        definitions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_def_root)
        block.parent = definitions_node

    @staticmethod
    def add_predicate_to_theory(theory_node: AuxSTOutline, block):
        definitions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_def_root)
        block.parent = definitions_node

    @staticmethod
    def add_functional_term_to_theory(theory_node: AuxSTOutline, block):
        definitions_node = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_def_root)
        block.parent = definitions_node

    @staticmethod
    def populate_global_nodes(theory_node: AuxSTOutline):
        all_globally_registered = tuple()
        other_blocks = AuxSymbolTable.get_child_by_outline(theory_node,
                                                           AuxSymbolTable.block_axiom_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_ir_root).children
        def_nodes = AuxSymbolTable.get_child_by_outline(theory_node, AuxSymbolTable.block_def_root).children
        for def_node in def_nodes:
            def_node.set_relative_id("")
            all_globally_registered += (def_node,)
            if def_node.def_type == AuxSymbolTable.classDeclaration:
                # add all constructors of class
                constructors = AuxSymbolTable.get_child_by_outline(def_node, AuxSymbolTable.classConstructors).children
                for constructor in constructors:
                    constructor.set_relative_id("")
                    all_globally_registered += (constructor,)
                # add all properties of class (if any)
                properties = AuxSymbolTable.get_child_by_outline(def_node, AuxSymbolTable.properties).children
                for prop in properties:
                    prop.set_relative_id(def_node.id)
                    all_globally_registered += (prop,)
            elif def_node.def_type == AuxSymbolTable.functionalTerm:
                # add all properties of functional term (if any)
                properties = AuxSymbolTable.get_child_by_outline(def_node, AuxSymbolTable.properties).children
                for prop in properties:
                    prop.set_relative_id(def_node.id)
                    all_globally_registered += (prop,)
            elif def_node.def_type == AuxSymbolTable.predicateDeclaration:
                # add all properties of predicate (if any)
                properties = AuxSymbolTable.get_child_by_outline(def_node, AuxSymbolTable.properties).children
                for prop in properties:
                    prop.set_relative_id(def_node.id)
                    all_globally_registered += (prop,)

        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_thm_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_lem_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_prop_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_conj_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_cor_root).children
        other_blocks += AuxSymbolTable.get_child_by_outline(theory_node,
                                                            AuxSymbolTable.block_proof_root).children

        for block in other_blocks:
            block.set_relative_id("")
            all_globally_registered += (block,)

        global_references = AuxSymbolTable.get_child_by_outline(theory_node.parent, AuxSymbolTable.globals)
        # todo: special treatment of corollaries
        for block in all_globally_registered:
            gid = '.'.join([theory_node.namespace, block.get_relative_id()])  # noqa
            AuxSTGlobal(global_references, gid, block)

    @staticmethod
    def add_vars_to_node(i, parent: AuxSTOutline, named_var_declaration):
        distinct_vars = dict()
        ast_info = named_var_declaration.get_ast_info()
        for var in reversed(named_var_declaration.var_list):
            if var.var.id in distinct_vars:
                named_var_declaration.all_errors().append(
                    poc.fplerror.FplVariableDuplicateInVariableList(distinct_vars[var.var.id], var.var, ast_info.file))
            else:
                distinct_vars[var.var.id] = var.var
            var_dec = AuxSTVarDec(i)
            var_dec.zto = named_var_declaration.zto
            var_dec.zfrom = named_var_declaration.zfrom
            var_dec.id = var.var.id
            var_dec.parent = parent
            var_dec.type = named_var_declaration.var_type.generalType.id
            var_dec.type_pattern = named_var_declaration.var_type.generalType.type_pattern
            var_dec.type_mod = named_var_declaration.var_type.generalType.type_mod
            if named_var_declaration.var_type.paramTuple is not None:
                for next_var_decl in named_var_declaration.var_type.paramTuple.tuple:  # noqa
                    AuxSymbolTable.add_vars_to_node(i, var_dec, next_var_decl)

    @staticmethod
    def get_theory_by_filename(root: AnyNode, theory_file_name: str):
        library_node = AuxSymbolTable.get_child_by_outline(root, AuxSymbolTable.library)
        return search.find(library_node, lambda node: hasattr(node, "file_name") and node.file_name == theory_file_name)

    @staticmethod
    def get_theory_by_namespace(root: AnyNode, theory_namespace: str):
        result = search.findall_by_attr(root, AuxSymbolTable.theory, AuxSymbolTable.outline)
        found_theory_node = None
        for node in result:
            if node.namespace == theory_namespace:
                found_theory_node = node
                break
        return found_theory_node

    @staticmethod
    def remove_library(root):
        library_node = AuxSymbolTable.get_child_by_outline(root, AuxSymbolTable.library)
        library_node.parent = None
