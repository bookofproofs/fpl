import tatsu
from anytree import AnyNode, RenderTree, search
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxSTClass import AuxSTClass
from poc import fplsemanticanalyzer
from poc.fplerror import FplErrorManager, FplNamespaceNotFound, FplCircularReference
from poc import fplmessage
import os
import sys
from poc.util.fplutil import Utils


class FplInterpreter:

    def __init__(self, parser, root_dir: str, library_node=None):
        self.version = "1.10.2"
        sys.setrecursionlimit(3500)
        self._parser = parser
        self._error_mgr = FplErrorManager()
        abs_path = os.path.abspath(root_dir)
        if os.path.isdir(abs_path):
            self._theory_root_dir = abs_path
        else:
            self._theory_root_dir = os.path.dirname(abs_path)
        self._symbol_table_root = AnyNode(outline=AuxSTConstants.root)
        self._utils = Utils()
        AnyNode(outline=AuxSTConstants.globals, parent=self._symbol_table_root)
        self.file_specific_tags = dict()
        # Used for the recursive loading of namespaces into to symbol table while syntax analysis is running
        # The syntax analysis stores in this dictionary for every namespace / FPL-combination
        # whether this combination was already processed.
        self.processed_namespaces = set()
        if library_node is None:
            self.library_node = AnyNode()
            AnyNode(outline=AuxSTConstants.library, parent=self.library_node)
            self._utils.reload_library(self.library_node, self._theory_root_dir)
        else:
            self.library_node = library_node
        # the analyzer will be initiated once the semantic_analysis method is called
        self._analyzer = None

    def syntax_analysis(self, path_to_theory: str):
        self._syntax_analysis_rek(path_to_theory)
        self._complement_class_inheritance()
        # populate global nodes
        for theory_node in AuxSymbolTable.get_theories(self._symbol_table_root):
            AuxSymbolTable.populate_global_nodes(theory_node, self._error_mgr)

    def _syntax_analysis_rek(self, path_to_theory: str):
        """
        Adds to the symbol table the namespace and its related contents from (potentially multiple) fpl files.
        :param path_to_theory: path to the fpl file with a theory
        :return: None
        """
        theory_file_name = os.path.basename(path_to_theory)
        # look for the file library in the symbol table
        fpl_file_node = AuxSymbolTable.get_library_by_filename(self.library_node, theory_file_name)
        if fpl_file_node is None:
            # the file was not found when the FplInterpreter was constructed
            raise FileNotFoundError(path_to_theory)
        else:
            processed_file_namespace_combination = fpl_file_node.namespace + ":" + theory_file_name
            if processed_file_namespace_combination not in self.processed_namespaces:
                # remember that the combination has been processed to prevent repeating doing the same recursively
                self.processed_namespaces.add(processed_file_namespace_combination)
                # check if the namespace of the file library is already in the symbol table
                fpl_theory_node = AuxSymbolTable.get_theory_by_namespace_and_file_name(self._symbol_table_root,
                                                                                       fpl_file_node.namespace,
                                                                                       fpl_file_node.file_name)
                if fpl_theory_node is None:
                    # the theory has not yet been imported into the symbol table
                    self._load_theory_into_symbol_table(fpl_file_node)
                    fpl_theory_node = AuxSymbolTable.get_theory_by_namespace_and_file_name(self._symbol_table_root,
                                                                                           fpl_file_node.namespace,
                                                                                           fpl_file_node.file_name)

                    # seal the loaded file in the symbol table using the checksum of the loaded FPL file
                    fpl_theory_node.checksum = fpl_file_node.checksum

                    # For each file loaded into the symbol table,
                    # remember the FPL code syntax highlight tags identified during the syntax analysis for the file.
                    # as a dictionary by file name and a list of highlighting tags.
                    self.file_specific_tags[fpl_theory_node.file_name] = fpl_file_node.get_analyser().i.highlight_tags

                    # load namespaces used by the loaded theory into the symbol table recursively
                    uses_node = AuxSymbolTable.get_child_by_outline(fpl_theory_node, AuxSTConstants.uses)
                    for used_namespace in uses_node.children:
                        files_related_to_namespace = \
                            AuxSymbolTable.get_library_by_namespace(self.library_node,
                                                                    used_namespace.id,
                                                                    used_namespace.modifier)
                        if len(files_related_to_namespace) == 0:
                            # We have the case that a namespace referenced inside the theory loaded into
                            # the symbol table was not available in self._theory_root_dir when
                            # the FPL interpreter was constructed.
                            self._error_mgr.add_error(
                                FplNamespaceNotFound(used_namespace.id, fpl_theory_node.file_name,
                                                     used_namespace.zfrom))
                        else:
                            for file_node in files_related_to_namespace:
                                self._syntax_analysis_rek(os.path.join(self._theory_root_dir, file_node.file_name))
                else:
                    if fpl_theory_node.file_name != fpl_file_node.file_name:
                        # We have the case that there is another FPL file in the same root directory
                        # whose namespace is the same as in another FPL file
                        # that was loaded previously into the symbol table.
                        raise NotImplementedError()
                    else:
                        # We have the case that the file was already loaded into the symbol table.
                        # Now we have to check if it had another checksum.
                        if fpl_theory_node.checksum != fpl_file_node.checksum:
                            # the file in the root directory has been changed and
                            # it has to be replaced in the symbol table
                            raise NotImplementedError()
                        else:
                            # The file was already loaded into the symbol table and was not changed by the user in the
                            # root directory, so the symbol table is up-to-date.
                            pass

    def _load_theory_into_symbol_table(self, fpl_file_node):
        fpl_file_node.set_analyser(self._symbol_table_root, self._error_mgr)
        analyser = fpl_file_node.get_analyser()
        if AuxISourceAnalyser.verbose:
            self._parser.parse(fpl_file_node.get_file_content(), semantics=analyser, whitespace='')
        else:
            try:
                self._parser.parse(fpl_file_node.get_file_content(), semantics=analyser, whitespace='')
            except tatsu.exceptions.FailedParse as ex:
                self._error_mgr.add_error(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 1,
                                              fpl_file_node.file_name))
            except tatsu.exceptions.FailedToken as ex:
                self._error_mgr.add_error(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 2,
                                              fpl_file_node.file_name))
            except tatsu.exceptions.FailedPattern as ex:
                self._error_mgr.add_error(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 3,
                                              fpl_file_node.file_name))
            except BaseException as ex:
                self._error_mgr.add_error(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 4,
                                              fpl_file_node.file_name))

    def semantic_analysis(self):
        self._analyzer = fplsemanticanalyzer.SemanticAnalyser(self._symbol_table_root, self._error_mgr)
        self._analyzer.semantic_analysis()

    def print_self_containment_graph(self):
        for i in self._analyzer.sc.get_refs():
            print(i)

    def symbol_table_to_str(self):
        return str(RenderTree(self._symbol_table_root))

    def clear(self):
        """
        Clears the whole symbol table using the garbage collector.
        :return: None
        """
        file_names = set()
        theories = AuxSymbolTable.get_theories(self._symbol_table_root)
        for theory_node in theories:
            if theory_node.file_name not in file_names:
                file_names.add(theory_node.file_name)
        for file_name in file_names:
            self.forget_file(file_name)
        self._error_mgr.clear_errors()

    def get_symbol_table_root(self):
        return self._symbol_table_root

    def get_error_mgr(self):
        return self._error_mgr

    def get_ast_list(self, file_name):
        fpl_node = AuxSymbolTable.get_library_by_filename(self._symbol_table_root, file_name)
        return fpl_node.get_analyser().ast_list

    def forget_file(self, file_name: str):
        # remove the file from the symbol table
        namespace = AuxSymbolTable.remove_file_from_symbol_table(self._symbol_table_root, file_name)
        # remove the file from processed_namespaces
        self.processed_namespaces.remove(namespace + ":" + file_name)
        # remove the errors related to the file
        self._error_mgr.remove_file_errors(file_name)

    def _complement_class_inheritance(self):
        """
        This method is used to complement the symbol table of all class nodes
        with the properties declared in their inheritance predecessors
        :return: None
        """
        all_classes = search.findall(self._symbol_table_root, lambda node: isinstance(node, AuxSTClass))
        # put the classes into a dictionary for faster searching
        all_classes_dict = dict()
        for class_node in all_classes:
            if class_node.id not in all_classes_dict:
                all_classes_dict[class_node.id] = class_node

        avoid_circular_reference = list()
        for class_node_id in all_classes_dict:
            avoid_circular_reference.clear()
            self._complement_class_rek(class_node_id, all_classes_dict, avoid_circular_reference)

    def _complement_class_rek(self, class_node_id: str, all_classes_dict: dict, avoid_circular_reference: list):
        if class_node_id in all_classes_dict:
            class_node = all_classes_dict[class_node_id]

            if class_node_id not in avoid_circular_reference:
                avoid_circular_reference.append(class_node_id)
            else:
                # we detected a circular inheritance
                avoid_circular_reference.append(class_node_id)
                self._error_mgr.add_error(FplCircularReference(class_node, avoid_circular_reference))
                return

            current_inheritance_set = class_node.class_types
            if not class_node.has_inherited_properties() and len(current_inheritance_set) > 0:
                # we have to handle this class because len(current_inheritance_set) > 0 and
                # the class is not yet marked as having inherited properties
                parent_class_id = current_inheritance_set[0]
                # we have to complement the parent class first
                if self._complement_class_rek(parent_class_id, all_classes_dict, avoid_circular_reference):
                    # now, since we have complemented the parent class, we can also complement the current one
                    parents_inheritance_set = all_classes_dict[parent_class_id].class_types
                    if parent_class_id not in parents_inheritance_set:
                        # we clone all properties of the parent classes in the current class
                        class_node.create_callers_parent_properties(all_classes_dict[parent_class_id])
                        # as a last step, complement the inheritance_set of the current class
                        current_inheritance_set += parents_inheritance_set
            return True
        else:
            # ignore this error since it will be detected at the latest in the semantical analysis
            # at this stage, we are still building up the symbol table.
            return False
