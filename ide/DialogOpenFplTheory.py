import tkinter as tk
from ide.Settings import Settings
from tkinter import ttk
from ide.Dialog import Dialog
from tkinter import messagebox
import os


class DialogOpenFplTheory(Dialog):

    def __init__(self, ide):
        super().__init__(ide, "Open FPL Theory", tk.VERTICAL)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (1000 / 2))
        y_coordinate = int((screen_height / 2) - (800 / 2))
        self.geometry("{}x{}+{}+{}".format(500, 200, x_coordinate, y_coordinate))
        self.geometry("{}x{}+{}+{}".format(500, 200, x_coordinate, y_coordinate))

        label_open_theory = tk.Label(self.main_pane, text="Open the main FPL file of some theory:", anchor=tk.NW,
                                     bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self.main_pane.add(label_open_theory)

        self.list_fpl_files = ttk.Treeview(self.main_pane, selectmode='browse', columns=('Namespace', 'File'),
                                           show='headings')
        self.list_fpl_files.heading("Namespace", text="Namespace", anchor=tk.W)
        self.list_fpl_files.heading("File", text="Main File", anchor=tk.W)
        self.list_fpl_files.column('Namespace', width=100, minwidth=100, stretch=tk.YES, anchor=tk.W)
        self.list_fpl_files.column('File', width=100, minwidth=100, stretch=tk.YES, anchor=tk.W)
        self.list_fpl_files.bind("<Double-1>", self._fpl_theory_selected)
        self.list_fpl_files.bind("<Return>", self._fpl_theory_selected)
        scrollbar = tk.Scrollbar(self.list_fpl_files)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        scrollbar.config(command=self.list_fpl_files.yview)
        self.list_fpl_files.pack(expand=True, fill=tk.BOTH)
        self._fill_list_fpl_files()
        self.main_pane.add(self.list_fpl_files)

    def _fill_list_fpl_files(self):
        list_files_namespaces = []
        for child in self.ide.model.library.children:
            list_files_namespaces.append((child.namespace, child.file_name))

        # sort by namespace and file name
        list_files_namespaces.sort(key=lambda x: (x[0], x[1],))
        # leave only the alphabetically first file name per namespace (=main namespace file)
        running_namespace = ""
        for item_tuple in list_files_namespaces:
            if item_tuple[0] != running_namespace:
                running_namespace = item_tuple[0]
                self.list_fpl_files.insert("", tk.END, values=item_tuple)

    def _on_closing(self):
        self.destroy()

    def _fpl_theory_selected(self, event=None):
        item = self.list_fpl_files.selection()[0]
        name_space = self.list_fpl_files.item(item, "value")[0]
        file_name = self.list_fpl_files.item(item, "value")[1]
        path = self.ide.model.config.get(Settings.section_paths, Settings.option_paths_fpl_theories)
        with open(os.path.join(path, file_name), 'r', encoding="UTF-8") as file:
            code = file.read()
        messagebox.showinfo("Open FPL Theory", "The theory {0} was successfully opened.".format(name_space),
                            icon="info")
        book = self.ide.get_editor_notebook()
        book.set_file(file_name)
        book.add_new_editor(code)
        editor_info = book.select_file(file_name)
        editor_info.is_new = False
        self.ide.model.main_file = file_name
        self.ide.model.theory_is_open_flag = True
        self.ide.menus.menu_configure()
        self.ide.verify_all()
        self.destroy()
