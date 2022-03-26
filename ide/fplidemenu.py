from tkinter import messagebox
from ide.SettingsDialog import SettingsDialog
import tkinter as tk


class FPLIdeMenus:

    def __init__(self, ide):
        self.ide = ide
        self._menuBar = tk.Menu(ide.window)

        fpl_theory_bar = tk.Menu(self._menuBar, tearoff=0)
        fpl_theory_bar.add_command(label='New', underline=0, command=self.not_implemented)
        fpl_theory_bar.add_command(label='Open', underline=0, command=self.not_implemented)
        fpl_theory_bar.add_command(label='Close', underline=0, command=self.not_implemented, state=tk.DISABLED)
        fpl_theory_bar.add_separator()
        fpl_theory_bar.add_command(label='Add FPL file', underline=0, command=self.not_implemented, state=tk.DISABLED)
        fpl_theory_bar.add_command(label='Remove FPL file', underline=0, command=self.not_implemented,
                                   state=tk.DISABLED)
        fpl_theory_bar.add_separator()
        fpl_theory_bar.add_command(label='Exit', underline=1, command=self.exit)
        self._menuBar.add_cascade(label='FPL Theory', underline=0, menu=fpl_theory_bar)

        file_bar = tk.Menu(self._menuBar, tearoff=0)
        file_bar.add_command(label='New', underline=0, command=self.new_file)
        file_bar.add_command(label='Open', underline=0, command=self.open_file)
        file_bar.add_command(label='Save', underline=0, command=self.save_file)
        file_bar.add_command(label='Save As', underline=6, command=self.save_file_as)
        self._menuBar.add_cascade(label='File', underline=0, menu=file_bar)

        build_bar = tk.Menu(self._menuBar, tearoff=0)
        build_bar.add_command(label='Current FPL File', command=self.not_implemented, state=tk.DISABLED)
        build_bar.add_command(label='Whole Theory', command=self.not_implemented, state=tk.DISABLED)
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

    def exit(self, event=None):
        book = self.ide.get_editor_notebook().get_files()
        at_least_one_open_file_changed = False
        for file in book:
            if book[file].text.is_dirty:
                at_least_one_open_file_changed = True
                self.ide.get_editor_notebook().select_file(file)
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
                self.ide.window.destroy()
        else:
            self.ide.window.destroy()

    def settings(self):
        SettingsDialog(self)
