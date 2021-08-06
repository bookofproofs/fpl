from tkinter import *
from ide.idetheme import DefaultTheme


class TextLineNumbers(Canvas):
    _foreground_color = None
    _theme = None

    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.text_widget = None
        self._theme = DefaultTheme()

    def attach(self, text_widget):
        self.text_widget = text_widget
        self.config(bg=self._theme.get_bg_color())
        self._foreground_color = self._theme.get_fg_color()

    def redraw(self, *args):
        """
        redraw line numbers
        :param args:
        :return:
        """
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            d_line = self.text_widget.dlineinfo(i)
            if d_line is None: break
            y = d_line[1]
            line_num = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=line_num, font=self._theme.line_number_font(), fill='cyan')
            i = self.text_widget.index("%s+1line" % i)
