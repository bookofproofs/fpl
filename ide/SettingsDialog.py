from tkinter import *
from tkinter import ttk
from ide.idetheme import DefaultTheme


class SettingsDialog(Toplevel):
    app = None
    _rootwindow = None
    _theme = None
    _mainframe = None
    _config_editor_pane = None
    _notebook = None
    _config_browser_pane = None
    _config_browser_tree = None

    def __init__(self, app):
        super().__init__(app.window)
        self.app = app
        self._theme = DefaultTheme()
        self.resizable()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (750 / 2))
        y_cordinate = int((screen_height / 2) - (400 / 2))
        self.geometry("{}x{}+{}+{}".format(750, 400, x_cordinate, y_cordinate))
        self.title("FPL IDE Settings")

        main_pane = ttk.PanedWindow(self, orient=HORIZONTAL)
        main_pane.pack(fill=BOTH, expand=1)

        left_pane = PanedWindow(main_pane, width=300)
        right_pane = PanedWindow(main_pane, bg=self._theme.get_bg_color())

        self._config_browser_tree = ttk.Treeview(left_pane)
        for section in self.app.config.sections():
            id = self._config_browser_tree.insert('', 'end', text=section)
            for option in self.app.config.options(section):
                self._config_browser_tree.insert(id, 'end', text=option)

        left_pane.add(self._config_browser_tree)

        right = Label(right_pane, text="Editing Settings not implemented yet", bg=self._theme.get_bg_color(),
                      fg=self._theme.get_fg_color())
        right_pane.add(right)

        main_pane.add(left_pane)
        main_pane.add(right_pane)

    def __add_scrollbar(self, frame, widget):
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        scrollbar.config(command=widget.yview)
