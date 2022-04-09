import tatsu
from anytree import AnyNode, RenderTree
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc import fplsemanticanalyzer
from poc import fplerror
from poc import fplmessage
import os
import sys
from poc.util.fplutil import Utils


class FplInterpreter:

    def __init__(self, parser, root_dir: str, library_node=None):
        self.version = "1.4.12"
        sys.setrecursionlimit(3500)
        self._parser = parser
        self._errors = []
        abs_path = os.path.abspath(root_dir)
        if os.path.isdir(abs_path):
            self._theory_root_dir = abs_path
        else:
            self._theory_root_dir = os.path.dirname(abs_path)
        self._symbol_table_root = AnyNode(outline=AuxSymbolTable.root)
        self._utils = Utils()
        AnyNode(outline=AuxSymbolTable.globals, parent=self._symbol_table_root)
        self.files_highlight_tags = dict()
        # Used for the recursive loading of namespaces into to symbol table while syntax analysis is running
        # The syntax analysis stores in this dictionary for every namespace / FPL-combination
        # whether this combination was already processed.
        self.processed_namespaces = set()
        if library_node is None:
            self.library_node = AnyNode()
            AnyNode(outline=AuxSymbolTable.library, parent=self.library_node)
            self._utils.reload_library(self.library_node, self._theory_root_dir)
        else:
            self.library_node = library_node

    def syntax_analysis(self, path_to_theory: str):
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
                    self.files_highlight_tags[fpl_theory_node.file_name] = fpl_file_node.get_analyser().i.highlight_tags

                    # load namespaces used by the loaded theory into the symbol table recursively
                    uses_node = AuxSymbolTable.get_child_by_outline(fpl_theory_node, AuxSymbolTable.uses)
                    for used_namespace in uses_node.children:
                        files_related_to_namespace = \
                            AuxSymbolTable.get_library_by_namespace(self.library_node,
                                                                    used_namespace.id,
                                                                    used_namespace.modifier)
                        if len(files_related_to_namespace) == 0:
                            # We have the case that a namespace referenced inside the theory loaded into
                            # the symbol table was not available in self._theory_root_dir when
                            # the FPL interpreter was constructed.
                            self._errors.append(
                                fplerror.FplNamespaceNotFound(used_namespace.id, fpl_theory_node.file_name,
                                                              used_namespace.zfrom))
                        else:
                            for file_node in files_related_to_namespace:
                                self.syntax_analysis(os.path.join(self._theory_root_dir, file_node.file_name))
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
        fpl_file_node.set_analyser(self._symbol_table_root, self._errors)
        analyser = fpl_file_node.get_analyser()
        if AuxISourceAnalyser.verbose:
            self._parser.parse(fpl_file_node.get_file_content(), semantics=analyser, whitespace='')
        else:
            try:
                self._parser.parse(fpl_file_node.get_file_content(), semantics=analyser, whitespace='')
            except tatsu.exceptions.FailedParse as ex:
                self._errors.append(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 1))
            except tatsu.exceptions.FailedToken as ex:
                self._errors.append(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 2))
            except tatsu.exceptions.FailedPattern as ex:
                self._errors.append(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 3))
            except BaseException as ex:
                self._errors.append(
                    fplmessage.FplParserError(ex, "in " + fpl_file_node.file_name + ":" + str(ex), 4))

    def semantic_analysis(self):
        analyzer = fplsemanticanalyzer.SemanticAnalyser(self._symbol_table_root, self._errors)
        analyzer.semantic_analysis()

    def print_symbol_table(self):
        print(RenderTree(self._symbol_table_root))

    def symbol_table_to_str(self):
        return str(RenderTree(self._symbol_table_root))

    def clear(self):
        self._symbol_table_root.children = tuple([])
        self._errors.clear()

    def get_symbol_table_root(self):
        return self._symbol_table_root

    def has_errors(self):
        return len(self._errors) > 0

    def print_errors(self):
        if len(self._errors) > 0:
            print(str(len(self._errors)), "errors found:")
            for err in self._errors:
                print(err)
        else:
            print("Congratulations! No errors found")

    def get_errors(self):
        return self._errors

    def get_ast_list(self, file_name):
        fpl_node = AuxSymbolTable.get_library_by_filename(self._symbol_table_root, file_name)
        return fpl_node.get_analyser().ast_list

    def forget_file(self, file_name: str):
        # remove the file from the symbol table
        namespace = AuxSymbolTable.remove_file_from_symbol_table(self._symbol_table_root, file_name)
        # remove the file from processed_namespaces
        self.processed_namespaces.remove(namespace + ":" + file_name)
        # remove the errors related to the file
        new_errors = list()
        for err in self._errors:
            if err.file != file_name:
                new_errors.append(err)
        self._errors.clear()
        self._errors = new_errors
