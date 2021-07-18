from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from util.fplutil import Utils
from idetheme import DefaultTheme
from CustomNotebook import CustomNotebook
from StatusBar import StatusBar
import os


class FplIde:
    fpl_parser = None
    _version = '1.2.0'
    _theme = None
    _window = None
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
    _statusBar = None
    images = None

    def __init__(self):
        self._theme = DefaultTheme()
        self._window = Tk()
        self._window.resizable()
        screen_width = self._window.winfo_screenwidth()
        screen_height = self._window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (1024 / 2))
        y_cordinate = int((screen_height / 2) - (768 / 2))
        self._window.geometry("{}x{}+{}+{}".format(1024, 768, x_cordinate, y_cordinate))
        self._window.title('Formal Proving Language IDE (' + self._version + ')')
        self.images = dict()
        dirname = os.path.dirname(__file__) + "/"
        self.images["warning"] = PhotoImage("warning", file=os.path.join(dirname, "assets/warning.png"))
        self.images["cancel"] = PhotoImage("cancel", file=os.path.join(dirname, "assets/cancel.png"))
        self.__add_paned_windows()
        self.__add_menu()
        self._all_editors = dict()
        self.current_file = ""
        self.fpl_init()
        self._tabEditor.stop_parser_thread = False
        self._window.mainloop()
        self._tabEditor.stop_parser_thread = True

    def get_version(self):
        return self._version

    def __add_menu(self):
        self._menuBar = Menu(self._window)

        file_bar = Menu(self._menuBar, tearoff=0)
        file_bar.add_command(label='Open', command=self.open_file)
        file_bar.add_command(label='Save', command=self.save_file)
        file_bar.add_command(label='Save As', command=self.save_file_as)
        file_bar.add_command(label='Exit', command=exit)
        self._menuBar.add_cascade(label='File', menu=file_bar)

        build_bar = Menu(self._menuBar, tearoff=0)
        build_bar.add_command(label='Build', command=self.build_fpl_code)
        self._menuBar.add_cascade(label='Build', menu=build_bar)

        self._window.config(menu=self._menuBar)

    def __add_paned_windows(self):
        self._panedWindow = PanedWindow(self._window)
        self._panedWindow.pack(expand=True, fill="both")

        self._panedWindowMainVertical = ttk.Frame(self._tabControl)
        self._panedWindowMainVertical.pack(expand=True, fill="both")

        self._panedWindowMainVertical = PanedWindow(self._window, orient=VERTICAL)
        self._panedWindow.add(self._panedWindowMainVertical)

        style = ttk.Style(self._panedMain)
        style.configure('TNotebook', tabposition='wn', background=self._theme.get_bg_color())
        self.__add_object_browser_treeview()
        self.__add_vertical_paned_window()

    def __add_object_browser_treeview(self):
        self._panedMain = PanedWindow(self._window)
        self._object_browser_tree = ttk.Treeview(self._panedMain, show='headings')
        self._object_browser_tree["columns"] = ("object")
        self._object_browser_tree.column("object", width=270, minwidth=270, stretch=YES)
        self._object_browser_tree.heading("object", text="Object Browser", anchor=W)
        self._object_browser_tree.insert("", 0, "TODO", text="item")
        self._panedMain.add(self._object_browser_tree)
        self._statusBar = StatusBar(self._panedWindowMainVertical)
        self._panedWindowMainVertical.add(self._panedMain)
        self._panedWindowMainVertical.add(self._statusBar, minsize=20, stretch="always")

    def __add_vertical_paned_window(self):
        self._panedWindowVertical = PanedWindow(self._window, orient=VERTICAL)
        self._panedMain.add(self._panedWindowVertical)

        self._panedWindowEditor = PanedWindow(self._panedWindowVertical, heigh=570)
        self._panedWindowEditor.config(bg=self._theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowEditor)

        style = ttk.Style()
        style.theme_create('TNotebook', settings=self._theme.get_notebook_style())
        style.theme_use('TNotebook')
        self._tabEditor = CustomNotebook(self, self._panedWindowEditor)
        self._panedWindowEditor.add(self._tabEditor)

        self._panedWindowBelowEditor = PanedWindow(self._panedWindowVertical, heigh=70, bg=self._theme.get_bg_color())
        self._panedWindowBelowEditor.config(bg=self._theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowBelowEditor)
        self.__add_info_boxes()

    def __add_info_boxes(self):
        self._tabControl = ttk.Notebook(self._panedWindowBelowEditor)

        self.__add_error_info_box()

        self._frameSyntax = ttk.Frame(self._tabControl)
        self._listBoxSyntax = ttk.Treeview(self._frameSyntax, selectmode='browse', show='headings')
        self._listBoxSyntax["columns"] = ("rule", "line", "col", "pos", "file")
        self._listBoxSyntax.column("rule", width=170, minwidth=170, stretch=YES, anchor=W)
        self._listBoxSyntax.column('line', width=30, minwidth=50, stretch=YES, anchor=E)
        self._listBoxSyntax.column('col', width=30, minwidth=50, stretch=YES, anchor=E)
        self._listBoxSyntax.column('pos', width=30, minwidth=50, stretch=YES, anchor=E)
        self._listBoxSyntax.column('file', width=100, minwidth=100, stretch=YES, anchor=W)
        self._listBoxSyntax.heading("rule", text="Grammar Rule", anchor=CENTER)
        self._listBoxSyntax.heading("line", text="Line", anchor=CENTER)
        self._listBoxSyntax.heading("col", text="Column", anchor=CENTER)
        self._listBoxSyntax.heading("pos", text="Position", anchor=CENTER)
        self._listBoxSyntax.heading("file", text="File", anchor=CENTER)
        self._listBoxSyntax.bind('<Button-1>', self.__listbox_syntax_item_clicked)
        self.__add_scrollbar(self._frameSyntax, self._listBoxSyntax)
        self._listBoxSyntax.pack(side=LEFT, expand=True, fill=BOTH)

        self._frameSemantics = ttk.Frame(self._tabControl)
        self._listBoxSemantics = Listbox(self._frameSemantics)
        self._listBoxSemantics.config(bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._listBoxSemantics.pack(side=LEFT, expand=True, fill=BOTH)
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
        self._label_error_num = Label(self._gridErrors, text="Errors (0)",
                                      relief=GROOVE, bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._label_error_num.grid()
        self._label_error_num["compound"] = LEFT
        self._label_error_num["image"] = self.images["cancel"]
        self._label_error_num.grid(row=0, column=0, sticky=W + E, pady=2)

        # number of warnings label
        self._label_warning_num = Label(self._gridErrors, text="Warnings (0)",
                                        relief=GROOVE, bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._label_warning_num.grid()
        self._label_warning_num["compound"] = LEFT
        self._label_warning_num["image"] = self.images["warning"]
        self._label_warning_num.grid(row=0, column=1, sticky=W + E, pady=2)

        # option menue for filtering all or current file errors
        self._all_file_list = ["All", "Current File"]
        self._all_file_option_menu = OptionMenu(self._gridErrors,
                                                StringVar(self._gridErrors, value="All"),
                                                *self._all_file_list)
        self._all_file_option_menu.config(relief=GROOVE,
                                          bg=self._theme.get_bg_color(),
                                          highlightbackground=self._theme.get_bg_color(),
                                          fg=self._theme.get_fg_color())
        self._all_file_option_menu.grid(row=0, column=2, sticky=W + E, pady=2)

        # option menue for filtering the error type
        self._error_type_list = ["(no types)"]
        self._error_type_option_menu = OptionMenu(self._gridErrors,
                                                  StringVar(self._gridErrors, value="(no types)"),
                                                  *self._error_type_list)
        self._error_type_option_menu.config(relief=GROOVE,
                                            bg=self._theme.get_bg_color(),
                                            highlightbackground=self._theme.get_bg_color(),
                                            fg=self._theme.get_fg_color())
        self._error_type_option_menu.grid(row=0, column=3, sticky=W + E, pady=2)

        # make the infos stretch with the window
        Grid.columnconfigure(self._gridErrors, 0, weight=1)
        Grid.columnconfigure(self._gridErrors, 1, weight=1)
        Grid.columnconfigure(self._gridErrors, 2, weight=50)
        Grid.columnconfigure(self._gridErrors, 3, weight=50)
        self._frameErrors = ttk.Frame(self._gridErrors)
        self._frameErrors.grid(row=1, column=0, columnspan=4, sticky=W + E + N + S)
        Grid.rowconfigure(self._gridErrors, 0, weight=1)
        Grid.rowconfigure(self._gridErrors, 1, weight=100)

        self._listBoxErrors = ttk.Treeview(self._frameErrors, selectmode='browse',
                                           column=('Type', 'Message', 'Line', 'Column', 'File'))
        # self._listBoxErrors["columns"] = ("#0", "#1", "#2", "#3", "#4", "#5")
        self._listBoxErrors.heading("#0", text="", anchor=W)
        self._listBoxErrors.heading("#1", text="Type", anchor=W)
        self._listBoxErrors.heading("#2", text="Message", anchor=W)
        self._listBoxErrors.heading("#3", text="Line", anchor=E)
        self._listBoxErrors.heading("#4", text="Column", anchor=E)
        self._listBoxErrors.heading("#5", text="File", anchor=CENTER)
        self._listBoxErrors.column('#0', width=40, minwidth=40, stretch=NO, anchor=W)
        self._listBoxErrors.column('Type', width=170, minwidth=170, stretch=YES, anchor=W)
        self._listBoxErrors.column('Message', width=170, minwidth=170, stretch=YES, anchor=W)
        self._listBoxErrors.column('Line', width=30, minwidth=30, stretch=YES, anchor=E)
        self._listBoxErrors.column('Column', width=30, minwidth=30, stretch=YES, anchor=E)
        self._listBoxErrors.column('File', width=100, minwidth=100, stretch=YES, anchor=CENTER)
        self._listBoxErrors.bind('<Button-1>', self.__listbox_error_clicked)
        self.__add_scrollbar(self._frameErrors, self._listBoxErrors)
        self._listBoxErrors.pack(expand=True, fill=BOTH)

    def __add_scrollbar(self, frame, widget):
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
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
            self.__set_position_in_editor(record[1], record[2])

    def __listbox_error_clicked(self, event):
        """
        When the user clicks the error item, then the editor cursor will go to the position where the
        error is located.
        :param event:
        :return:
        """
        record = self.__identify_clicked_treeview_item(self._listBoxErrors)
        if record is not None:
            self.__set_position_in_editor(record[2], record[3])

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

    def __set_position_in_editor(self, line, column):
        editor_frame = self._tabEditor.get_current_file_object()
        self._panedWindowEditor.focus_set()
        self._panedWindowVertical.focus_set()
        self._panedWindowEditor.focus_set()
        self._tabEditor.focus_set()
        editor_frame.focus_set()
        editor_frame.set_pos(line, column)

    def build_fpl_code(self):
        messagebox.showinfo("FPL", "Not implemented yet! (Build)")

    def open_file(self):
        self._tabEditor.open_file()

    def save_file(self):
        self._tabEditor.save_file()

    def save_file_as(self):
        self._tabEditor.save_file_as()

    def fpl_init(self):
        self._statusBar.set_status_text('Initiating FPL parser... Please wait!')
        u = Utils()
        self.fpl_parser = u.get_parser("../grammar/fpl_tatsu_format.ebnf")
        self._statusBar.set_status_text("FPL parser ready.")

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
