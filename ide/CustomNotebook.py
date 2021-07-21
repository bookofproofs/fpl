# adapted from https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
# by Bryan Oakley

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ide.FrameWithLineNumbers import FrameWithLineNumbers
import time
from poc import fplinterpreter
from threading import *
from idetheme import DefaultTheme


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    images = None
    _theme = None
    __initialized = False
    _ide = None
    _my_files = dict()
    _current_file = ""
    _global_path = ""
    stop_parser_thread = False  # indicates if the thread has to stop
    _milliseconds_idle = 300  # number of milliseconds the _parser_thread is idle
    initial_calm_down_countdown = 2  # number of idle cycles of the _parser_thread to wait
    _status_fpl_parse_and_interpret = dict()  # indicates whether the open files are parsed or interpreted
    _parser_thread = None  # thread object to parse and interpret the open files

    def __init__(self, ide, *args, **kwargs):
        self._ide = ide
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True
            self._my_files = dict()
            self._current_file = ""
            self._global_path = ""
            self.stop_parser_thread = False
            self._parser_thread = Thread(target=self.thread_based_refresh_info_open_files)
            self._parser_thread.start()
            self._theme = DefaultTheme()

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind('<<NotebookTabChanged>>', self.tab_changed)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)
        if len(self._my_files) == 0:
            # prevent handling the event if no files are open
            return
        index = self.index("@%d,%d" % (event.x, event.y))
        if "close" in element:
            editor_info = self.get_current_file_object()

            if editor_info.text.is_dirty:
                msg = tk.messagebox.askquestion("Save File?",
                                                "Do you want to save changes to " + editor_info.title + "?",
                                                icon='warning')
                if msg == 'yes':
                    self.save_file()
                    self._remove_editor_from_ide(editor_info, index)

            else:
                self.state(['pressed'])
                self._active = index
                return "break"

    def _remove_editor_from_ide(self, editor_info: FrameWithLineNumbers, index: int):
        self.forget(index)
        # remove all errors associated with the closed editor
        self.__remove_items_from_tree_view(self._ide.get_error_list(), 4, editor_info.title)
        # remove all errors associated with the closed editor
        self.__remove_items_from_tree_view(self._ide.get_syntax_list(), 4, editor_info.title)
        del self._my_files[editor_info.title]

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            editor_info = self.get_current_file_object()
            self._remove_editor_from_ide(editor_info, index)

        self.state(["!pressed"])
        self._active = None

    def tab_changed(self, event):
        selected_tab = event.widget.select()
        try:
            self._current_file = event.widget.tab(selected_tab, "text")
            self._ide.get_status_bar().set_status_text(selected_tab)
        except tk.TclError:
            self._ide.get_status_bar().set_status_text("")
            pass

    def save_file(self, event=None):
        editor_info = self.get_current_file_object()
        if self._global_path == '':
            return self.save_file_as()
        elif editor_info.is_new:
            return self.save_file_as()
        with open(self._global_path, 'w') as file:
            code = editor_info.get_text()
            file.write(code)
            # change the appearance of the tab to "unchanged"
            self.tab(editor_info, text=editor_info.title)
            # reset the initial value to the new value
            editor_info.text.init_value(editor_info.get_text())

    def save_file_as(self, event=None):
        editor_info = self.get_current_file_object()
        path = asksaveasfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')],
                                 initialfile=os.path.join(self._global_path, editor_info.title))
        if path == "":
            # cancel clicked
            return
        with open(path, 'w') as file:
            code = editor_info.get_text()
            file.write(code)
            # change the appearance of the tab to "unchanged"
            self.tab(editor_info, text=editor_info.title)
            # reset the initial value to the new value
            editor_info.text.init_value(editor_info.get_text())

    def new_file(self, event=None):
        self._current_file = self._generate_new_file_name()
        self._add_new_editor("")

    def _generate_new_file_name(self) -> str:
        file_name = "NewTheory"
        numb = 1
        while file_name + str(numb) + ".fpl" in self._my_files:
            numb += 1
        return file_name + str(numb) + ".fpl"

    def open_file(self, event=None):
        path = askopenfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')])
        if path == "":
            # cancel clicked
            return
        self._global_path = path
        with open(path, 'r') as file:
            self._current_file = os.path.basename(path)
            if self._current_file in self._my_files:
                # do not open the file once again if there is already an open tab
                # instead, check if the already opened file was changed and the user wants to re-open it
                editor_info = self._my_files[self._current_file]
                if editor_info.text.is_dirty:
                    msg = tk.messagebox.askquestion("Re-open File?",
                                                    "You made changes to the file " + editor_info.title + "." +
                                                    "Do you really want to reopen it? " +
                                                    "If you do, the changes you have made will be lost!",
                                                    icon='warning')
                    if msg == 'no':
                        # the user does not want to reopen the file, just select the tab!
                        self.select(editor_info)
                        return
                    else:
                        # the user wants to reopen the file and undo all changes.
                        code = file.read()
                        # reset the text of the tab
                        editor_info.set_text(code)
                        # flag not to interpret the file by the thread, because the main thread will interpret it
                        editor_info.to_be_parsed_and_interpreted = False
                        # interpret the file in the main thread. light=False means, also syntax tree will be recreated
                        self.refresh_info_open_file(editor_info, light=False)
                        # at this point, everything is done
                        return
                else:
                    # the user reopened an already opened file, that is not dirty
                    # in this case, just select it
                    self.select(editor_info)
                    self.tab(editor_info, state="normal")
            else:
                # read the file
                code = file.read()
                self._add_new_editor(code)

    def _add_new_editor(self, code):
        # this is a new file that is not already open yet. Create a new tab content
        editor_info = FrameWithLineNumbers(self, self._current_file)
        # set the text
        editor_info.set_text(code)
        # flag not to interpret the file by the thread, because the main thread will interpret it
        editor_info.to_be_parsed_and_interpreted = False
        # pack the frame
        editor_info.pack(expand=True, fill="both")
        # remember the object
        self._my_files[self._current_file] = editor_info
        # add the object to the tab
        self.add(editor_info, text=self._current_file)
        # and select the tab
        self.select(editor_info)
        # interpret the file in the main thread. light=False means, also syntax tree will be recreated
        self.refresh_info_open_file(editor_info, light=False)

    def get_current_file_object(self) -> FrameWithLineNumbers:
        self._current_file = self.tab(self.select(), "text")
        if self._current_file[-1] == "*":
            # remove the '*' of any changed files to find the file in the dictionary
            self._current_file = self._current_file[:-1]
        if self._current_file in self._my_files:
            return self._my_files[self._current_file]
        else:
            return None

    def get_book(self):
        return self._my_files

    def select_file(self, file):
        if file in self._my_files:
            self._current_file = file
            self.select(self._my_files[file])
            return self._my_files[file]
        else:
            return None

    def refresh_info_open_file(self, editor_info: FrameWithLineNumbers, light=False):
        # flag that the file has not to be reparsed again by the thread since
        editor_info.to_be_parsed_and_interpreted = False
        # get code
        code = editor_info.get_text()
        # parse and interpret it
        interpreter = fplinterpreter.FplInterpreter(editor_info.title, code, self._ide.fpl_parser)
        # refresh error list
        self.__refresh_items_tree_view(editor_info,
                                       interpreter.get_errors(),
                                       self._ide.get_error_list(),
                                       column=4)
        # highlight the code
        self.highlight(editor_info, interpreter.get_ast_list())
        if not light:
            self.__refresh_items_tree_view(editor_info,
                                           interpreter.get_ast_list(),
                                           self._ide.get_syntax_list(),
                                           column=4)

    def thread_based_refresh_info_open_files(self):
        """
        Updates the info lists regarding the code of the open files
        :return:
        """
        while not self.stop_parser_thread:
            for fpl_file in list(self._my_files):
                editor_info = self._my_files[fpl_file]
                if editor_info.calm_down_countdown > 0:
                    editor_info.calm_down_countdown = editor_info.calm_down_countdown - 1
                elif editor_info.to_be_parsed_and_interpreted:
                    self.refresh_info_open_file(editor_info, light=True)

            # sleep to enable the main thread to handle all user events properly
            time.sleep(self._milliseconds_idle / 1000)

    def highlight(self, editor_info: FrameWithLineNumbers, ast_info_list: list):
        """
        Update all tags
        :param editor_info:
        :param ast_info_list:
        :return:
        """
        # reconfigure all tags
        editor_info.reconfigure_all_tags()
        # add new tags
        list_indices = list()
        for item in ast_info_list:
            current_index = str(item.line) + "." + str(item.col)
            list_indices.append(current_index)
            grammar_tags = self._theme.get_grammar_tags()
            # set all the tags for syntax highlighting while the parsed rules are added to the _listBoxSyntax
            if item.rule in grammar_tags:
                tag = grammar_tags[item.rule]
                last_index = current_index
                while len(list_indices) > 0 and last_index == current_index:
                    last_index = list_indices.pop()
                if len(list_indices) == 0:
                    last_index = "1.0"
                editor_info.add_tag(tag, last_index, current_index)

    def __refresh_items_tree_view(self, editor_info: FrameWithLineNumbers,
                                  tuple_list: list,
                                  tree_view: ttk.Treeview,
                                  column: int):
        # delete all old items in tree_view that belong to the current interpreter, i.e. have its name
        self.__remove_items_from_tree_view(tree_view, column, editor_info.title)
        # insert new items (if any) in tree_view
        for item in tuple_list:
            if item.mainType == "E":
                im = self._ide.images["cancel"]
            else:
                im = self._ide.images["warning"]
            item_tuple = item.to_tuple() + (editor_info.title,)
            tree_view.insert("", tk.END, text="", image=im, values=item_tuple)

        self.__update_error_warning_numbers()

    def __update_error_warning_numbers(self):
        error_num_label = self._ide.get_error_number()
        warning_num_label = self._ide.get_warning_number()
        tree_view = self._ide.get_error_list()
        error_num = 0
        warning_num = 0
        for id in tree_view.get_children():
            item = tree_view.item(id)
            if type(item['image']) is list:
                if item['image'][0] == 'warning':
                    warning_num += 1
                elif item['image'][0] == 'cancel':
                    error_num += 1
        error_num_label.config(text="Errors (" + str(error_num) + ")")
        warning_num_label.config(text="Warnings (" + str(warning_num) + ")")

    def get_line(self):
        return self.__line

    def get_col(self):
        return self.__col

    def get_type(self):
        return self.__type

    def get_msg(self):
        return self.__msg

    @staticmethod
    def __remove_items_from_tree_view(tree_view, column, file_name):
        for id in tree_view.get_children():
            item = tree_view.item(id)
            if item['values'][column] == file_name:
                tree_view.delete(id)

    def get_parent(self):
        return self._ide

    def __initialize_custom_style(self):
        style = ttk.Style()
        # dirname = os.path.dirname(__file__) + "/"

        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=10, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            (
                "CustomNotebook.tab", {
                    "sticky": "nswe",
                    "children": [
                        ("CustomNotebook.padding", {
                            "side": "top",
                            "sticky": "nswe",
                            "children": [
                                ("CustomNotebook.focus", {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                        ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                    ]
                                })
                            ]
                        })
                    ]
                }
            )
        ])
