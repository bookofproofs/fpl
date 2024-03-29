import time
import tatsu
import io
import os
import re
from poc.classes.AuxSTFplFile import AuxSTFplFile
from poc.fplerror import FplErrorManager


class Utils:
    _stopwatch_measurements = dict()
    _stopwatch = time.perf_counter()
    preprocessor = '##############################'

    @staticmethod
    def get_file_content(path_to_file):
        with io.open(path_to_file, 'r', encoding="utf-8") as file:
            file = file.read()
        return file

    @staticmethod
    def save_file_content(path_to_file: str, content):
        with io.open(path_to_file, 'w', encoding="UTF-8") as file:
            file.write(content)

    def get_elapsed_seconds(self):
        """
        read the stopwatch
        :return: elapsed seconds from the initialization of the semantics class
        """
        return round(time.perf_counter() - self._stopwatch, 2)

    def add_distinct_duration(self, action_label):
        """
        Adds a labeled duration measurement for an action and resets the stopwatch
        :param action_label:  label of the action
        :return: elapsed seconds
        """
        self._stopwatch_measurements[action_label] = self.get_elapsed_seconds()
        self._stopwatch = time.perf_counter()

    def print_durations(self):
        for dur in self._stopwatch_measurements:
            print(dur, ": ", self._stopwatch_measurements[dur], "s")

    def get_parser(self, path_to_ebnf_file):
        """
        creates a tatsu parser out of an ebnf_file from source
        :param path_to_ebnf_file: path to source
        :return: tatsu parser
        """
        return tatsu.compile(self.get_file_content(path_to_ebnf_file))

    @staticmethod
    def adjust_symbol_table_for_testing(interpreter):
        """
        Removes from the test output all dynamic object memory addresses because they are irrelevant for the test.
        :param interpreter: interpreter object reference
        :return: test_result replaced
        """
        test_output = interpreter.symbol_table_to_str().strip()
        # remove "poc.classes." paths
        test_output = test_output.replace("poc.classes.", "")
        # remove dynamic object memory overridden_qualified_identifiers
        test_output = re.sub(' object at 0x[0-9A-F]+', '', test_output)
        # remove AnyNode string representations that are the "node" attribute of AnyNode
        test_output = re.sub(r'(=AnyNode\()([\$a-zA-Z0-9_=\', <.>*+\[\]\:@]+)(\)[.]*)', r"\1\3", test_output)
        # remove Aux* string representations
        test_output = re.sub(r'(=Aux[a-zA-Z]+\()([\$a-zA-Z0-9_=\', <.>*+\[\]\:@]+)(\)[.]*)', r"\1\3", test_output)
        return test_output

    @staticmethod
    def get_code_and_expected(path_to_usecases, use_case_name):
        file_content = Utils.get_file_content(path_to_usecases + "/" + use_case_name)
        return file_content.split(Utils.preprocessor)

    @staticmethod
    def rewrite_expected_test_case(path_to_usecases, use_case_name, expected):
        file_content_split = Utils.get_code_and_expected(path_to_usecases, use_case_name)
        new_file_content = file_content_split[0].strip() + "\n" + Utils.preprocessor + "\n" + expected
        Utils.save_file_content(path_to_usecases + "/" + use_case_name, new_file_content)

    @staticmethod
    def strip_preprocessor(source: str):
        return source.split(Utils.preprocessor)[0].strip()

    def reload_library(self, library_node, root_dir):
        """
        This function reads all fpl files within the root directory, extracts
        their namespace and adds it to the library node of this ide.
        :return: None
        """
        for child in library_node.children:
            child.parent = None
            del child

        for file in os.listdir(root_dir):
            if file.endswith(".fpl"):
                fpl_file = AuxSTFplFile()
                fpl_file.file_name = os.path.basename(file)
                file_content = self.get_file_content(os.path.join(root_dir, file))
                # strip any preprocessor from the file content
                file_content = self.strip_preprocessor(file_content)
                fpl_file.set_file_content(file_content)
                first_block = fpl_file.get_file_content().find("{")
                if first_block > -1:
                    namespace_of_source = fpl_file.get_file_content()[0:first_block].strip()
                else:
                    raise AssertionError("Namespace not found in " + file)
                fpl_file.namespace = namespace_of_source
                fpl_file.parent = library_node

    @staticmethod
    def identify_clicked_treeview_item(tree_view):
        """
        Try to identify the clicked tkinter treeview item.
        :param tree_view: tree view object
        :return: None if failure, or tuple of clicked values
        """
        curr_item = tree_view.focus()
        if curr_item == "":
            # for some reason, some clicks do not focus the item but ''. In this case try to select the first one
            all_children = tree_view.get_children()
            if len(all_children) > 0:
                curr_item = tree_view.get_children()[0]
            else:
                # return nothing
                return None
        tree_view.selection_set(curr_item)
        tree_view.focus(curr_item)
        item = tree_view.item(curr_item)
        return item['values']

    @staticmethod
    def check_if_error_occurs(error_msg: str, error_mgr: FplErrorManager, expected_diagnose_id):
        error_msg = error_msg.strip()
        for error in error_mgr.get_errors():
            if error_msg == str(error):
                if expected_diagnose_id == error.diagnose_id:
                    return True
        return False

    @staticmethod
    def check_if_error_does_not_occur(error_mgr: FplErrorManager, diagnose_id):
        for error in error_mgr.get_errors():
            if diagnose_id == error.diagnose_id:
                return False
        return True

