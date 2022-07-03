import tkinter as tk
import threading
from tkinter import ttk
from ide.idetheme import DefaultTheme
from ide.fplidemenu import FPLIdeMenus
from ide.CustomNotebook import CustomNotebook
from ide.FrameWithLineNumbers import FrameWithLineNumbers
from ide.StatusBar import StatusBar
from ide.IdeModel import IdeModel
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from ide.ObjectBrowser import ObjectBrowser
from ide.InfoBoxes import InfoBoxes


class FplIde:

    def __init__(self):
        self.ide_version = '1.6.12'
        self.theme = DefaultTheme()
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
        self.info_boxes = None
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
        style.configure('TNotebook', tabposition='wn', background=self.theme.get_bg_color())
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
        self._panedWindowEditor.config(bg=self.theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowEditor)

        style = ttk.Style()
        style.theme_create('TNotebook', settings=self.theme.get_notebook_style())
        style.theme_use('TNotebook')
        self._tabEditor = CustomNotebook(self, self._panedWindowEditor)
        self._panedWindowEditor.add(self._tabEditor)

        self._panedWindowBelowEditor = tk.PanedWindow(self._panedWindowVertical, heigh=70,
                                                      bg=self.theme.get_bg_color())
        self._panedWindowBelowEditor.config(bg=self.theme.get_bg_color())
        self._panedWindowVertical.add(self._panedWindowBelowEditor)
        self.info_boxes = InfoBoxes(self._panedWindowBelowEditor, self)

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

    def refresh_info(self, editor_info: FrameWithLineNumbers):
        """
        Refreshes all information based on the current transformer like errors, warnings, and syntax tree
        :param editor_info: Current editor info
        :return: None
        """
        self.info_boxes.refresh_boxes(self.model.fpl_interpreter.get_error_mgr().get_errors())
        self.object_browser.refresh(self.model.fpl_interpreter.get_symbol_table_root())

    def get_status_bar(self):
        return self._statusBar

    def get_editor_notebook(self):
        return self._tabEditor

    def verify_all(self):
        main_fpl_file = self.model.get_main_file()
        # make sure the main file is open
        book = self.get_editor_notebook()
        if main_fpl_file.file_name not in book.get_files():
            book.add_new_editor(main_fpl_file.get_source())
        self.window.update_idletasks()
        x = threading.Thread(target=self.rebuild_thread, args=(main_fpl_file.file_name,))
        x.start()

    def rebuild_thread(self, main_file_name):
        self.window.config(cursor="watch")
        # clear the symbol table and all errors of the interpreter
        self.clear_theory_metadata()
        # refresh the library (because the user might have added new Fpl files)
        self.model.utils.reload_library(self.model.library, self.model.path_to_fpl_root)
        # perform the syntax and semantic analysis for the theory as a whole
        self.model.fpl_interpreter.syntax_analysis(self.model.path_to_fpl_root + '\\' + main_file_name)
        self.model.fpl_interpreter.semantic_analysis()
        if AuxISourceAnalyser.verbose:
            self.model.debug_print()
        # refresh all open files of the theory, including the main file
        for file_name in self._tabEditor.get_files():
            editor_info = self._tabEditor.get_files()[file_name]
            self.highlight_file(editor_info)
        self.refresh_info(editor_info)
        self.window.config(cursor="")

    def clear_theory_metadata(self):
        # empty error list
        error_tree_view = self.info_boxes.tree_view_errors
        error_tree_view.delete(*error_tree_view.get_children())
        self.info_boxes.update_error_warning_counts()
        # empty object tree
        self.object_browser.clear()
        # clear the symbol table and all errors of the interpreter
        self.model.fpl_interpreter.clear()


if __name__ == "__main__":
    ide = FplIde()
