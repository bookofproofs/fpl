# solution adapted from https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
# By Bryan Oakley
import _tkinter
from tkinter import *
from idetheme import DefaultTheme
from TextLineNumbers import TextLineNumbers
from EditorText import EditorText


class FrameWithLineNumbers(Frame):
    _parent_notebook = None  # parent notebook containing this Frame
    _theme = None
    _tag_indices = {}
    _image_save = None
    to_be_parsed_and_interpreted = False
    title = ""
    calm_down_countdown = 0

    def __init__(self, parent_note_book, title, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self._parent_notebook = parent_note_book
        self._theme = DefaultTheme()
        self.text = EditorText(self, undo=True)
        self.text.settings(self._theme.get_bg_color(), self._theme.get_fg_color())
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)
        self.to_be_parsed_and_interpreted = False
        self.title = title

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
        ide = self._parent_notebook.get_parent()
        for child in ide.get_syntax_list().get_children():
            treeview_row = ide.get_syntax_list().item(child)
            # search for the corresponding row and column in the syntax list
            if treeview_row['values'][1] == row:
                if treeview_row['values'][2] <= column:
                    # if found
                    ide.get_syntax_list().focus(child)
                    ide.get_syntax_list().selection_set(child)
                    ide.get_syntax_list().focus_force()
                    ide.get_syntax_list().see(child)

    def _on_change(self, event):
        self.linenumbers.redraw()
        pos = self.get_pos()
        row = pos.split('.')[0]
        column = pos.split('.')[1]
        ide = self._parent_notebook.get_parent()
        ide.get_status_bar().set_status_text(self.title + " (R:" + row + " C:" + column + ")")
        try:
            if self.text.is_dirty:
                # change the appearance title to "changed"
                self._parent_notebook.tab(self, text=self.title + "*")
            else:
                # change the title to the original one
                self._parent_notebook.tab(self, text=self.title)
        except _tkinter.TclError:
            # ignore the error .!framewithlinenumbers is not managed by .!panedwindow4.!panedwindow.!customnotebook'
            # the very first time when of this event, the _parent_nodebook will not managed 'self' yet
            pass

        # signal the parser thread to work again
        if self.text.has_changed_content:
            self.to_be_parsed_and_interpreted = True
            self.calm_down_countdown = self._parent_notebook.initial_calm_down_countdown

    def set_text(self, code):
        self.text.init_value(code)
        self.reconfigure_all_tags()

    def get_text(self):
        return self.text.get_value()

    def get_pos(self):
        return self.text.index(INSERT)

    def set_pos(self, row, column):
        index = str(row) + "." + str(column)
        self.text.see(index)
        self.text.mark_set("insert", index)
        self.focus_set()
        self.text.focus_set()

    def reconfigure_all_tags(self):
        """
        Initiates the formatting of all tags in the text area and a list per tag with its indices
        that we can remember them to remove them again when the user changes the FPL code
        :return:
        """

        tags = self._theme.get_tag_formatting()
        self.text.tag_delete(list(tags))
        for tag in tags:
            self.text.tag_config(tag, foreground=tags[tag])

    def add_tag(self, tag, start_index, end_index):
        formattings = self._theme.get_tag_formatting()
        if tag in formattings:
            self.text.tag_add(tag, start_index, end_index)
