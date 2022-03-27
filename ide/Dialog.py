import tkinter as tk
from ide.idetheme import DefaultTheme

class Dialog(tk.Toplevel):

    def __init__(self, ide, title: str, orient):
        self._theme = DefaultTheme()
        super().__init__(ide.window, bg=self._theme.get_bg_color())
        self.ide = ide
        self.resizable()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (1000 / 2))
        y_coordinate = int((screen_height / 2) - (800 / 2))
        self.geometry("{}x{}+{}+{}".format(750, 400, x_coordinate, y_coordinate))
        self.title(title)
        self.main_pane = tk.PanedWindow(self, orient=orient, bg=self._theme.get_bg_color())
        self.main_pane.pack(fill=tk.BOTH, padx=10, pady=10)
