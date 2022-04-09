import tkinter as tk
from idetheme import DefaultTheme


class StatusBar(tk.PanedWindow):

    def __init__(self, master):
        theme = DefaultTheme()
        tk.PanedWindow.__init__(self, master)
        self.config(bg=theme.get_bg_color())
        self._variable = tk.StringVar()
        self.label = tk.Label(self, bd=0, relief=tk.SUNKEN, anchor=tk.W,
                              bg=theme.get_bg_color(), fg=theme.get_fg_color(),
                              textvariable=self._variable, height=1,
                              font=('consolas', 10, 'normal'))
        self.initialize()
        self.label.pack(fill=tk.BOTH)
        self.pack(fill=tk.BOTH, expand=False)

    def initialize(self):
        self.set_text("FPL interpreter ready.")

    def set_text(self, value):
        self._variable.set(value)
