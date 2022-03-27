# adapted from https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
# by Bryan Oakley

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ide.FrameWithLineNumbers import FrameWithLineNumbers
from ide.idetheme import DefaultTheme
from ide.Settings import Settings
import io


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""


    def __init__(self, ide, *args, **kwargs):
        self.ide = ide
        self.main_theory_file = ""
        if not hasattr(self, "__initialized"):
            self.__initialize_custom_style()
            self.__inititialized = True
            self.images = None
            self._my_files = dict()
            self._current_file = ""
            self._theme = DefaultTheme()
            self._active = None
        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)
        self.bind("<ButtonPress-1>", self.on_close_press)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind('<<NotebookTabChanged>>', self.tab_changed)
        self.__initialized = False

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
        self.ide.remove_items_from_tree_view(self.ide.get_error_list(), 4, editor_info.title)
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
        try:
            editor_info = self.get_current_file_object()
            editor_info.on_change(None)  # reset the status bar and other info according to to tab
        except tk.TclError:
            self.ide.get_status_bar().set_status_text("")
            pass

    def save_file(self, event=None):
        editor_info = self.get_current_file_object()
        path_to_fpl_theories = self.ide.config.get(Settings.section_paths, Settings.option_paths_fpl_theories)
        if path_to_fpl_theories == '':
            return self.save_file_as()
        elif editor_info.is_new:
            return self.save_file_as()
        with io.open(path_to_fpl_theories, 'w', encoding="UTF-8") as file:
            code = editor_info.get_text()
            file.write(code)
            # change the appearance of the tab to "unchanged"
            self.tab(editor_info, text=editor_info.title)
            # reset the initial value to the new value
            editor_info.text.init_value(editor_info.get_text())
            editor_info.is_new = False

    def save_file_as(self, event=None):
        editor_info = self.get_current_file_object()
        path = asksaveasfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')],
                                 initialfile=editor_info.title)
        if path == "":
            # cancel clicked
            return
        with io.open(path, 'w', encoding="UTF-8") as file:
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
        path_to_fpl_theories = self.ide.config.get(Settings.section_paths, Settings.option_paths_fpl_theories)
        path = askopenfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')],
                               initialdir=path_to_fpl_theories)
        if path == "":
            # cancel clicked
            return
        with open(path, 'r', encoding="UTF-8") as file:
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
        """
        if self.main_theory_file == "":
            self.main_theory_file = self._current_file
        else:
            # There is the main FPL theory loaded already. Therefore, check if the to-be-opened file
            # is part of the symbol table.
            fpl_file_node = AuxSymbolTable.get_library_by_filename(self._symbol_table_root, self._current_file)
            if fpl_file_node is None:
                # The to-be-opened file is not part of the theory.
        """
        # this is a new file that is not already open yet. Create a new tab content
        editor_info = FrameWithLineNumbers(self, self._current_file)
        # set the text
        editor_info.set_text(code)
        # pack the frame
        editor_info.pack(expand=True, fill="both")
        # remember the object
        self._my_files[self._current_file] = editor_info
        # add the object to the tab
        self.add(editor_info, text=self._current_file)
        # and select the tab
        self.select(editor_info)
        # interpret the file
        # get the transformer, highlight the code, refresh all info
        editor_info.parse_interpret_highlight_update_all()
        self.ide.window.config(cursor="")

    def get_current_file_object(self) -> FrameWithLineNumbers:
        self._current_file = self.tab(self.select(), "text")
        if self._current_file[-1] == "*":
            # remove the '*' of any changed files to find the file in the dictionary
            self._current_file = self._current_file[:-1]
        if self._current_file in self._my_files:
            return self._my_files[self._current_file]
        else:
            return None

    def get_files(self):
        return self._my_files

    def select_file(self, file):
        if file in self._my_files:
            self._current_file = file
            self.select(self._my_files[file])
            return self._my_files[file]
        else:
            return None

    def get_line(self):
        return self.__line

    def get_col(self):
        return self.__col

    def get_type(self):
        return self.__type

    def get_msg(self):
        return self.__msg

    def get_parent(self):
        return self.ide

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
