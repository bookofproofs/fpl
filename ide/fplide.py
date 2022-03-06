import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from poc.util.fplutil import Utils
from ide.idetheme import DefaultTheme
from ide.CustomNotebook import CustomNotebook
from ide.FrameWithLineNumbers import FrameWithLineNumbers
from ide.StatusBar import StatusBar
from ide.SettingsDialog import SettingsDialog
from poc.fplinterpreter import FplInterpreter
from poc.fplsourcetransformer import FPLSourceTransformer
from ide.Settings import Settings
import configparser
import os
from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser


class FplIde:

    def __init__(self):
        self._version = '1.3.0'
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
        self.window.state('zoomed')
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
        self.fpl_parser = u.get_parser("../grammar/fpl_tatsu_format.ebnf")
        self.fpl_source_transformer = FPLSourceTransformer(self.fpl_parser)
        path_to_fpl_root = os.path.abspath(self.config.get(Settings.section_paths, Settings.option_paths_fpl_theories))
        self.fpl_interpreter = FplInterpreter(self.fpl_parser, path_to_fpl_root)
        self._statusBar.set_status_text("FPL interpreter ready.")
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
        self._object_browser_tree = ttk.Treeview(self._panedMain, selectmode='browse')
        self._object_browser_tree["columns"] = ("Name", "Status", "File")
        self._object_browser_tree.column("#0", minwidth=25, anchor=tk.W)
        self._object_browser_tree.column("Name", width=270, minwidth=270, stretch=tk.YES, anchor=tk.W)
        self._object_browser_tree.column("Status", width=25, minwidth=25, stretch=tk.YES, anchor=tk.W)
        self._object_browser_tree.column("File", width=170, minwidth=170, stretch=tk.YES, anchor=tk.W)
        self._object_browser_tree.heading("#0", text="Theory Structure", anchor=tk.W)
        self._object_browser_tree.heading("Name", text="Name", anchor=tk.W)
        self._object_browser_tree.heading("Status", text="Status", anchor=tk.W)
        self._object_browser_tree.heading("File", text="File", anchor=tk.W)
        n = self._object_browser_tree.insert('', index='end', iid='n', text='TestNamespace', values=("", "ok", ""))
        ir = self._object_browser_tree.insert(n, index='end', iid='i', text='Inference Rules', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=ir, index='end', iid='i.1', text='Inference',
                                         values=("ExampleInferenceRule()", "ok", "Example.fpl"))
        a = self._object_browser_tree.insert(parent=n, index='end', iid='a', text='Axioms', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=a, index='end', iid='a.1', text='Axiom',
                                         values=("ExampleAxiom()", "ok", "Example.fpl"))
        c = self._object_browser_tree.insert(parent=n, index='end', iid='c', text='Conjectures', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=c, index='end', iid='c.1', text='Conjecture',
                                         values=("ExampleConjecture()", "ok", "Example.fpl"))
        d = self._object_browser_tree.insert(parent=n, index='end', iid='d', text='Definitions', values=("", "ok", ""))
        ob = self._object_browser_tree.insert(parent=d, index='end', iid='d.o', text='Mathematical Objects',
                                              values=("", "ok", ""))
        self._object_browser_tree.insert(parent=ob, index='end', iid='d.o.r', text='Object',
                                         values=("RealNumber()", "ok", "Example.fpl"))
        fu = self._object_browser_tree.insert(parent=d, index='end', iid='d.f', text='Functions', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=fu, index='end', iid='d.f.i', text='Function',
                                         values=("RealIntegral(RealNumber,RealNumber)", "ok", "Example.fpl"))
        pr = self._object_browser_tree.insert(parent=d, index='end', iid='d.p', text='Predicates',
                                              values=("", "ok", ""))
        self._object_browser_tree.insert(parent=pr, index='end', iid='d.p.g', text='Predicate',
                                         values=("IsGreater(RealNumber,RealNumber)", "ok", "Example.fpl"))
        t = self._object_browser_tree.insert(parent=n, index='end', iid='t', text='Theorems', values=("", "ok", ""))
        t1 = self._object_browser_tree.insert(parent=t, index='end', iid='t.1', text="Theorem",
                                              values=("ExampleTheorem()", "ok", "Example.fpl"))
        self._object_browser_tree.insert(parent=t1, index='end', iid='t.1.1', text="Proof",
                                         values=("Proof#1", "ok", "Example.fpl"))
        self._object_browser_tree.insert(parent=t1, index='end', iid='t.1.2', text="Corollary",
                                         values=("Corollary#1()", "ok", "Example.fpl"))
        p = self._object_browser_tree.insert(parent=n, index='end', iid='p', text="Propositions", values=("", "ok", ""))
        self._object_browser_tree.insert(p, index='end', iid='p.1', text="Proposition",
                                         values=("ExampleProposition()", "ok", "Example.fpl"))
        l = self._object_browser_tree.insert(parent=n, index='end', iid='l', text="Lemmas", values=("", "ok", ""))
        self._object_browser_tree.insert(l, index='end', iid='l.1', text="Lemmas",
                                         values=("ExampleLemma()", "ok", "Example.fpl"))
        self._object_browser_tree.insert(parent=n, index='end', iid='u', text="Unassigned", values=("", "ok", ""))
        n1 = self._object_browser_tree.insert('', index='end', iid='n1', text='SecondTestNamespace',
                                              values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='i1', text='Inference Rules',
                                         values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='a1', text='Axioms', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='c1', text='Conjectures', values=("", "ok", ""))
        d1 = self._object_browser_tree.insert(parent=n1, index='end', iid='d1', text='Definitions',
                                              values=("", "ok", ""))
        self._object_browser_tree.insert(parent=d1, index='end', iid='d.o1', text='Mathematical Objects',
                                         values=("", "ok", ""))
        self._object_browser_tree.insert(parent=d1, index='end', iid='d.f1', text='Functions', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=d1, index='end', iid='d.p1', text='Predicates', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='t1', text='Theorems', values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='p1', text="Propositions", values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='l1', text="Lemmas", values=("", "ok", ""))
        self._object_browser_tree.insert(parent=n1, index='end', iid='u1', text="Unassigned", values=("", "ok", ""))
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

        self._frameDebug = ttk.Frame(self._tabControl)
        self._frameDebug.config()

        self._tabControl.add(self._gridErrors, text='Error List')
        self._tabControl.add(self._frameDebug, text='Debug')

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

        self._listBoxErrors = ttk.Treeview(self._frameErrors, selectmode='browse',
                                           column=('Type', 'Message', 'Line', 'Column', 'File'))
        # self._listBoxErrors["columns"] = ("#0", "#1", "#2", "#3", "#4", "#5")
        self._listBoxErrors.heading("#0", text="", anchor=tk.W)
        self._listBoxErrors.heading("#1", text="Code", anchor=tk.W)
        self._listBoxErrors.heading("#2", text="Message", anchor=tk.W)
        self._listBoxErrors.heading("#3", text="Line", anchor=tk.E)
        self._listBoxErrors.heading("#4", text="Column", anchor=tk.E)
        self._listBoxErrors.heading("#5", text="File", anchor=tk.CENTER)
        self._listBoxErrors.column('#0', width=40, minwidth=40, stretch=tk.NO, anchor=tk.W)
        self._listBoxErrors.column('Type', width=40, minwidth=40, stretch=tk.YES, anchor=tk.W)
        self._listBoxErrors.column('Message', width=240, minwidth=240, stretch=tk.YES, anchor=tk.W)
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
        editor_frame.set_pos(line, column - 1)

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

    def refresh_info(self, interpreter: FplInterpreter, editor_info: FrameWithLineNumbers):
        """
        Refreshes all information based on the current transformer like errors, warnings, and syntax tree
        :param interpreter: Current transformer
        :param editor_info: Current editor info
        :return: None
        """
        self._refresh_items_tree_view(editor_info, interpreter.get_errors(), self.get_error_list(), column=4)
        if AuxISourceAnalyser.verbose:
            print(interpreter.symbol_table_to_str())
        self._refresh_object_tree(interpreter.get_symbol_table_root())

    def _refresh_items_tree_view(self, editor_info: FrameWithLineNumbers, tuple_list: list, tree_view: ttk.Treeview,
                                 column: int):
        # delete all old items in tree_view that belong to the current transformer, i.e. have its name
        self.remove_items_from_tree_view(tree_view, column, editor_info.title)
        # insert new items (if any) in tree_view
        for item in tuple_list:
            if item.mainType == "E":
                im = self.images["cancel"]
            else:
                im = self.images["warning"]
            item_tuple = item.to_tuple() + (editor_info.title,)
            tree_view.insert("", tk.END, text="", image=im, values=item_tuple)
            editor_info.add_error_tag(item.get_tkinter_pos())
        self.update_error_warning_counts()

    def _refresh_object_tree(self, root: AnyNode):
        """
        Updates the object tree according to the current syntax tree.
        :param root: root of the syntax tree
        :param tree_view: object tree widget in the IDE
        :return: None
        """
        # dictionary prevents creating multiple theory nodes for the same namespace split across different FPL files
        tree_view_theories = dict()
        # remove all items from previous tree_view
        self._object_browser_tree.delete(*self._object_browser_tree.get_children())
        theories = AuxSymbolTable.get_theories(root)
        for theory_node in theories:
            if theory_node.namespace not in tree_view_theories:
                tree_view_theories[theory_node.namespace] = \
                    self._object_browser_tree.insert('', index='end',
                                                     iid=theory_node.namespace,
                                                     text=theory_node.namespace,
                                                     values=("", "ok", theory_node.file_name))
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_ir_root, "_i", "Inference Rules",
                                                  "Inference")
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_axiom_root, "_a", "Axioms",
                                                  "Axiom")
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_conj_root, "_c", "Conjectures",
                                                  "Conjecture")
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_def_root, "_d", "Definitions",
                                                  "Definition")
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_thm_root, "_t", "Theorems",
                                                  "Theorem")
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_prop_root, "_p", "Propositions",
                                                  "Proposition")
            self.__propagate_object_tree_children(theory_node, tree_view_theories[theory_node.namespace],
                                                  AuxSymbolTable.block_lem_root, "_l", "Lemmas",
                                                  "Lemma")

    def __propagate_object_tree_children(self, theory_node: AnyNode, treeview_theory_node, outline: str, postfix: str,
                                         node_title: str,
                                         node_label: str):
        syntax_tree_node = AuxSymbolTable.get_child_by_outline(theory_node, outline)
        if len(syntax_tree_node.children):
            tree_view_node = self._object_browser_tree.insert(treeview_theory_node, index='end',
                                                              iid=theory_node.namespace + postfix,
                                                              text=node_title, values=("", "ok", theory_node.file_name))
            need_def_objects = True
            need_def_objects_constructors = True
            need_def_objects_properties = True
            need_def_predicates = True
            need_def_predicate_properties = True
            need_def_functions = True
            need_def_function_properties = True
            ob = None
            pr = None
            fu = None
            for child in syntax_tree_node.children:
                if outline == AuxSymbolTable.block_def_root:
                    if child.def_type == AuxSymbolTable.classDeclaration:
                        if need_def_objects:
                            ob = self._object_browser_tree.insert(parent=tree_view_node, index='end',
                                                                  iid=theory_node.namespace + postfix + '_o',
                                                                  text='Objects',
                                                                  values=("", "ok", theory_node.file_name))
                            need_def_objects = False
                        obj = self._object_browser_tree.insert(parent=ob, index='end',
                                                               iid=theory_node.namespace + postfix + '_o' + child.id,
                                                               text=child.id,
                                                               values=("", "ok", theory_node.file_name))
                        self.__propagate_object_tree_children_sub(theory_node, child, obj,
                                                                  theory_node.namespace + postfix + '_o' + child.id + '_c',
                                                                  AuxSymbolTable.classConstructors,
                                                                  need_def_objects_constructors)
                        self.__propagate_object_tree_children_sub(theory_node, child, obj,
                                                                  theory_node.namespace + postfix + '_o' + child.id + '_p',
                                                                  AuxSymbolTable.properties,
                                                                  need_def_objects_properties)
                    elif child.def_type == AuxSymbolTable.predicateDeclaration:
                        if need_def_predicates:
                            pr = self._object_browser_tree.insert(parent=tree_view_node, index='end',
                                                                  iid=theory_node.namespace + postfix + '_p',
                                                                  text='Predicates',
                                                                  values=("", "ok", theory_node.file_name))
                            need_def_predicates = False
                        prop = self._object_browser_tree.insert(parent=pr, index='end',
                                                                iid=theory_node.namespace + postfix + '_p' + child.id,
                                                                text=child.id,
                                                                values=("", "ok", theory_node.file_name))
                        self.__propagate_object_tree_children_sub(theory_node, child, prop,
                                                                  theory_node.namespace + postfix + '_p' + child.id + '_p',
                                                                  AuxSymbolTable.properties,
                                                                  need_def_predicate_properties)
                    elif child.def_type == AuxSymbolTable.functionalTerm:
                        if need_def_functions:
                            fu = self._object_browser_tree.insert(parent=tree_view_node, index='end',
                                                                  iid=theory_node.namespace + postfix + '_f',
                                                                  text='Functions',
                                                                  values=("", "ok", theory_node.file_name))
                            need_def_functions = False
                        func = self._object_browser_tree.insert(parent=fu, index='end',
                                                                iid=theory_node.namespace + postfix + '_f' + child.id,
                                                                text=child.id,
                                                                values=("", "ok", theory_node.file_name))
                        self.__propagate_object_tree_children_sub(theory_node, child, func,
                                                                  theory_node.namespace + postfix + '_f' + child.id + '_p',
                                                                  AuxSymbolTable.properties,
                                                                  need_def_function_properties)
                    else:
                        raise NotImplementedError(outline)
                else:
                    self._object_browser_tree.insert(parent=tree_view_node, index='end',
                                                     iid=theory_node.namespace + postfix + child.id, text=node_label,
                                                     values=(child.id, "ok", theory_node.file_name))

    def __propagate_object_tree_children_sub(self, theory_node: AnyNode, node: AnyNode, tree_view_node, postfix: str,
                                             outline: str, need_for_outline_node: bool):
        if outline == AuxSymbolTable.classConstructors:
            sub_node = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.classConstructors)
            sub_node_title = 'Constructors'
        else:
            sub_node = AuxSymbolTable.get_child_by_outline(node, AuxSymbolTable.properties)
            sub_node_title = 'Properties'

        if len(sub_node.children) > 0:
            if need_for_outline_node:
                sub_node_tree_view = self._object_browser_tree.insert(parent=tree_view_node, index='end',
                                                                      iid=postfix + node.id,
                                                                      text=sub_node_title,
                                                                      values=("", "ok", theory_node.file_name))
            for sub_sub_node in sub_node.children:
                self._object_browser_tree.insert(parent=sub_node_tree_view, index='end',
                                                 iid=postfix + node.id + sub_sub_node.id,
                                                 text=sub_sub_node.id,
                                                 values=("", "ok", theory_node.file_name))

    def build_fpl_code(self):
        messagebox.showinfo("FPL", "Not implemented yet! (Build)")

    def settings(self):
        SettingsDialog(self)

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

    def get_editor_notebook(self):
        return self._tabEditor

    def get_warning_number(self):
        return self._label_warning_num

    def get_error_number(self):
        return self._label_error_num


if __name__ == "__main__":
    ide = FplIde()
