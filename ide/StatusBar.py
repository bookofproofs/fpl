import tkinter as tk
from idetheme import DefaultTheme


class StatusBar(tk.PanedWindow):
    _labelText = ""
    _current_editor_tab = ""

    def __init__(self, master):
        theme = DefaultTheme()
        tk.PanedWindow.__init__(self, master)
        self.config(bg=theme.get_bg_color())
        self.variable = tk.StringVar()
        self.label = tk.Label(self, bd=0, relief=tk.SUNKEN, anchor=tk.W,
                              bg=theme.get_bg_color(), fg=theme.get_fg_color(),
                              textvariable=self.variable,
                              font=('consolas', 10, 'normal'))
        self.variable.set('Status Bar')
        self.label.pack(fill=tk.X)
        self.pack()

    def set_status_text(self, value):
        self.variable.set(self._current_editor_tab + " " + value)
