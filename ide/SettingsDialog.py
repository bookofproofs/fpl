import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from ide.idetheme import DefaultTheme
from ide.Settings import Settings
import os


class SettingsDialog(tk.Toplevel):
    ide = None
    _root_window = None
    _theme = None
    _mainframe = None
    _config_editor_pane = None
    _notebook = None
    _config_browser_pane = None
    _config_browser_tree = None

    def __init__(self, ide):
        super().__init__(ide.window)
        self.ide = ide
        self._theme = DefaultTheme()
        self.resizable()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (750 / 2))
        y_coordinate = int((screen_height / 2) - (400 / 2))
        self.geometry("{}x{}+{}+{}".format(750, 400, x_coordinate, y_coordinate))
        self.title("FPL IDE Settings")

        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=1)

        left_pane = tk.PanedWindow(main_pane, width=300)
        self._config_browser_pane = tk.PanedWindow(main_pane, bg=self._theme.get_bg_color(), orient=tk.VERTICAL)

        self._config_browser_tree = ttk.Treeview(left_pane)
        self._config_browser_tree.bind("<Double-1>", self._on_setting_doubleclick)
        for section in self.ide.config.sections():
            j = self._config_browser_tree.insert('', 'end', text=section.capitalize())
            for option in self.ide.config.options(section):
                self._config_browser_tree.insert(j, 'end', text=option.capitalize())

        left_pane.add(self._config_browser_tree)

        right = tk.Label(self._config_browser_pane, text="Editing Settings not implemented yet",
                         bg=self._theme.get_bg_color(),
                         fg=self._theme.get_fg_color())
        self._config_browser_pane.add(right)

        main_pane.add(left_pane)
        main_pane.add(self._config_browser_pane)

    def _on_closing(self):
        self._apply_some_settings()
        self.destroy()

    def _apply_some_settings(self):
        """
        Applies all settings that can be applied without re-opening the ide
        :return: None
        """
        # apply tab_length to all open editors
        self._apply_tab_length_to_all_open_editors()

    def _apply_tab_length_to_all_open_editors(self):
        notebook = self.ide.get_editor_notebook()
        for file in notebook.get_files():
            editor_info = notebook.get_files()[file]
            editor_info.configure_tab_width(
                self.ide.config.get(Settings.section_editor, Settings.option_editor_tab_length))

    @staticmethod
    def __add_scrollbar(frame, widget):
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        scrollbar.config(command=widget.yview)

    def _on_setting_doubleclick(self, event=None):
        self._clear_config_browser_pane()
        path = self._get_full_path_of_clicked_config()
        self._refresh_config_browser_pane(path)

    def _clear_config_browser_pane(self):
        for key in list(self._config_browser_pane.children):
            widget = self._config_browser_pane.children[key]
            widget.destroy()

    def _get_full_path_of_clicked_config(self):
        item_iid = self._config_browser_tree.selection()[0]
        parent_iid = self._config_browser_tree.parent(item_iid)
        return [self._config_browser_tree.item(parent_iid)['text'].lower(),
                self._config_browser_tree.item(item_iid)['text'].lower()]

    def _refresh_config_browser_pane(self, path: list):
        if path[0] != '':
            # the user clicked a leaf
            if path[0] == Settings.section_editor.lower():
                if path[1] == Settings.option_editor_tab_length.lower():
                    self._option_editor_tab_length()
                else:
                    self._config_not_implemented()
            elif path[0] == Settings.section_paths.lower():
                if path[1] == Settings.option_paths_fpl_theories.lower():
                    self._path_fpl_theories()
                else:
                    self._config_not_implemented()
            elif path[0] == Settings.section_codereform.lower():
                if path[1] == Settings.option_codereform_1linecomppred.lower():
                    self._option_codereform_1linecomppred()
                else:
                    self._config_not_implemented()
            else:
                self._config_section_not_implemented()
        else:
            # the user clicked not a leaf. Do nothing
            pass

    def _path_fpl_theories(self):
        label = tk.Label(self._config_browser_pane, text="Path to " + Settings.option_paths_fpl_theories.capitalize(),
                         anchor=tk.W,
                         bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._config_browser_pane.add(label)
        one_line_frame = tk.Frame(self._config_browser_pane, height=20, bg=self._theme.get_bg_color())
        self.entry_var = tk.StringVar()
        self.entry_var.set(self.ide.config.get(Settings.section_paths, Settings.option_paths_fpl_theories))
        self.entry_var.trace("w", lambda name, index, mode, var=self.entry_var: self.option_paths_fpl_theories_trace(
            self.entry_var))
        entry = tk.Entry(one_line_frame, textvariable=self.entry_var, bg=self._theme.get_bg_color(),
                         fg=self._theme.get_fg_color())
        entry.grid(row=0, column=0, sticky=tk.EW)

        one_line_frame.columnconfigure(0, weight=80)
        btn = tk.Button(one_line_frame, bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color(), text="...")
        btn.grid(row=0, column=1, sticky=tk.EW)
        btn.bind("<Button-1>", self._select_dir)
        self._config_browser_pane.add(one_line_frame)
        self.option_paths_fpl_theories_trace(self.entry_var)

    def _select_dir(self):
        directory_name = askdirectory(
            initialdir=self.ide.config.get(Settings.section_paths, Settings.option_paths_fpl_theories))
        if directory_name == "":
            # the user cancelled
            return
        self.entry_var.set(directory_name)
        self.focus_set()

    def option_paths_fpl_theories_trace(self, entry_value):
        if os.path.isdir(entry_value.get()):
            self.ide.config.set(Settings.section_paths, Settings.option_paths_fpl_theories, entry_value.get())
        else:
            self.ide.config.set(Settings.section_paths, Settings.option_paths_fpl_theories,
                                os.path.dirname(__file__) + "/")
        self._write_config()

    def _option_editor_tab_length(self):
        one_line_frame = tk.Frame(self._config_browser_pane, height=20, bg=self._theme.get_bg_color())
        tab_length = Settings.to_positive_integer(
            self.ide.config.get(Settings.section_editor, Settings.option_editor_tab_length))
        entry_var = tk.StringVar()
        entry_var.set(str(tab_length))
        entry_var.trace("w", lambda name, index, mode, var=entry_var: self._option_editor_tab_length_trace(entry_var))
        tk.Entry(one_line_frame,
                 textvariable=entry_var,
                 bg=self._theme.get_bg_color(),
                 fg=self._theme.get_fg_color(),
                 justify="right",
                 width=15
                 ).grid(row=0, column=0)
        tk.Label(one_line_frame, text=Settings.option_editor_tab_length.capitalize(), anchor=tk.W,
                 bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color()).grid(row=0, column=1)
        self._config_browser_pane.add(one_line_frame)
        label = tk.Label(self._config_browser_pane, text="Preview:", anchor=tk.W,
                         bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._config_browser_pane.add(label)

        self._preview_text = tk.Text(self._config_browser_pane, height=10, width=50)
        self._preview_text.config(bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color(),
                                  insertbackground='white')
        self._config_browser_pane.add(self._preview_text)
        self._preview_text['font'] = self._theme.editor_font()
        self._option_editor_tab_length_trace(entry_var)

    def _option_editor_tab_length_trace(self, entry_value):
        entry_val = Settings.to_positive_integer(entry_value.get())
        self._preview_text.delete("1.0", tk.END)
        font = tk.font.Font(font=self._preview_text['font'])
        self._preview_text.config(tabs=font.measure(' ' * entry_val))
        self._preview_text.insert("1.0", Settings.preview_editor_tab_length)
        self.ide.config.set(Settings.section_editor, Settings.option_editor_tab_length, entry_val)
        self._write_config()

    def _option_codereform_1linecomppred(self):
        self.check_var = tk.IntVar()
        boolval = self.ide.config.get(Settings.section_codereform, Settings.option_codereform_1linecomppred)
        if boolval == "True":
            self.check_var.set(1)
        else:
            self.check_var.set(0)
        check = tk.Checkbutton(self._config_browser_pane,
                               text=Settings.option_codereform_1linecomppred.capitalize(),
                               variable=self.check_var,
                               bg=self._theme.get_bg_color(),
                               fg=self._theme.get_fg_color(),
                               anchor=tk.NW,
                               height=2,
                               command=self.__option_codereform_1linecomppred_click)
        self._config_browser_pane.add(check)
        label = tk.Label(self._config_browser_pane, text="Preview:", anchor=tk.W,
                         bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color())
        self._config_browser_pane.add(label)
        self._preview_text = tk.Text(self._config_browser_pane, height=10, width=50)
        self._preview_text.config(bg=self._theme.get_bg_color(), fg=self._theme.get_fg_color(),
                                  insertbackground='white')
        self._config_browser_pane.add(self._preview_text)
        self._preview_text['font'] = self._theme.editor_font()
        self.__option_codereform_1linecomppred_click()

    def __option_codereform_1linecomppred_click(self):
        self._preview_text.delete("1.0", tk.END)
        if self.check_var.get():
            self._preview_text.insert("1.0", Settings.preview_codereform_1linecomppred_true)
            self.ide.config.set(Settings.section_codereform, Settings.option_codereform_1linecomppred, True)
        else:
            self._preview_text.insert("1.0", Settings.preview_codereform_1linecomppred_false)
            self.ide.config.set(Settings.section_codereform, Settings.option_codereform_1linecomppred, False)
        self._write_config()

    def _config_not_implemented(self):
        lbl = tk.Label(self._config_browser_pane, text="The editor for this settings not implemented yet!",
                       bg=self._theme.get_bg_color(),
                       fg=self._theme.get_fg_color())
        self._config_browser_pane.add(lbl)

    def _config_section_not_implemented(self):
        lbl = tk.Label(self._config_browser_pane, text="The editor for this section not implemented yet!",
                       bg=self._theme.get_bg_color(),
                       fg=self._theme.get_fg_color())
        self._config_browser_pane.add(lbl)

    def _write_config(self):
        cfgfile = open(os.path.dirname(__file__) + "/config.ini", "w")
        self.ide.config.write(cfgfile)
