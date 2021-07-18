import _tkinter
from tkinter import *
from idetheme import DefaultTheme


class EditorText(Text):
    _theme = None
    is_dirty = False  # indicates if the string changed as compared to the _initial_value
    has_changed_content = False  # indicates if the string changed as compared to the previous one
    _initial_value = ""  # remember the initial value
    _last_value = ""  # remember the last value

    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self._theme = DefaultTheme()
        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def init_value(self, code):
        self.delete("1.0", END)
        self.insert("1.0", code)
        self._initial_value = self.get_value()
        self._last_value = self._initial_value
        self.edit_reset()
        self.is_dirty = False

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)
        # update the is_dirty and has_changed_content flags if something was added or deleted,
        if args[0] in ("insert", "replace", "delete"):
            value = self.get_value()
            self.has_changed_content = self._last_value != value
            self._last_value = value
            self.is_dirty = self._initial_value != value

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
        # self.is_dirty = False if self._initial_value == result else True
        return result

    def get_value(self):
        return self.get("1.0", END)

    def settings(self, background_color, foreground_color):
        self.config(bg=background_color, fg=foreground_color, insertbackground='white')
        self['font'] = self._theme.editor_font()
