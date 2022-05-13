# solution adapted from https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
# By Bryan Oakley
import _tkinter
import tkinter as tk
from ide.idetheme import DefaultTheme
from ide.TextLineNumbers import TextLineNumbers
from ide.EditorText import EditorText
import tkinter.font as tkfont
from ide.Settings import Settings


class FrameWithLineNumbers(tk.Frame):

    def __init__(self, parent_note_book, title, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self._parent_notebook = parent_note_book  # parent notebook containing this Frame
        self._theme = DefaultTheme()
        self.text = EditorText(self, undo=True)
        self._last_pos = "1.0"
        self._number_spaces_per_tab = 3
        self.is_new = False  # is True if this is a new file, or False, if it was loaded from disk
        self.text.settings(self._theme.get_bg_color(), self._theme.get_fg_color())
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)
        self.to_be_parsed_and_interpreted = False
        self.title = title
        self.configure_tab_width(
            self._parent_notebook.ide.model.config.get(Settings.section_editor, Settings.option_editor_tab_length)
        )
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill=tk.BOTH, expand=True)

        self.text.bind("<<Change>>", self.on_change)
        self.text.bind('<Return>', self._press_enter)
        self.text.bind('<Key>', self._key_pressed)
        self.text.bind('<Tab>', self._press_tab)
        self.text.bind('<Shift-Tab>', self._press_shift_tab)
        self.text.bind("<Configure>", self.on_change)

    def configure_tab_width(self, number_spaces):
        font = tkfont.Font(font=self.text['font'])
        self.text.config(tabs=font.measure(' ' * Settings.to_positive_integer(number_spaces)))

    def _key_pressed(self, event):
        split_last_pos = self.get_pos().split('.')
        last_row = int(split_last_pos[0])
        last_col = int(split_last_pos[1])
        if event.char in ["(", "[", "{"]:
            # Enter a closing brace when an opening brace was entered
            self.text.insert(self.get_pos(), event.char + self._get_closing_character(event.char))
            self.set_pos(last_row, last_col + 1)
            return 'break'
        elif event.char in [")", "]", "}"]:
            last_char = self.text.get(str(last_row) + "." + str(last_col), str(last_row) + "." + str(last_col + 1))
            if last_char == event.char:
                # prevent the entry of closing braces if there is already one at the current cursor position
                # However, move the position one character to the right
                self.set_pos(last_row, last_col + 1)
                return 'break'

    def _press_tab(self, event):
        """
        Handles the event when the user presses the tab key and increases the indentation of the selection.
        :param event: key event
        :return: None
        """
        if self.text.index(tk.SEL_FIRST) == "None" or self.text.index(tk.SEL_LAST) == "None":
            # prevent indenting anything if there is no current selection
            return
        # remember position of old text
        selected_text = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        # create replacement
        selection_replacement = ""
        for line in selected_text.splitlines():
            selection_replacement += "\t" + line + "\n"

        self.__replace_selection_by_text_and_select_it(selection_replacement)
        return "break"

    def __replace_selection_by_text_and_select_it(self, text: str):
        # remember first position
        pos_first = self.text.index(tk.SEL_FIRST)
        first_line = int(pos_first.split('.')[0])
        # delete all select
        self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        # insert new selection
        self.text.insert(pos_first, text)
        # identify where the new selection should end
        pos_last = str(len(text.splitlines()) + first_line) + ".0"
        # mark the text selected
        self.text.tag_add(tk.SEL, pos_first, pos_last)

    def _press_shift_tab(self, event):
        """
        Handles the event when the user presses the Shift tab key and decreases the indentation of the selection.
        :param event: key event
        :return: None
        """
        if self.text.index(tk.SEL_FIRST) == "None" or self.text.index(tk.SEL_LAST) == "None":
            # prevent outdenting anything if there is no current selection
            return
        # remember position of old text
        selected_text = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        # create replacement
        selection_replacement = ""
        for line in selected_text.splitlines():
            if len(line) > 0:
                if line[0] == " " or line[0] == "\t":
                    line = line[1:]
            selection_replacement += line + "\n"
        self.__replace_selection_by_text_and_select_it(selection_replacement)
        return "break"

    def _press_enter(self, event):
        text_to_the_left = self.text.get("0.0", self.get_pos())
        indent = self.__determine_current_indent(text_to_the_left, "{")
        split_pos = self.get_pos().split('.')
        last_row = int(split_pos[0])
        last_col = int(split_pos[1])
        possible_brackets = ""
        if last_col > 0:
            possible_brackets = self.text.get(str(last_row) + "." + str(last_col - 1),
                                              str(last_row) + "." + str(last_col + 1))
        if possible_brackets in ["{}"]:
            self.__insert_indented_brackets(last_row, last_col, indent - 1, possible_brackets, True)
        elif possible_brackets in ["()", "[]"]:
            self.__insert_indented_brackets(last_row, last_col, indent, possible_brackets, False)
        else:
            # new line entered with nothing to the left, so insert the line to the right indented
            self.text.insert(self.get_pos(), "\n" + indent * "\t")
        # do not handle new lines on your own
        return "break"

    def __determine_current_indent(self, text: str, bracket: str):
        indent = 0
        if len(text) > 0:
            i = 0
            stack = []
            while i < len(text):
                if text[i] == bracket:
                    stack.append(text[i])
                    indent += 1
                elif text[i] == self._get_closing_character(bracket):
                    if len(stack) > 0:
                        stack.pop()
                        indent -= 1
                i += 1
        return indent

    def __insert_indented_brackets(self, at_row, at_column, indent: int, possible_brackets: str, newline: bool):
        # insert an indented new block
        if newline:
            self.text.insert(str(at_row) + "." + str(at_column - 1), "\n" + indent * "\t")
            self.text.insert(str(at_row + 1) + "." + str(indent + 1), "\n\n" + indent * "\t")
            # increase indent and insert it inside this block
            self.set_pos(at_row + 2, 0)
            self.text.insert(self.get_pos(), (indent + 1) * "\t")
            # at this stage, the cursor is positioned inside the block at an indented position
        else:
            self.text.insert(str(at_row) + "." + str(at_column), "\n" + indent * "\t")

    def _get_closing_character(self, opening):
        if opening == "{":
            return "}"
        elif opening == "(":
            return ")"
        elif opening == "[":
            return "]"
        else:
            return ""

    def reformat_code(self, event=None):
        """
        Reformats the code inside self and highlights it again
        :param event: Event for any key binding
        :return: None
        """
        self._parent_notebook.ide.window.config(cursor="wait")
        self._parent_notebook.ide.update_idletasks()
        code = self.get_text()
        ide_model = self._parent_notebook.ide.model
        ide_model.fpl_source_transformer.syntax_transform_from_source(code)
        self.set_text(ide_model.fpl_source_transformer.get_prettified(), init=False)

        # make sure the highlighting is updated according to the re-formatted code
        ide_model.fpl_interpreter.forget_file(self.title)
        code = self.get_text()

        # replace the code in the library
        ide_model.refresh_file_in_library(self.title, code)
        self.parse_interpret_highlight_update_all()
        self._parent_notebook.ide.window.config(cursor="")

    def on_change(self, event):
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
        column = str(int(pos.split('.')[1]) + 1)
        ide = self._parent_notebook.get_parent()
        ide.get_status_bar().set_text(self.title + " (R:" + row + " C:" + column + ")")
        return pos

    def set_text(self, code, init=True):
        if init:
            self.text.init_value(code)
        else:
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, code)
        self.reconfigure_all_tags()

    def get_text(self):
        return self.text.get_value()

    def get_pos(self):
        return self.text.index(tk.INSERT)

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
        # remove all existing tags
        tags = self._theme.get_tag_formatting()
        self.text.tag_delete(list(tags) + ["err"])
        # add new tags
        self.text.tag_config('err', underline=True, underlinefg='red')
        for tag in tags:
            self.text.tag_config(tag, foreground=tags[tag])

    def add_tag(self, tag, start_index, end_index):
        formattings = self._theme.get_tag_formatting()
        if tag in formattings:
            self.text.tag_add(tag, start_index, end_index)

    def add_error_tag(self, start_index, end_index=None):
        if end_index is None:
            self.text.tag_add('err', index1=start_index)
        else:
            self.text.tag_add('err', index1=start_index, index2=end_index)
