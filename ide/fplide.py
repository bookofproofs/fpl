from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
from tkinter import messagebox
import os
from ide.linenumbers import FrameWithLineNumbers
from poc import fplinterpreter
from util.fplutil import Utils
from idetheme import Theme


class StatusBar(PanedWindow):
    _labelText = ""
    _current_editor_tab = ""

    def __init__(self, master):
        theme = Theme()
        PanedWindow.__init__(self, master)
        self.config(bg=theme.get_bg_color())
        self.variable = StringVar()
        self.label = Label(self, bd=0, relief=SUNKEN, anchor=W,
                           bg=theme.get_bg_color(), fg=theme.get_fg_color(),
                           textvariable=self.variable,
                           font=('consolas', 10, 'normal'))
        self.variable.set('Status Bar')
        self.label.pack(fill=X)
        self.pack()

    def set_editor_tab(self, editor_tab):
        self._current_editor_tab = editor_tab

    def text(self, value):
        self.variable.set(self._current_editor_tab + " " + value)


class FplIde:
    _version = '1.1.0'
    fpl_parser = None
    _theme = None
    _global_path = ''
    _window = None
    _panedWindow = None
    _panedMain = None
    _theories_tree = None
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
    _all_editors = dict()
    _current_file = None
    _statusBar = None

    def __init__(self):
        self._theme = Theme()
        self._window = Tk()
        self._window.minsize(1024, 768)
        self._window.title('Formal Proving Language IDE (' + self._version + ')')
        self.__add_paned_windows()
        self.__add_menu()
        self._all_editors = dict()
        self._current_file = ""
        self.fpl_init()
        self._window.mainloop()

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

        self._panedWindowMainVertical = PanedWindow(self._window, orient=VERTICAL)
        self._panedWindow.add(self._panedWindowMainVertical)

        style = ttk.Style(self._panedMain)
        style.configure('TNotebook', tabposition='wn', background=self._theme.get_bg_color())
        self.__add_treeview()
        self.__add_vertical_paned_window()

    def __add_treeview(self):
        self._panedMain = PanedWindow(self._window)
        style = ttk.Style(self._panedMain)
        style.theme_use("classic")
        style.configure("Treeview", background=self._theme.get_bg_color(), fieldbackground=self._theme.get_bg_color(),
                        foreground=self._theme.get_fg_color())
        self._theories_tree = ttk.Treeview(self._panedMain, show='headings')
        self._theories_tree["columns"] = ("object")
        self._theories_tree.column("object", width=270, minwidth=270, stretch=YES)
        self._theories_tree.heading("object", text="Object Browser", anchor=W)
        self._theories_tree.insert("", 0, "TODO", text="item")
        self._panedMain.add(self._theories_tree)
        self._statusBar = StatusBar(self._panedWindowMainVertical)
        self._panedWindowMainVertical.add(self._panedMain)
        self._panedWindowMainVertical.add(self._statusBar, minsize=20, stretch="always")

    def __add_vertical_paned_window(self):
        self._panedWindowVertical = PanedWindow(self._window, orient=VERTICAL)
        self._panedMain.add(self._panedWindowVertical)

        self._panedWindowEditor = PanedWindow(self._panedWindowVertical, heigh=570)
        self._panedWindowEditor.config(bg=self._theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowEditor)

        self._tabEditor = ttk.Notebook(self._panedWindowEditor, style='TNotebook')
        self._panedWindowEditor.add(self._tabEditor)

        self._panedWindowBelowEditor = PanedWindow(self._panedWindowVertical, heigh=70)
        self._panedWindowBelowEditor.config(bg=self._theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowBelowEditor)
        self.__add_info()

    def __add_info(self):
        self._tabControl = ttk.Notebook(self._panedWindowBelowEditor, style='TNotebook')
        self._tabControl.config()

        self._frameErrors = ttk.Frame(self._tabControl)
        self._listBoxErrors = ttk.Treeview(self._frameErrors, show='headings')
        self._listBoxErrors["columns"] = ("type", "exception", "message", "line", "col", "file")
        self._listBoxErrors.column("type", width=15, minwidth=50, stretch=NO, anchor=CENTER)
        self._listBoxErrors.column('exception', width=170, minwidth=170, stretch=YES, anchor=W)
        self._listBoxErrors.column('message', width=170, minwidth=170, stretch=YES, anchor=W)
        self._listBoxErrors.column('line', width=30, minwidth=50, stretch=YES, anchor=E)
        self._listBoxErrors.column('col', width=30, minwidth=50, stretch=YES, anchor=E)
        self._listBoxErrors.column('file', width=100, minwidth=100, stretch=YES, anchor=W)
        self._listBoxErrors.heading("type", text="", anchor=CENTER)
        self._listBoxErrors.heading("exception", text="Type", anchor=CENTER)
        self._listBoxErrors.heading("message", text="Message", anchor=CENTER)
        self._listBoxErrors.heading("line", text="Line", anchor=CENTER)
        self._listBoxErrors.heading("col", text="Column", anchor=CENTER)
        self._listBoxErrors.heading("file", text="File", anchor=CENTER)
        self._listBoxErrors.bind('<Button-1>', self.__listbox_error_clicked)
        self.__add_scrollbar(self._frameErrors, self._listBoxErrors)
        self._listBoxErrors.pack(side=LEFT, expand=True, fill=BOTH)

        self._frameSyntax = ttk.Frame(self._tabControl)
        self._listBoxSyntax = ttk.Treeview(self._frameSyntax, show='headings')
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

        self._tabControl.add(self._frameErrors, text='Error List')
        self._tabControl.add(self._frameSyntax, text='Syntax Browser')
        self._tabControl.add(self._frameSemantics, text='Semantics Browser')
        self._tabControl.add(self._frameOutput, text='Output')

        self._tabControl.pack(expand=True, fill="both")

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
        selected_item = self._listBoxSyntax.selection()[0]
        item = self._listBoxSyntax.item(selected_item)
        record = item['values']
        self.__set_position_in_editor(record[1], record[2])

    def __listbox_error_clicked(self, event):
        """
        When the user clicks the error item, then the editor cursor will go to the position where the
        error is located.
        :param event:
        :return:
        """
        selected_item = self._listBoxErrors.selection()[0]
        item = self._listBoxErrors.item(selected_item)
        record = item['values']
        self.__set_position_in_editor(record[3], record[4])

    def __set_position_in_editor(self, line, column):
        editor_frame = self._all_editors[self._current_file]['editor']
        self._panedWindowEditor.focus_set()
        self._panedWindowVertical.focus_set()
        self._panedWindowEditor.focus_set()
        self._tabEditor.focus_set()
        editor_frame.focus_set()
        editor_frame.set_pos(line, column)

    def build_fpl_code(self):
        for editor_name in self._all_editors:
            code = self._all_editors[editor_name].get('1.0', END)
            messagebox.showinfo("FPL", "Not implemented yet! (Build of " + editor_name + ")")

    def open_file(self):
        path = askopenfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')])
        self._global_path = path
        with open(path, 'r') as file:
            code = file.read()
            self._current_file = os.path.basename(path)
            editor_frame = FrameWithLineNumbers()
            editor_frame.set_statusbar_handler(self._statusBar)
            editor_frame.set_syntax_list_handler(self._listBoxSyntax)
            editor_frame.set_text(code)
            editor_frame.pack(expand=True, fill="both")

            self._tabEditor.add(editor_frame, text=self._current_file)

            self._all_editors[self._current_file] = dict()
            self._all_editors[self._current_file]['editor'] = editor_frame
            self._all_editors[self._current_file]['dirty'] = False

            self._tabEditor.select(len(self._all_editors) - 1)
            self._tabEditor.bind('<<NotebookTabChanged>>', self.editor_tab_changed)

            self.update_info()

    def update_info(self):
        """
        Updates the info lists regarding the code
        :return:
        """
        code = self._all_editors[self._current_file]['editor'].get_text()
        interpreter = fplinterpreter.FplInterpreter("fplide", code, self.fpl_parser, True)

        self._listBoxErrors.delete(*self._listBoxErrors.get_children())
        no = 0
        for item in interpreter.get_errors():
            item = item.to_tuple() + (self._current_file,)
            self._listBoxErrors.insert("", END, values=item)

        self._listBoxSyntax.delete(*self._listBoxSyntax.get_children())
        editor_frame = self._all_editors[self._current_file]['editor']
        list_indices = list()
        for item in interpreter.get_ast_list():
            item = item + (self._current_file,)
            self._listBoxSyntax.insert("", END, values=item)
            rule_name = item[0]
            current_index = str(item[1]) + "." + str(item[2])
            list_indices.append(current_index)
            grammar_tags = self._theme.get_grammar_tags()
            # set all the tags for syntax highlighting while the parsed rules are added to the _listBoxSyntax
            if rule_name in grammar_tags:
                tag = grammar_tags[rule_name]
                last_index = current_index
                while len(list_indices) > 0 and last_index == current_index:
                    last_index = list_indices.pop()
                if len(list_indices) == 0:
                    last_index = "1.0"
                editor_frame.add_tag(tag, last_index, current_index)

        self._listBoxSemantics.delete(0, 'end')
        no = 0
        for item in interpreter.get_semantics():
            self._listBoxSemantics.insert(no, str(item))
            no += 1

    def editor_tab_changed(self, event):
        selected_tab = event.widget.select()
        self._current_file = event.widget.tab(selected_tab, "text")
        self._statusBar.set_editor_tab(self._current_file)
        self._statusBar.text("")

    def save_file(self):
        if self._global_path == '':
            return self.save_file_as()
        with open(self._global_path, 'w') as file:
            code = self._all_editors[self._current_file]['editor'].get('1.0', END)
            file.write(code)

    def save_file_as(self):
        path = asksaveasfilename(filetypes=[('FPL Files', '*.fpl'), ('Python Files', '*.py')],
                                 initialfile=self._global_path)
        with open(path, 'w') as file:
            code = self._all_editors[self._current_file]['editor'].get('1.0', END)
            file.write(code)

    def fpl_init(self):
        self._statusBar.text('Initiating FPL parser... Please wait!')
        u = Utils()
        self.fpl_parser = u.get_parser("../grammar/fpl_tatsu_format.ebnf")
        self._statusBar.text("FPL parser ready.")


ide = FplIde()
