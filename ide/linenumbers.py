# solution adapted from https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
# By Bryan Oakley

from tkinter import *
from idetheme import Theme


class TextLineNumbers(Canvas):
    _foreground_color = None
    _theme = None

    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.text_widget = None
        self._theme = Theme()

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


class CustomText(Text):
    _theme = None

    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._theme = Theme()
        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

    def settings(self, background_color, foreground_color):
        self.config(bg=background_color, fg=foreground_color, insertbackground='white')
        self['font'] = self._theme.editor_font()


class FrameWithLineNumbers(Frame):
    _status_bar_handler = None
    _syntax_list_handler = None
    _theme = None
    _tag_indices = {}

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self._theme = Theme()
        self.text = CustomText(self)
        self.text.settings(self._theme.get_bg_color(), self._theme.get_fg_color())
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Double-1>", self._on_click)
        self.text.bind("<Configure>", self._on_change)

    def _on_click(self, event):
        pos = self.get_pos()
        row = int(pos.split('.')[0])
        column = int(pos.split('.')[1])
        for child in self._syntax_list_handler.get_children():
            treeview_row =self._syntax_list_handler.item(child)
            if treeview_row['values'][1] == row:
                if treeview_row['values'][2] <= column:
                    self._syntax_list_handler.selection_set(child)
                    self._syntax_list_handler.focus(child)
                    self._syntax_list_handler.see(child)
                    self._syntax_list_handler.focus_force()

    def _on_change(self, event):
        self.linenumbers.redraw()
        pos = self.get_pos()
        row = pos.split('.')[0]
        column = pos.split('.')[1]
        self._status_bar_handler.text("R:" + row + " C:" + column)

    def set_text(self, code):
        self.text.delete("1.0", END)
        self.text.insert("1.0", code)
        self.remove_all_tags()
        self.configure_all_tags()

    def set_statusbar_handler(self, status_bar):
        self._status_bar_handler = status_bar

    def set_syntax_list_handler(self, syntax_list):
        self._syntax_list_handler = syntax_list

    def get_text(self):
        return self.text.get("1.0", END)

    def get_pos(self):
        return self.text.index(INSERT)

    def set_pos(self, row, column):
        index = str(row) + "." + str(column)
        self.text.see(index)
        self.text.mark_set("insert", index)
        self.focus_set()
        self.text.focus_set()

    def configure_all_tags(self):
        tags = self._theme.get_tag_formatting()
        for tag in tags:
            self.text.tag_config(tag, foreground=tags[tag])
            self._tag_indices[tag] = []

    def remove_all_tags(self):
        for tag in self._tag_indices:
            # remove all tags from text box
            for index in self._tag_indices[tag]:
                start_end = index.split(':')
                self.text.tag_remove(tag, start_end[0], start_end[1])
            # clear the indices of each tag
            self._tag_indices[tag].clear()

    def add_tag(self, tag, start_index, end_index):
        formattings = self._theme.get_tag_formatting()
        if tag in formattings:
            self.text.tag_add(tag, start_index, end_index)
            # remember the indices of the tag so we can remove them again when the user changes the FPL code
            self._tag_indices[tag].append(start_index + ":" + end_index)
