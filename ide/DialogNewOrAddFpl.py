from poc.classes.AuxSTFplFile import AuxSTFplFile
import tkinter as tk
from poc.classes.AuxSymbolTable import AuxSymbolTable
from tkinter import messagebox
from ide.Settings import Settings
from ide.Dialog import Dialog
import re
import os


class DialogNewOrAddFpl(Dialog):

    def __init__(self, ide, new_or_add: str):
        if new_or_add == "new":
            super().__init__(ide, "New FPL Theory", tk.VERTICAL)
        else:
            super().__init__(ide, "Add FPL File to Theory", tk.VERTICAL)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (1000 / 2))
        y_coordinate = int((screen_height / 2) - (800 / 2))
        self.geometry("{}x{}+{}+{}".format(500, 200, x_coordinate, y_coordinate))
        self.geometry("{}x{}+{}+{}".format(500, 200, x_coordinate, y_coordinate))

        # _variable label + entry
        self.file_name = tk.StringVar()
        self._actual_file_name = tk.StringVar()
        label_file_name = tk.Label(self.main_pane, text="File name (*.fpl)",
                                   anchor=tk.NW,
                                   bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self.main_pane.add(label_file_name)

        file_name_one_line_frame = tk.Frame(self.main_pane, height=30, bg=self._theme.get_bg_color())
        entry_filename = tk.Entry(file_name_one_line_frame, textvariable=self.file_name, bg=self._theme.get_bg_color(),
                                  fg=self._theme.get_fg_color())
        entry_filename.grid(row=0, column=0, sticky=tk.EW)
        file_name_one_line_frame.columnconfigure(0, weight=80)
        self.main_pane.add(file_name_one_line_frame)

        # _variable label + entry
        self.name_space = tk.StringVar()
        label_name_space = tk.Label(self.main_pane, text="Namespace ( Syntax: PascalCaseId (.PascalCaseId)* ) ",
                                    anchor=tk.NW,
                                    bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self.main_pane.add(label_name_space)

        name_space_one_line_frame = tk.Frame(self.main_pane, height=30, bg=self._theme.get_bg_color())
        entry_namespace = tk.Entry(name_space_one_line_frame, textvariable=self.name_space,
                                   bg=self._theme.get_bg_color(),
                                   fg=self._theme.get_fg_color())
        entry_namespace.grid(row=0, column=0, sticky=tk.EW)
        name_space_one_line_frame.columnconfigure(0, weight=80)
        self.main_pane.add(name_space_one_line_frame)

        self.warning_text = tk.Text(self.main_pane, height=3, width=50, fg=self._theme.get_warning_color(),
                                    bg=self._theme.get_bg_color(), wrap=tk.WORD, relief=tk.FLAT, state=tk.DISABLED)
        self.main_pane.add(self.warning_text)
        if new_or_add == "new":
            button = tk.Button(self.main_pane, text="Create", width=10, fg=self._theme.get_bg_color(), anchor=tk.CENTER)
            button.bind("<Button-1>", self.create)
            self.bind("<Return>", self.create)
        else:
            button = tk.Button(self.main_pane, text="Add", width=10, fg=self._theme.get_bg_color(), anchor=tk.CENTER)
            button.bind("<Button-1>", self.add_fpl_file)
            self.bind("<Return>", self.add_fpl_file)
        self.main_pane.add(button)
        file_name_one_line_frame.focus_set()

    def _on_closing(self):
        self.destroy()

    def add_fpl_file(self, event):
        file_name = self.file_name.get()
        name_space = self.name_space.get()
        if self._sanitize_file_name(file_name) and self._sanitize_name_space_syntax(name_space):
            initial_code = name_space + "\n{\n\ttheory{}\n}\n"
            # write initial code of the new empty FPL file
            self.ide.model.utils.save_file_content(initial_code)
            messagebox.showinfo("Adding FPL File",
                                "A new fpl file {0} was successfully added to the namespace {1}.".format(file_name,
                                                                                                         name_space),
                                icon="info")
            fpl_file = AuxSTFplFile()
            fpl_file.file_name = os.path.basename(self._actual_file_name.get())
            fpl_file.set_file_content(initial_code.strip())
            fpl_file.namespace = name_space
            fpl_file.parent = self.ide.model.library
            book = self.ide.get_editor_notebook()
            book.set_file(os.path.basename(self._actual_file_name.get()))
            book.add_new_editor(initial_code)
            editor_info = book.select_file(file_name)
            editor_info.is_new = True
            self.ide.model.theory_is_open_flag = True
            self.ide.menus.menu_configure()
            self.destroy()

        else:
            pass

    def create(self, event):
        file_name = self.file_name.get()
        name_space = self.name_space.get()
        if self._sanitize_file_name(file_name) and self._sanitize_name_space(name_space):
            initial_code = name_space + "\n{\n\ttheory{}\n}\n"
            # write initial code of the new empty FPL file
            self.ide.model.utils.save_file_content(initial_code)
            messagebox.showinfo("New FPL Theory", "A new theory {0} was successfully created.".format(name_space),
                                icon="info")

            fpl_file = AuxSTFplFile()
            fpl_file.file_name = os.path.basename(self._actual_file_name.get())
            fpl_file.set_file_content(initial_code.strip())
            fpl_file.namespace = name_space
            fpl_file.parent = self.ide.model.library
            self.ide.model.main_file = file_name
            book = self.ide.get_editor_notebook()
            book.set_file(os.path.basename(self._actual_file_name.get()))
            book.add_new_editor(initial_code)
            editor_info = book.select_file(file_name)
            editor_info.is_new = True
            self.ide.model.theory_is_open_flag = True
            self.ide.menus.menu_configure()
            self.destroy()
        else:
            pass

    def _sanitize_file_name(self, file_name: str):
        self.warning_text.config(state=tk.NORMAL)
        self.warning_text.delete("1.0", tk.END)
        no_error = True
        path = self.ide.model.config.get(Settings.section_paths, Settings.option_paths_fpl_theories)
        file_name = file_name.strip()
        if file_name == "":
            self.warning_text.insert(tk.END, "Please provide a name for the FPL file.")
            no_error = False
        if not file_name.endswith(".fpl"):
            file_name = file_name + ".fpl"
        full_path = os.path.join(path, file_name)
        if os.path.exists(full_path):
            self.warning_text.insert(tk.END, "There is already a file named '{0}' in {1}.".format(file_name, path))
            no_error = False
        self._actual_file_name.set(full_path)
        self.warning_text.tag_configure("center", justify='center')
        self.warning_text.tag_add("center", "1.0", tk.END)
        self.warning_text.config(state=tk.DISABLED)
        return no_error

    def _sanitize_name_space_syntax(self, name_space: str):
        self.warning_text.config(state=tk.NORMAL)
        self.warning_text.delete("1.0", tk.END)
        no_error = True
        pattern = re.compile("^[A-Z][a-z0-9A-Z_]*(\.[A-Z][a-z0-9A-Z_]*)*$")
        if pattern.match(name_space):
            # the name space has a correct syntax
            pass
        else:
            self.warning_text.insert(tk.END,
                                     "The namespace '{0}' does not match the allowed syntax.".format(name_space))
            no_error = False
        self.warning_text.tag_configure("center", justify='center')
        self.warning_text.tag_add("center", "1.0", tk.END)
        self.warning_text.config(state=tk.DISABLED)
        return no_error

    def _sanitize_name_space(self, name_space: str):
        if self._sanitize_name_space_syntax(name_space):
            self.warning_text.config(state=tk.NORMAL)
            self.warning_text.delete("1.0", tk.END)
            no_error = True
            name_space_in_library = AuxSymbolTable.get_library_by_namespace(self.ide.model.library, name_space, "")
            if len(name_space_in_library) > 0:
                file_list = []
                for t in name_space_in_library:
                    file_list.append(t.file_name)
                self.warning_text.insert(tk.END, "The namespace '{0}'".format(name_space) +
                                         " already exists. Please open any one of: {0}".format(", ".join(file_list)))
                no_error = False
            self.warning_text.tag_configure("center", justify='center')
            self.warning_text.tag_add("center", "1.0", tk.END)
            self.warning_text.config(state=tk.DISABLED)
            return no_error
