import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from poc.util.fplutil import Utils
from ide.idetheme import DefaultTheme
from ide.CustomNotebook import CustomNotebook
from ide.FrameWithLineNumbers import FrameWithLineNumbers
from ide.StatusBar import StatusBar
from ide.SettingsDialog import SettingsDialog
from poc import fplinterpreter
from ide.Settings import Settings
import configparser
import os


class FplIde:
    """
    config = None
    _theme = None
    window = None
    _panedWindow = None
    _panedMain = None
    _object_browser_tree = None
    _panedWindowMainVertical = None
    _panedWindowVertical = None
    _panedWindowEditor = None
    _tabEditor = None
    _panedWindowBelowEditor = None
    _tabControl = None
    _frameErrors = None
    _frameSyntax = None
    _frameSemantics = None
    _frameOutput = None
    _listBoxErrors = None
    _listBoxSyntax = None
    _listBoxSemantics = None
    _menuBar = None
    """

    def __init__(self):
        self._version = '1.2.5'
        self._theme = DefaultTheme()
        self.window = tk.Tk()
        self.window.call('encoding', 'system', 'utf-8')
        self.window.resizable()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (1024 / 2))
        y_cordinate = int((screen_height / 2) - (768 / 2))
        self.window.geometry("{}x{}+{}+{}".format(1024, 768, x_cordinate, y_cordinate))
        self.window.title('Formal Proving Language IDE (' + self._version + ')')
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.images = dict()
        self._root_dir = os.path.dirname(__file__) + "/"
        self.images["warning"] = tk.PhotoImage("warning", file=os.path.join(self._root_dir, "assets/warning.png"))
        self.images["cancel"] = tk.PhotoImage("cancel", file=os.path.join(self._root_dir, "assets/cancel.png"))
        self.config_init()
        self.__add_paned_windows()
        self.__add_menu()
        self._all_editors = dict()
        self.current_file = ""
        self.window.config(cursor="wait")
        self._statusBar.set_status_text('Initiating FPL parser... Please wait!')
        u = Utils()
        self.fpl_interpreter = fplinterpreter.FplInterpreter(u.get_parser("../grammar/fpl_tatsu_format.ebnf"))
        self._statusBar.set_status_text("FPL parser ready.")
        self.window.config(cursor="")
        self.window.mainloop()

    def get_version(self):
        return self._version

    def __add_menu(self):
        self._menuBar = tk.Menu(self.window)

        file_bar = tk.Menu(self._menuBar, tearoff=0)
        file_bar.add_command(label='New', underline=0, command=self.new_file)
        file_bar.add_command(label='Open', underline=0, command=self.open_file)
        file_bar.add_command(label='Save', underline=0, command=self.save_file)
        file_bar.add_command(label='Save As', underline=6, command=self.save_file_as)
        file_bar.add_command(label='Exit', underline=1, command=self.exit)
        self._menuBar.add_cascade(label='File', underline=0, menu=file_bar)

        build_bar = tk.Menu(self._menuBar, tearoff=0)
        build_bar.add_command(label='Build', command=self.build_fpl_code)
        self._menuBar.add_cascade(label='Build', underline=0, menu=build_bar)

        options_bar = tk.Menu(self._menuBar, tearoff=0)
        options_bar.add_command(label='Settings', command=self.settings)
        self._menuBar.add_cascade(label='Options', underline=0, menu=options_bar)

        help_bar = tk.Menu(self._menuBar, tearoff=0)
        help_bar.add_command(label='About', command=self.about)
        self._menuBar.add_cascade(label='Help', underline=0, menu=help_bar)

        self.window.bind_all('<Control-Key-n>', self.new_file)
        self.window.bind_all('<Control-Key-o>', self.open_file)
        self.window.bind_all('<Control-Key-S>', self.save_file)
        self.window.bind_all('<Control-Key-s>', self.save_file_as)
        self.window.bind_all('<Control-Key-x>', self.exit)
        self.window.config(menu=self._menuBar)

    def __add_paned_windows(self):
        self._panedWindow = tk.PanedWindow(self.window)
        self._panedWindow.pack(expand=True, fill="both")

        self._panedWindowMainVertical = ttk.Frame(self._panedWindow)
        self._panedWindowMainVertical.pack(expand=True, fill="both")

        self._panedWindowMainVertical = tk.PanedWindow(self.window, orient=tk.VERTICAL)
        self._panedWindow.add(self._panedWindowMainVertical)

        style = ttk.Style(self._panedWindowMainVertical)
        style.configure('TNotebook', tabposition='wn', background=self._theme.get_bg_color())
        self.__add_object_browser_treeview()
        self.__add_vertical_paned_window()

    def __add_object_browser_treeview(self):
        self._panedMain = tk.PanedWindow(self.window)
        self._object_browser_tree = ttk.Treeview(self._panedMain, show='headings')
        self._object_browser_tree["columns"] = ("object")
        self._object_browser_tree.column("object", width=270, minwidth=270, stretch=tk.YES)
        self._object_browser_tree.heading("object", text="Object Browser", anchor=tk.W)
        self._object_browser_tree.insert("", 0, "TODO", text="item")
        self._panedMain.add(self._object_browser_tree)
        self._statusBar = StatusBar(self._panedWindowMainVertical)
        self._panedWindowMainVertical.add(self._panedMain)
        self._panedWindowMainVertical.add(self._statusBar, minsize=20, stretch="always")

    def __add_vertical_paned_window(self):
        self._panedWindowVertical = tk.PanedWindow(self.window, orient=tk.VERTICAL)
        self._panedMain.add(self._panedWindowVertical)

        self._panedWindowEditor = tk.PanedWindow(self._panedWindowVertical, heigh=570)
        self._panedWindowEditor.config(bg=self._theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowEditor)

        style = ttk.Style()
        style.theme_create('TNotebook', settings=self._theme.get_notebook_style())
        style.theme_use('TNotebook')
        self._tabEditor = CustomNotebook(self, self._panedWindowEditor)
        self._panedWindowEditor.add(self._tabEditor)

        self._panedWindowBelowEditor = tk.PanedWindow(self._panedWindowVertical, heigh=70,
                                                      bg=self._theme.get_bg_color())
        self._panedWindowBelowEditor.config(bg=self._theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowBelowEditor)
        self.__add_info_boxes()

    def __add_info_boxes(self):
        self._tabControl = ttk.Notebook(self._panedWindowBelowEditor)

        self.__add_error_info_box()

        self._frameSyntax = ttk.Frame(self._tabControl)
        self._listBoxSyntax = ttk.Treeview(self._frameSyntax, selectmode='browse', show='headings')
        self._listBoxSyntax["columns"] = ("rule", "line", "col", "pos", "file")
        self._listBoxSyntax.column("rule", width=170, minwidth=170, stretch=tk.YES, anchor=tk.W)
        self._listBoxSyntax.column('line', width=30, minwidth=50, stretch=tk.YES, anchor=tk.E)
        self._listBoxSyntax.column('col', width=30, minwidth=50, stretch=tk.YES, anchor=tk.E)
        self._listBoxSyntax.column('pos', width=30, minwidth=50, stretch=tk.YES, anchor=tk.E)
        self._listBoxSyntax.column('file', width=100, minwidth=100, stretch=tk.YES, anchor=tk.W)
        self._listBoxSyntax.heading("rule", text="Grammar Rule", anchor=tk.CENTER)
        self._listBoxSyntax.heading("line", text="Line", anchor=tk.CENTER)
        self._listBoxSyntax.heading("col", text="Column", anchor=tk.CENTER)
        self._listBoxSyntax.heading("pos", text="Position", anchor=tk.CENTER)
        self._listBoxSyntax.heading("file", text="File", anchor=tk.CENTER)
        self._listBoxSyntax.bind('<Button-1>', self.__listbox_syntax_item_clicked)
        self.__add_scrollbar(self._frameSyntax, self._listBoxSyntax)
        self._listBoxSyntax.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._frameSemantics = ttk.Frame(self._tabControl)
        self._listBoxSemantics = tk.Listbox(self._frameSemantics)
        self._listBoxSemantics.config(bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._listBoxSemantics.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.__add_scrollbar(self._frameSemantics, self._listBoxSemantics)

        self._frameOutput = ttk.Frame(self._tabControl)
        self._frameOutput.config()

        self._tabControl.add(self._gridErrors, text='Error List')
        self._tabControl.add(self._frameSyntax, text='Syntax Browser')
        self._tabControl.add(self._frameSemantics, text='Semantics Browser')
        self._tabControl.add(self._frameOutput, text='Output')

        self._tabControl.pack(expand=True, fill="both")

    def __add_error_info_box(self):
        self._gridErrors = ttk.Frame(self._tabControl)
        self._gridErrors.pack(expand=True, fill="both")

        # number of errors label
        self._label_error_num = tk.Label(self._gridErrors, text="Errors (0)",
                                         relief=tk.GROOVE, bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._label_error_num.grid()
        self._label_error_num["compound"] = tk.LEFT
        self._label_error_num["image"] = self.images["cancel"]
        self._label_error_num.grid(row=0, column=0, sticky=tk.W + tk.E, pady=2)

        # number of warnings label
        self._label_warning_num = tk.Label(self._gridErrors, text="Warnings (0)",
                                           relief=tk.GROOVE, bg=self._theme.get_bg_color(),
                                           fg=self._theme.get_fg_color())
        self._label_warning_num.grid()
        self._label_warning_num["compound"] = tk.LEFT
        self._label_warning_num["image"] = self.images["warning"]
        self._label_warning_num.grid(row=0, column=1, sticky=tk.W + tk.E, pady=2)

        # option menue for filtering all or current file errors
        self._all_file_list = ["All", "Current File"]
        self._all_file_option_menu = tk.OptionMenu(self._gridErrors,
                                                   tk.StringVar(self._gridErrors, value="All"),
                                                   *self._all_file_list)
        self._all_file_option_menu.config(relief=tk.GROOVE,
                                          bg=self._theme.get_bg_color(),
                                          highlightbackground=self._theme.get_bg_color(),
                                          fg=self._theme.get_fg_color())
        self._all_file_option_menu.grid(row=0, column=2, sticky=tk.W + tk.E, pady=2)

        # option menue for filtering the error type
        self._error_type_list = ["(no types)"]
        self._error_type_option_menu = tk.OptionMenu(self._gridErrors,
                                                     tk.StringVar(self._gridErrors, value="(no types)"),
                                                     *self._error_type_list)
        self._error_type_option_menu.config(relief=tk.GROOVE,
                                            bg=self._theme.get_bg_color(),
                                            highlightbackground=self._theme.get_bg_color(),
                                            fg=self._theme.get_fg_color())
        self._error_type_option_menu.grid(row=0, column=3, sticky=tk.W + tk.E, pady=2)

        # make the infos stretch with the window
        tk.Grid.columnconfigure(self._gridErrors, 0, weight=1)
        tk.Grid.columnconfigure(self._gridErrors, 1, weight=1)
        tk.Grid.columnconfigure(self._gridErrors, 2, weight=50)
        tk.Grid.columnconfigure(self._gridErrors, 3, weight=50)
        self._frameErrors = ttk.Frame(self._gridErrors)
        self._frameErrors.grid(row=1, column=0, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)
        tk.Grid.rowconfigure(self._gridErrors, 0, weight=1)
        tk.Grid.rowconfigure(self._gridErrors, 1, weight=100)

        self._listBoxErrors = ttk.Treeview(self._frameErrors, selectmode='browse',
                                           column=('Type', 'Message', 'Line', 'Column', 'File'))
        # self._listBoxErrors["columns"] = ("#0", "#1", "#2", "#3", "#4", "#5")
        self._listBoxErrors.heading("#0", text="", anchor=tk.W)
        self._listBoxErrors.heading("#1", text="Type", anchor=tk.W)
        self._listBoxErrors.heading("#2", text="Message", anchor=tk.W)
        self._listBoxErrors.heading("#3", text="Line", anchor=tk.E)
        self._listBoxErrors.heading("#4", text="Column", anchor=tk.E)
        self._listBoxErrors.heading("#5", text="File", anchor=tk.CENTER)
        self._listBoxErrors.column('#0', width=40, minwidth=40, stretch=tk.NO, anchor=tk.W)
        self._listBoxErrors.column('Type', width=170, minwidth=170, stretch=tk.YES, anchor=tk.W)
        self._listBoxErrors.column('Message', width=170, minwidth=170, stretch=tk.YES, anchor=tk.W)
        self._listBoxErrors.column('Line', width=30, minwidth=30, stretch=tk.YES, anchor=tk.E)
        self._listBoxErrors.column('Column', width=30, minwidth=30, stretch=tk.YES, anchor=tk.E)
        self._listBoxErrors.column('File', width=100, minwidth=100, stretch=tk.YES, anchor=tk.CENTER)
        self._listBoxErrors.bind('<Button-1>', self.__listbox_error_clicked)
        self.__add_scrollbar(self._frameErrors, self._listBoxErrors)
        self._listBoxErrors.pack(expand=True, fill=tk.BOTH)

    def __add_scrollbar(self, frame, widget):
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        scrollbar.config(command=widget.yview)

    def __listbox_syntax_item_clicked(self, event):
        """
        When the user clicks the syntax item, then the editor cursor will go to the position where the
        parsed item is located.
        :param event:
        :return:
        """
        record = self.__identify_clicked_treeview_item(self._listBoxSyntax)
        if record is not None:
            self.__set_position_in_editor(record[1], record[2], record[4])

    def __listbox_error_clicked(self, event):
        """
        When the user clicks the error item, then the editor cursor will go to the position where the
        error is located.
        :param event:
        :return:
        """
        record = self.__identify_clicked_treeview_item(self._listBoxErrors)
        if record is not None:
            self.__set_position_in_editor(record[2], record[3], record[4])

    def __identify_clicked_treeview_item(self, tree_view):
        """
        Try to identify the clicked treeview item.
        :param tree_view: tree view object
        :return: None if failure, or tuple of clicked values
        """
        currItem = tree_view.focus()
        if currItem == "":
            # for some reason, some clicks do not focus the item but ''. In this case try to select the first one
            all_children = tree_view.get_children()
            if len(all_children) > 0:
                currItem = tree_view.get_children()[0]
            else:
                # return nothing
                return None
        tree_view.selection_set(currItem)
        tree_view.focus(currItem)
        item = tree_view.item(currItem)
        return item['values']

    def __set_position_in_editor(self, line: int, column: int, file: str):
        editor_frame = self._tabEditor.select_file(file)
        self._panedWindowEditor.focus_set()
        self._panedWindowVertical.focus_set()
        self._panedWindowEditor.focus_set()
        self._tabEditor.focus_set()
        editor_frame.focus_set()
        editor_frame.set_pos(line, column)

    def update_error_warning_counts(self):
        """
        Update the counts in the IDE depending on the error list
        :return: None
        """
        error_num_label = self.get_error_number()
        warning_num_label = self.get_warning_number()
        tree_view = self.get_error_list()
        error_num = 0
        warning_num = 0
        for i in tree_view.get_children():
            item = tree_view.item(i)
            if type(item['image']) is list:
                if item['image'][0] == 'warning':
                    warning_num += 1
                elif item['image'][0] == 'cancel':
                    error_num += 1
        error_num_label.config(text="Errors (" + str(error_num) + ")")
        warning_num_label.config(text="Warnings (" + str(warning_num) + ")")

    @staticmethod
    def remove_items_from_tree_view(tree_view, column, file_name):
        """
        Removes the items from tree view depending on the open file
        :param tree_view: Tree view object
        :param column: Column of the tree view with the name of the file
        :param file_name: Name of the file to search in the column
        :return: None
        """
        for i in tree_view.get_children():
            item = tree_view.item(i)
            if item['values'][column] == file_name:
                tree_view.delete(i)

    def refresh_info(self, interpreter: fplinterpreter.FplInterpreter, editor_info: FrameWithLineNumbers):
        """
        Refreshes all information based on the current interpreter like errors, warnings, and syntax tree
        :param interpreter: Current interpreter
        :param editor_info: Current editor info
        :return: None
        """
        self._refresh_items_tree_view(editor_info, interpreter.get_errors(), self.get_error_list(), column=4)
        self._refresh_items_tree_view(editor_info, interpreter.get_ast_list(), self.get_syntax_list(), column=4)

    def _refresh_items_tree_view(self, editor_info: FrameWithLineNumbers, tuple_list: list, tree_view: ttk.Treeview,
                                 column: int):
        # delete all old items in tree_view that belong to the current interpreter, i.e. have its name
        self.remove_items_from_tree_view(tree_view, column, editor_info.title)
        # insert new items (if any) in tree_view
        for item in tuple_list:
            if item.mainType == "E":
                im = self.images["cancel"]
            else:
                im = self.images["warning"]
            item_tuple = item.to_tuple() + (editor_info.title,)
            tree_view.insert("", tk.END, text="", image=im, values=item_tuple)

        self.update_error_warning_counts()

    def build_fpl_code(self):
        messagebox.showinfo("FPL", "Not implemented yet! (Build)")

    def settings(self):
        settings_dialog = SettingsDialog(self)

    def about(self):
        messagebox.showinfo("FPL",
                            "IDE for the Formal Proving Language (FPL), Version " + self._version +
                            "\n\n" + u"\u00A9" + " All Rights Reserved")

    def new_file(self, event=None):
        self._tabEditor.new_file(event)

    def open_file(self, event=None):
        self._tabEditor.open_file(event)

    def save_file(self, event=None):
        self._tabEditor.save_file(event)

    def save_file_as(self, event=None):
        self._tabEditor.save_file_as(event)

    def exit(self, event=None):
        book = self._tabEditor.get_files()
        at_least_one_open_file_changed = False
        for file in book:
            if book[file].text.is_dirty:
                at_least_one_open_file_changed = True
                self._tabEditor.select_file(file)
                msg = messagebox.askyesnocancel("Quit FPLIDE",
                                                "Do you want to save changes of the file " + file + " before quitting?",
                                                icon='warning')
                if msg:
                    # the user does not want to reopen the file, just select the tab!
                    self.save_file(None)
                elif msg is None:
                    # do nothing
                    return
        if not at_least_one_open_file_changed:
            # if no message boxes were answered yet, ask if the user really want's to quit the application
            msg = messagebox.askyesnocancel("Quit FPLIDE",
                                            "Do you want quit the application?",
                                            icon='warning')
            if not msg or msg is None:
                # do nothing
                return
            else:
                self.window.destroy()
        else:
            self.window.destroy()

    def config_init(self):
        """
        Initialise the config (file) of this IDE. If the values in the ini-file are invalid, they will be overwritten
        with valid default values
        :return: None
        """
        self.config = configparser.RawConfigParser()
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
                valid_value = os.path.dirname(__file__) + "/"
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

    def _check_config_section(self, section: str):
        """
        Checks if the current config file has all necessary settings.
        If not, they will be complemented
        :param section: name of the config section
        :return: None
        """

    def get_status_bar(self):
        return self._statusBar

    def get_error_list(self):
        return self._listBoxErrors

    def get_syntax_list(self):
        return self._listBoxSyntax

    def get_editor_notebook(self):
        return self._tabEditor

    def get_warning_number(self):
        return self._label_warning_num

    def get_error_number(self):
        return self._label_error_num


if __name__ == "__main__":
    ide = FplIde()
