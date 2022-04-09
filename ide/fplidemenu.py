from tkinter import messagebox
from ide.DialogSettings import DialogSettings
from ide.DialogNewOrAddFpl import DialogNewOrAddFpl
from ide.DialogOpenFplTheory import DialogOpenFplTheory
import tkinter as tk


class FPLIdeMenus:

    def __init__(self, ide):
        self.ide = ide
        self._menuBar = tk.Menu(ide.window)

        self.fpl_theory_menu = tk.Menu(self._menuBar, tearoff=0)
        self.fpl_theory_menu.add_command(label='New', underline=0, command=self.new_fpl_theory)
        self.fpl_theory_menu.add_command(label='Open', underline=0, command=self.open_fpl_theory)
        self.fpl_theory_menu.add_command(label='Close', underline=0, command=self.close_fpl_theory)
        self.fpl_theory_menu.add_separator()
        self.fpl_theory_menu.add_command(label='Add FPL file', underline=0, command=self.add_fpl_file)
        self.fpl_theory_menu.add_command(label='Remove FPL file', underline=0, command=self.not_implemented)
        self.fpl_theory_menu.add_separator()
        self.fpl_theory_menu.add_command(label='Exit', underline=1, command=self.exit)
        self._menuBar.add_cascade(label='FPL Theory', underline=0, menu=self.fpl_theory_menu)

        file_bar = tk.Menu(self._menuBar, tearoff=0)
        file_bar.add_command(label='New', underline=0, command=self.new_file)
        file_bar.add_command(label='Open', underline=0, command=self.open_file)
        file_bar.add_command(label='Save', underline=0, command=self.save_file)
        file_bar.add_command(label='Save As', underline=6, command=self.save_file_as)
        self._menuBar.add_cascade(label='File', underline=0, menu=file_bar)

        build_bar = tk.Menu(self._menuBar, tearoff=0)
        build_bar.add_command(label='Current FPL File', command=self.not_implemented)
        build_bar.add_command(label='Whole Theory', command=self.not_implemented)
        self._menuBar.add_cascade(label='Build', underline=0, menu=build_bar)

        options_bar = tk.Menu(self._menuBar, tearoff=0)
        options_bar.add_command(label='Settings', command=self.settings)
        self._menuBar.add_cascade(label='Options', underline=0, menu=options_bar)

        help_bar = tk.Menu(self._menuBar, tearoff=0)
        help_bar.add_command(label='Open Guide', command=self.not_implemented)
        help_bar.add_command(label='About', command=self.about)
        self._menuBar.add_cascade(label='Help', underline=0, menu=help_bar)

        self.ide.window.bind_all('<Control-Key-n>', self.new_file)
        self.ide.window.bind_all('<Control-Key-o>', self.open_file)
        self.ide.window.bind_all('<Control-Key-S>', self.save_file)
        self.ide.window.bind_all('<Control-Key-s>', self.save_file_as)
        self.ide.window.bind_all('<Control-Key-x>', self.exit)
        self.ide.window.config(menu=self._menuBar)
        self.ide.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.menu_configure()

    @staticmethod
    def not_implemented():
        messagebox.showinfo("FPL", "This menu item is not implemented yet!")

    def about(self):
        messagebox.showinfo("FPL",
                            "IDE for the Formal Proving Language (FPL), Version " + self._version +
                            "\n\n" + u"\u00A9" + " All Rights Reserved")

    def new_file(self, event=None):
        self.ide.get_editor_notebook().new_file(event)

    def open_file(self, event=None):
        self.ide.get_editor_notebook().open_file(event)

    def close_file(self, event=None):
        raise NotImplementedError("close_file")

    def save_file(self, event=None):
        self.ide.get_editor_notebook().save_file(event)

    def save_file_as(self, event=None):
        self.ide.get_editor_notebook().save_file_as(event)

    def menu_configure(self):
        if self.ide.model.theory_is_open_flag:
            self.fpl_theory_menu.entryconfig("New", state=tk.DISABLED)
            self.fpl_theory_menu.entryconfig("Open", state=tk.DISABLED)
            self.fpl_theory_menu.entryconfig("Close", state=tk.NORMAL)
            self.fpl_theory_menu.entryconfig("Add FPL file", state=tk.NORMAL)
            self.fpl_theory_menu.entryconfig("Remove FPL file", state=tk.NORMAL)
        else:
            self.fpl_theory_menu.entryconfig("New", state=tk.NORMAL)
            self.fpl_theory_menu.entryconfig("Open", state=tk.NORMAL)
            self.fpl_theory_menu.entryconfig("Close", state=tk.DISABLED)
            self.fpl_theory_menu.entryconfig("Add FPL file", state=tk.DISABLED)
            self.fpl_theory_menu.entryconfig("Remove FPL file", state=tk.DISABLED)

    def exit(self, event=None):
        closeable = self._ask_to_save_any_open_files()
        if closeable:
            # if no message boxes were answered yet, ask if the user really want's to quit the application
            msg = messagebox.askyesnocancel("Quit FPLIDE",
                                            "Do you want quit the application?",
                                            icon='warning')
            if not msg or msg is None:
                # do nothing
                return
            else:
                self.ide.window.destroy()
        else:
            self.ide.window.destroy()

    def settings(self):
        DialogSettings(self.ide)

    def new_fpl_theory(self):
        DialogNewOrAddFpl(self.ide, "new")

    def open_fpl_theory(self):
        DialogOpenFplTheory(self.ide)

    def add_fpl_file(self):
        DialogNewOrAddFpl(self.ide, "add")

    def _ask_to_save_any_open_files(self):
        book = self.ide.get_editor_notebook().get_files()
        for file in book:
            if book[file].text.is_dirty:
                self.ide.get_editor_notebook().select_file(file)
                msg = messagebox.askyesnocancel("Quit FPLIDE",
                                                "Do you want to save changes of the file " + file + " before quitting?",
                                                icon='warning')
                if msg:
                    # the user wants to save the file!
                    self.save_file(None)
                elif msg is None:
                    # the user cancelled the exist
                    return False
        # the user decided if to save each file and saved it.
        return True

    def close_fpl_theory(self):
        closeable = self._ask_to_save_any_open_files()
        if closeable:
            # close all open tabs
            book = self.ide.get_editor_notebook()
            for tab_name in book.tabs():
                book.forget(tab_name)
            # empty error list
            error_tree_view = self.ide.get_error_list()
            error_tree_view.delete(*error_tree_view.get_children())
            self.ide.update_error_warning_counts()
            # empty object tree
            object_tree = self.ide.get_object_browser_tree()
            object_tree.delete(*object_tree.get_children())
            # flag that no theory is open
            self.ide.model.theory_is_open_flag = False
            self.ide.menus.menu_configure()
            # set the status bar
            status_bar = self.ide.get_status_bar()
            status_bar.set_text("Ready.")

