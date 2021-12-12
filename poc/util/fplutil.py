import time
import tatsu
import io
import re


class Utils:
    _stopwatch_measurements = dict()
    _stopwatch = time.perf_counter()

    @staticmethod
    def get_file_content(path_to_file):
        with io.open(path_to_file, 'r', encoding="utf-8") as file:
            file = file.read()
        return file

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
    def remove_object_references_from_string(test_output: str):
        """
        Removes from the test output all dynamic object memory addresses because they are irrelevant for the test.
        :param test_output: output of the test
        :return: test_result replaced
        """
        # remove "poc.classes." paths
        test_output = test_output.replace("poc.classes.", "")
        # remove dynamic object memory references
        test_output = re.sub(' object at 0x[0-9A-F]+', '', test_output)
        # remove AnyNode string representations that are the "node" attribute of AnyNode
        test_output = re.sub(r'(=AnyNode\()([a-zA-Z0-9_=\', <.>*+\[\]\:@]+)(\)[.]*)', r"\1\3", test_output)
        # remove Aux* string representations
        test_output = re.sub(r'(=Aux[a-zA-Z]+\()([a-zA-Z0-9_=\', <.>*+\[\]\:@]+)(\)[.]*)', r"\1\3", test_output)
        test_output = re.sub('<AuxAstInfo.AuxAstInfo>', "AuxAstInfo()", test_output)
        return test_output

    @staticmethod
    def get_code_and_expected(path_to_usecases, use_case_name):
        file_content = Utils.get_file_content(path_to_usecases + "/" + use_case_name + ".txt")
        return file_content.split('##############################')





