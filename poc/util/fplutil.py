import time
import tatsu
import io


class Utils:
    _stopwatch_measurements = dict()
    _stopwatch = time.perf_counter()

    def get_file_content(self, path_to_file):
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
