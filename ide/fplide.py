import tkinter as tk
from tkinter import ttk
from ide.idetheme import DefaultTheme
from ide.fplidemenu import FPLIdeMenus
from ide.CustomNotebook import CustomNotebook
from ide.FrameWithLineNumbers import FrameWithLineNumbers
from ide.StatusBar import StatusBar
from ide.IdeModel import IdeModel
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from ide.ObjectBrowser import ObjectBrowser
from poc.util.fplutil import Utils


class FplIde:

    def __init__(self):
        self.ide_version = '1.6.6'
        self._theme = DefaultTheme()
        self.window = tk.Tk()
        self.window.call('encoding', 'system', 'utf-8')
        self.window.resizable()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (1024 / 2))
        y_cordinate = int((screen_height / 2) - (768 / 2))
        self.window.geometry("{}x{}+{}+{}".format(1024, 768, x_cordinate, y_cordinate))
        self.window.title('Formal Proving Language IDE (' + self.ide_version + ')')
        self.window.state('zoomed')
        self.model = IdeModel()
        self.__add_paned_windows()
        self.menus = FPLIdeMenus(self)
        self.window.mainloop()

    def get_version(self):
        return self.ide_version

    def __add_paned_windows(self):
        self._panedWindow = tk.PanedWindow(self.window)
        self._panedWindow.pack(expand=True, fill=tk.BOTH)

        self._panedWindowMainVertical = ttk.Frame(self._panedWindow)
        self._panedWindowMainVertical.pack(expand=True, fill=tk.BOTH)

        self._panedWindowMainVertical = tk.PanedWindow(self.window, orient=tk.VERTICAL)
        self._panedWindow.add(self._panedWindowMainVertical)

        style = ttk.Style(self._panedWindowMainVertical)
        style.configure('TNotebook', tabposition='wn', background=self._theme.get_bg_color())
        self.__add_object_browser_treeview()
        self.__add_vertical_paned_window()

    def __add_object_browser_treeview(self):
        self._panedMain = tk.PanedWindow(self.window)
        self.object_browser = ObjectBrowser(self._panedMain, self)
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

        self._frameDebug = ttk.Frame(self._tabControl)
        self._frameDebug.config()

        self._tabControl.add(self._gridErrors, text='Error List')
        self._tabControl.add(self._frameDebug, text='Debug')

        self._tabControl.pack(expand=True, fill=tk.BOTH)

    def __add_error_info_box(self):
        self._gridErrors = ttk.Frame(self._tabControl)
        self._gridErrors.pack(expand=True, fill=tk.BOTH)

        # number of errors label
        self._label_error_num = tk.Label(self._gridErrors, text="Errors (0)",
                                         relief=tk.GROOVE, bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._label_error_num.grid()
        self._label_error_num["compound"] = tk.LEFT
        self._label_error_num["image"] = self.model.images["cancel"]
        self._label_error_num.grid(row=0, column=0, sticky=tk.W + tk.E, pady=2)

        # number of warnings label
        self._label_warning_num = tk.Label(self._gridErrors, text="Warnings (0)",
                                           relief=tk.GROOVE, bg=self._theme.get_bg_color(),
                                           fg=self._theme.get_fg_color())
        self._label_warning_num.grid()
        self._label_warning_num["compound"] = tk.LEFT
        self._label_warning_num["image"] = self.model.images["warning"]
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

        # option menu for filtering the error type
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

        self._tree_view_errors = ttk.Treeview(self._frameErrors, selectmode='browse',
                                              column=('Type', 'Message', 'Line', 'Column', 'File'))
        # self._tree_view_errors["columns"] = ("#0", "#1", "#2", "#3", "#4", "#5")
        self._tree_view_errors.heading("#0", text="", anchor=tk.W)
        self._tree_view_errors.heading("#1", text="Code", anchor=tk.W)
        self._tree_view_errors.heading("#2", text="Message", anchor=tk.W)
        self._tree_view_errors.heading("#3", text="Line", anchor=tk.E)
        self._tree_view_errors.heading("#4", text="Column", anchor=tk.E)
        self._tree_view_errors.heading("#5", text="File", anchor=tk.CENTER)
        self._tree_view_errors.column('#0', width=40, minwidth=40, stretch=tk.NO, anchor=tk.W)
        self._tree_view_errors.column('Type', width=40, minwidth=40, stretch=tk.YES, anchor=tk.W)
        self._tree_view_errors.column('Message', width=240, minwidth=240, stretch=tk.YES, anchor=tk.W)
        self._tree_view_errors.column('Line', width=30, minwidth=30, stretch=tk.YES, anchor=tk.E)
        self._tree_view_errors.column('Column', width=30, minwidth=30, stretch=tk.YES, anchor=tk.E)
        self._tree_view_errors.column('File', width=100, minwidth=100, stretch=tk.YES, anchor=tk.CENTER)
        self._tree_view_errors.bind('<Double-Button-1>', self.__tree_view_error_clicked)
        self.__add_scrollbar(self._frameErrors, self._tree_view_errors)
        self._tree_view_errors.pack(expand=True, fill=tk.BOTH)

    def __add_scrollbar(self, frame, widget):
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        scrollbar.config(command=widget.yview)

    def __tree_view_error_clicked(self, event):
        """
        When the user clicks the error item, then the editor cursor will go to the position where the
        error is located.
        :param event:
        :return:
        """
        record = Utils.identify_clicked_treeview_item(self._tree_view_errors)
        if record is not None:
            self.set_position_in_editor(record[2], record[3], record[4])

    def set_position_in_editor(self, line: int, column: int, file_name: str):
        editor_info = self._tabEditor.select_file(file_name)
        if file_name not in self._tabEditor.get_files():
            fpl_file = self.model.get_file_by_name(file_name)
            self._tabEditor.set_file(file_name)
            self._tabEditor.add_new_editor(fpl_file.get_file_content())
            editor_info = self._tabEditor.select_file(file_name)
            self.highlight_file(editor_info)

        self._panedWindowVertical.focus_set()
        self._panedWindowEditor.focus_set()
        self._tabEditor.focus_set()
        editor_info.focus_set()
        editor_info.set_pos(line, column)

    def highlight_file(self, editor_info):
        editor_info.reconfigure_all_tags()
        list_of_file_specific_tags = self.model.fpl_interpreter.file_specific_tags[editor_info.title]
        for item in list_of_file_specific_tags:
            editor_info.add_tag(item.tag, item.zfrom, item.zto)
        for error in self.model.fpl_interpreter.get_error_mgr().get_errors():
            if editor_info.title == error.file:
                editor_info.add_error_tag(error.get_tkinter_pos())

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
    def remove_items_from_tree_view(tree_view, column, file_name=None):
        """
        Removes the items from tree view depending on the open file
        :param tree_view: Tree view object
        :param column: Column of the tree view with the name of the file
        :param file_name: Name of the file to search in the column
        :return: None
        """
        if file_name is None:
            tree_view.delete(*tree_view.get_children())
        else:
            for i in tree_view.get_children():
                item = tree_view.item(i)
                if item['values'][column] == file_name:
                    tree_view.delete(i)

    def refresh_info(self, editor_info: FrameWithLineNumbers):
        """
        Refreshes all information based on the current transformer like errors, warnings, and syntax tree
        :param editor_info: Current editor info
        :return: None
        """
        self._refresh_items_tree_view(editor_info, self.model.fpl_interpreter.get_error_mgr().get_errors(),
                                      self.get_error_list(),
                                      column=4)
        if AuxISourceAnalyser.verbose:
            print(self.model.fpl_interpreter.symbol_table_to_str())
        self.object_browser.refresh(self.model.fpl_interpreter.get_symbol_table_root())

    def _refresh_items_tree_view(self, editor_info: FrameWithLineNumbers, set_of_errors: set, tree_view: ttk.Treeview,
                                 column: int):
        # delete all old items in tree_view that belong to the current transformer, i.e. have its name
        self.remove_items_from_tree_view(tree_view, column)
        # convert the set to list to make it sortable and sort it by the sortkey of the error
        list_of_errors = list(set_of_errors)
        list_of_errors.sort(reverse=False, key=lambda x: x.sort_key())
        # insert new items (if any) in tree_view
        for item in list_of_errors:
            if item.mainType == "E":
                im = self.model.images["cancel"]
            else:
                im = self.model.images["warning"]
            item_tuple = item.to_tuple()
            tree_view.insert("", tk.END, text="", image=im, values=item_tuple)
        self.update_error_warning_counts()

    def get_status_bar(self):
        return self._statusBar

    def get_error_list(self):
        return self._tree_view_errors

    def get_editor_notebook(self):
        return self._tabEditor

    def get_warning_number(self):
        return self._label_warning_num

    def get_error_number(self):
        return self._label_error_num

    def rebuild(self):
        self.window.config(cursor="watch")
        self.window.update()
        # clear the symbol table and all errors of the interpreter
        self.clear_theory_metadata()
        main_fpl_file = self.model.get_main_file()
        # make sure the main file is open
        book = self.get_editor_notebook()
        if main_fpl_file.file_name not in book.get_files():
            book.add_new_editor(main_fpl_file.get_source())
        # perform the syntax and semantic analysis for the theory as a whole
        self.model.fpl_interpreter.syntax_analysis(
            self.model.path_to_fpl_root + '\\' + main_fpl_file.file_name)
        self.model.fpl_interpreter.semantic_analysis()
        # refresh all open files of the theory, including the main file
        for file_name in self._tabEditor.get_files():
            editor_info = self._tabEditor.get_files()[file_name]
            self.highlight_file(editor_info)
        self.refresh_info(editor_info)
        self.window.config(cursor="")

    def clear_theory_metadata(self):
        # empty error list
        error_tree_view = self.get_error_list()
        error_tree_view.delete(*error_tree_view.get_children())
        self.update_error_warning_counts()
        # empty object tree
        self.object_browser.clear()
        # clear the symbol table and all errors of the interpreter
        self.model.fpl_interpreter.clear()

if __name__ == "__main__":
    ide = FplIde()
