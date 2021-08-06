# solution adapted from https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
# By Bryan Oakley
import _tkinter
from tkinter import *
from ide.idetheme import DefaultTheme
from ide.TextLineNumbers import TextLineNumbers
from ide.EditorText import EditorText
import tkinter.font as tkfont
from poc import fplinterpreter


class FrameWithLineNumbers(Frame):
    _parent_notebook = None  # parent notebook containing this Frame
    _theme = None
    _tag_indices = {}
    _image_save = None
    title = ""
    is_new = True  # is True if this is a new file, or False, if it was loaded from disk
    _last_pos = "1.0"
    _indent = 0
    _number_spaces_per_tab = 3

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
        self.configure_tab_width(self._number_spaces_per_tab)
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.bind_all('<Alt-Control-j>', self.parse_interpret_highlight)
        self.bind_all('<Alt-Control-g>', self.parse_interpret_highlight_update_all)
        self.bind_all('<Alt-Control-l>', self.reformat_code)
        self.bind_all('<Return>', self._enter_return)
        self.text.bind("<Double-1>", self._on_click)
        self.text.bind("<Configure>", self._on_change)

    def configure_tab_width(self, number_spaces):
        font = tkfont.Font(font=self.text['font'])
        self.text.config(tabs=font.measure(' ' * number_spaces))

    def _enter_return(self, event):
        split_last_pos = self._last_pos.split('.')
        last_row = int(split_last_pos[0])
        last_col = int(split_last_pos[1])
        last_char = self.text.get(str(last_row) + "." + str(last_col - 1), str(last_row) + "." + str(last_col))
        if last_char in ["{", "("]:
            # replace current row by the same content except the last character

            # insert the closed block with an indent inside
            self.text.insert(self.get_pos(),
                             self._indent * "\t" + last_char + "\n\n" +
                             self._indent * "\t" + self._get_closing_character(last_char)
                             )
            self._indent += 1
            self.set_pos(last_row + 2, 0)
            self.text.insert(self.get_pos(), self._indent * "\t")
            # at this stage, the cursor is positioned inside the block

        elif last_char in ["}", ")"]:
            if self._indent > 0:
                self._indent -= 1
        else:
            pass

    def _get_closing_character(self, last_char):
        if last_char == "{":
            return "}"
        elif last_char == "(":
            return ")"
        else:
            return ""

    def parse_interpret_highlight(self, event=None):
        """
        Parses the code in self.text and highlights it.
        :param event: Event for any key binding
        :return: FPL interpreter
        """
        self._parent_notebook.ide.window.config(cursor="wait")
        self._parent_notebook.ide.window.update_idletasks()
        # parse and interpret the code
        code = self.get_text()
        interpreter = fplinterpreter.FplInterpreter(self.title, code, self._parent_notebook.ide.fpl_parser)
        # reconfigure all tags
        self.reconfigure_all_tags()
        # add new tags
        list_indices = list()
        for item in interpreter.get_ast_list():
            current_index = str(item.line) + "." + str(item.col)
            list_indices.append(current_index)
            grammar_tags = self._theme.get_grammar_tags()
            # set all the tags for syntax highlighting while the parsed rules are added to the _listBoxSyntax
            if item.rule in grammar_tags:
                tag = grammar_tags[item.rule]
                last_index = current_index
                while len(list_indices) > 0 and last_index == current_index:
                    last_index = list_indices.pop()
                if len(list_indices) == 0:
                    last_index = "1.0"
                self.add_tag(tag, last_index, current_index)
        self._parent_notebook.ide.window.config(cursor="")
        return interpreter

    def parse_interpret_highlight_update_all(self, event=None):
        """
        Parses the code in self.text, highlights it. Moreover, updates the info (errors list, syntax tree).
        :param event: Event for any key binding
        :return: None
        """
        interpreter = self.parse_interpret_highlight()
        self._parent_notebook.ide.refresh_info(interpreter, self)

    def reformat_code(self, event=None):
        """
        Reformats the code inside self and highlights it again
        :param event: Event for any key binding
        :return: None
        """
        code = self.get_text()
        interpreter = fplinterpreter.FplInterpreter(self.title, code, self._parent_notebook.ide.fpl_parser)
        self.set_text(interpreter.prettyfied(), init=False)
        self.parse_interpret_highlight()

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
        # rewrite all line numbers
        self.linenumbers.redraw()
        # print the current position in the status bar of the ide
        pos = self._write_pos_in_status_bar()
        try:
            if self.text.is_dirty:
                # change the appearance title to "changed"
                self._parent_notebook.tab(self, text=self.title + "*")
                self._last_pos = pos
            else:
                # change the title to the original one
                self._parent_notebook.tab(self, text=self.title)
        except _tkinter.TclError:
            # ignore the error .!framewithlinenumbers is not managed by .!panedwindow4.!panedwindow.!customnotebook'
            # the very first time when of this event, the _parent_nodebook will not managed 'self' yet
            pass

    def _write_pos_in_status_bar(self):
        pos = self.get_pos()
        row = pos.split('.')[0]
        column = pos.split('.')[1]
        ide = self._parent_notebook.get_parent()
        ide.get_status_bar().set_status_text(self.title + " (R:" + row + " C:" + column + ")")
        return pos

    def set_text(self, code, init=True):
        if init:
            self.text.init_value(code)
        else:
            self.text.delete(1.0, END)
            self.text.insert(END, code)
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
