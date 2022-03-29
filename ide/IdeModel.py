from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.util.fplutil import Utils
import tkinter as tk
import os
import configparser
from ide.Settings import Settings
from poc.fplsourcetransformer import FPLSourceTransformer
from poc.fplinterpreter import FplInterpreter

"""
This class stores the model of the FPL IDE, allowing the communication between different user interactions with the IDE
"""


class IdeModel:
    def __init__(self):
        self._utils = Utils()
        self.config = configparser.RawConfigParser()
        self._root_dir = os.path.dirname(__file__) + "/"
        self._config_init()
        self.path_to_fpl_root = os.path.abspath(
            self.config.get(Settings.section_paths, Settings.option_paths_fpl_theories))
        self.library = AnyNode()
        AnyNode(outline=AuxSymbolTable.library, parent=self.library)
        self._utils.reload_library(self.library, self.path_to_fpl_root)
        self.fpl_parser = self._utils.get_parser("../grammar/fpl_tatsu_format.ebnf")
        self.fpl_source_transformer = FPLSourceTransformer(self.fpl_parser)
        self.fpl_interpreter = FplInterpreter(self.fpl_parser, self.path_to_fpl_root, self.library)
        self.images = dict()
        self.images["warning"] = tk.PhotoImage("warning", file=os.path.join(self._root_dir, "assets/warning.png"))
        self.images["cancel"] = tk.PhotoImage("cancel", file=os.path.join(self._root_dir, "assets/cancel.png"))
        self.theory_is_open_flag = False

    def _config_init(self):
        """
        Initialise the config (file) of this IDE. If the values in the ini-file are invalid, they will be overwritten
        with valid default values
        :return: None
        """
        # check if there is a config file
        path_to_config = os.path.join(self._root_dir, "config.ini")
        if os.path.exists(path_to_config):
            # if so, read the config file
            self.config.read(path_to_config)
        # ensure all mandatory sections and options are set
        if not self.config.has_section(Settings.section_paths):
            self.config.add_section(Settings.section_paths)
        if not self.config.has_option(Settings.section_paths, Settings.option_paths_fpl_theories):
            self.config.set(Settings.section_paths, Settings.option_paths_fpl_theories, os.path.dirname(__file__) + "/")
        else:
            valid_value = self.config.get(Settings.section_paths, Settings.option_paths_fpl_theories)
            if not os.path.isdir(valid_value):
                valid_value = self._root_dir
                self.config.set(Settings.section_paths, Settings.option_paths_fpl_theories, valid_value)

        if not self.config.has_section(Settings.section_editor):
            self.config.add_section(Settings.section_editor)
        if not self.config.has_option(Settings.section_editor, Settings.option_editor_tab_length):
            self.config.set(Settings.section_editor, Settings.option_editor_tab_length, 3)
        else:
            valid_value = self.config.get(Settings.section_editor, Settings.option_editor_tab_length)
            valid_value = Settings.to_positive_integer(valid_value)
            self.config.set(Settings.section_editor, Settings.option_editor_tab_length, valid_value)

        if not self.config.has_section(Settings.section_codereform):
            self.config.add_section(Settings.section_codereform)
        if not self.config.has_option(Settings.section_codereform, Settings.option_codereform_1linecomppred):
            self.config.set(Settings.section_codereform, Settings.option_codereform_1linecomppred, True)
        else:
            valid_value = self.config.get(Settings.section_codereform, Settings.option_codereform_1linecomppred)
            if valid_value not in ["True", "False"]:
                self.config.set(Settings.section_codereform, Settings.option_codereform_1linecomppred, True)

        # make sure, the config file is now complete
        cfgfile = open(path_to_config, "w")
        self.config.write(cfgfile)
