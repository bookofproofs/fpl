import tkinter as tk
from tkinter import ttk, messagebox
from poc.util.fplutil import Utils


class InfoBoxes:
    def __init__(self, panedWindowBelowEditor, ide):
        self.ide = ide
        self.tree_view_errors = None
        self._tabControl = ttk.Notebook(panedWindowBelowEditor)
        self.__add_error_info_box()

        self._frameDebug = ttk.Frame(self._tabControl)
        self._frameDebug.config()

        self._frameSelfContainment = ttk.Frame(self._tabControl)
        self._frameSelfContainment.config()

        self._tabControl.add(self._gridErrors, text='Error List')
        self._tabControl.add(self._frameDebug, text='Debug')
        self._tabControl.add(self._frameSelfContainment, text='Self-Containment')

        self._tabControl.pack(expand=True, fill=tk.BOTH)

    def __add_error_info_box(self):
        self._gridErrors = ttk.Frame(self._tabControl)
        self._gridErrors.pack(expand=True, fill=tk.BOTH)

        # number of errors label
        self._label_error_num = tk.Label(self._gridErrors, text="Errors (0)",
                                         relief=tk.GROOVE, bg=self.ide.theme.get_bg_color(),
                                         fg=self.ide.theme.get_fg_color())
        self._label_error_num.grid()
        self._label_error_num["compound"] = tk.LEFT
        self._label_error_num["image"] = self.ide.model.images["cancel"]
        self._label_error_num.grid(row=0, column=0, sticky=tk.W + tk.E, pady=2)

        # number of warnings label
        self._label_warning_num = tk.Label(self._gridErrors, text="Warnings (0)",
                                           relief=tk.GROOVE, bg=self.ide.theme.get_bg_color(),
                                           fg=self.ide.theme.get_fg_color())
        self._label_warning_num.grid()
        self._label_warning_num["compound"] = tk.LEFT
        self._label_warning_num["image"] = self.ide.model.images["warning"]
        self._label_warning_num.grid(row=0, column=1, sticky=tk.W + tk.E, pady=2)

        # option menue for filtering all or current file errors
        self._all_file_list = ["All", "Current File"]
        self._all_file_option_menu = tk.OptionMenu(self._gridErrors,
                                                   tk.StringVar(self._gridErrors, value="All"),
                                                   *self._all_file_list)
        self._all_file_option_menu.config(relief=tk.GROOVE,
                                          bg=self.ide.theme.get_bg_color(),
                                          highlightbackground=self.ide.theme.get_bg_color(),
                                          fg=self.ide.theme.get_fg_color())
        self._all_file_option_menu.grid(row=0, column=2, sticky=tk.W + tk.E, pady=2)

        # option menu for filtering the error type
        self._error_type_list = ["(no types)"]
        self._error_type_option_menu = tk.OptionMenu(self._gridErrors,
                                                     tk.StringVar(self._gridErrors, value="(no types)"),
                                                     *self._error_type_list)
        self._error_type_option_menu.config(relief=tk.GROOVE,
                                            bg=self.ide.theme.get_bg_color(),
                                            highlightbackground=self.ide.theme.get_bg_color(),
                                            fg=self.ide.theme.get_fg_color())
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

        self.tree_view_errors = ttk.Treeview(self._frameErrors, selectmode='browse',
                                             column=('Type', 'Message', 'Line', 'Column', 'File'))
        self.tree_view_errors.heading("#0", text="", anchor=tk.W)
        self.tree_view_errors.heading("#1", text="Code", anchor=tk.W)
        self.tree_view_errors.heading("#2", text="Message", anchor=tk.W)
        self.tree_view_errors.heading("#3", text="Line", anchor=tk.E)
        self.tree_view_errors.heading("#4", text="Column", anchor=tk.E)
        self.tree_view_errors.heading("#5", text="File", anchor=tk.CENTER)
        self.tree_view_errors.column('#0', width=40, minwidth=40, stretch=tk.NO, anchor=tk.W)
        self.tree_view_errors.column('Type', width=40, minwidth=40, stretch=tk.YES, anchor=tk.W)
        self.tree_view_errors.column('Message', width=440, minwidth=440, stretch=tk.YES, anchor=tk.W)
        self.tree_view_errors.column('Line', width=30, minwidth=30, stretch=tk.YES, anchor=tk.E)
        self.tree_view_errors.column('Column', width=30, minwidth=30, stretch=tk.YES, anchor=tk.E)
        self.tree_view_errors.column('File', width=70, minwidth=70, stretch=tk.YES, anchor=tk.CENTER)
        self.tree_view_errors.bind('<Double-Button-1>', self.__tree_view_error_clicked)
        self.__add_scrollbar(self._frameErrors, self.tree_view_errors)
        self.tree_view_errors.pack(expand=True, fill=tk.BOTH)

    def update_error_warning_counts(self):
        """
        Update the counts in the IDE depending on the error list
        :return: None
        """
        error_num = 0
        warning_num = 0
        for i in self.tree_view_errors.get_children():
            item = self.tree_view_errors.item(i)
            if type(item['image']) is list:
                if item['image'][0] == 'warning':
                    warning_num += 1
                elif item['image'][0] == 'cancel':
                    error_num += 1
        self._label_error_num.config(text="Errors (" + str(error_num) + ")")
        self._label_warning_num.config(text="Warnings (" + str(warning_num) + ")")

    def refresh_boxes(self, set_of_errors: set):
        # delete all old items in tree_view that belong to the current transformer, i.e. have its name
        self.tree_view_errors.delete(*self.tree_view_errors.get_children())
        # convert the set to list to make it sortable and sort it by the sortkey of the error
        list_of_errors = list(set_of_errors)
        list_of_errors.sort(reverse=False, key=lambda x: x.sort_key())
        # insert new items (if any) in tree_view
        for item in list_of_errors:
            if item.mainType == "E":
                im = self.ide.model.images["cancel"]
            else:
                im = self.ide.model.images["warning"]
            item_tuple = item.to_tuple()
            self.tree_view_errors.insert("", tk.END, text="", image=im, values=item_tuple)
        self.update_error_warning_counts()

    def __tree_view_error_clicked(self, event):
        """
        When the user clicks the error item, then the editor cursor will go to the position where the
        error is located.
        :param event:
        :return:
        """
        record = Utils.identify_clicked_treeview_item(self.tree_view_errors)
        if record is not None:
            if record[4] != "":
                self.ide.set_position_in_editor(record[2], record[3], record[4])
            else:
                messagebox.showerror("This is unfortunate, we are working on this!", record[1])

    def __add_scrollbar(self, frame, widget):
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        scrollbar.config(command=widget.yview)
