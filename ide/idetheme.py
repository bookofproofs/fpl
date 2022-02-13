class DefaultTheme:

    @staticmethod
    def get_bg_color():
        return '#1E1E1E'

    @staticmethod
    def get_bg_color_selected():
        return '#2E2E2E'

    @staticmethod
    def get_fg_color():
        return '#DCDCDC'

    @staticmethod
    def editor_font():
        return ('consolas', '11')

    @staticmethod
    def notebook_font():
        return ('OpenSymbol', '9')

    @staticmethod
    def line_number_font():
        return ('consolas', '11')

    @staticmethod
    def get_tag_formatting():
        return {
            'comment': "#608B4E",
            'inbuilttype': "#A3D6A3",
            'keyword': "#4D9CD5",
            'type': "#39BCB0",
            'variable': "#ffdb58"
        }

    def get_notebook_style(self):
        return {
            ".": {
                "configure": {
                    "background": self.get_bg_color(),  # All except tabs
                    "highlightbackground": self.get_bg_color_selected(),  # All except tabs
                    "fieldbackground": self.get_bg_color_selected(),  # All except tabs
                    "font": self.notebook_font(),
                    "foreground": self.get_fg_color()
                }
            },
            "TNotebook": {
                "configure": {
                    "background": self.get_bg_color(),  # Your margin color
                    "highlightbackground": self.get_bg_color_selected(),  # All except tabs
                    "highlightthickness": 1,
                    "foreground": self.get_fg_color(),
                    "tabmargins": [0, 5, 0, 0],  # margins: left, top, right, separator
                },
                "map": {
                    "background": [("selected", self.get_bg_color_selected())],  # row color when selected
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": self.get_bg_color(),  # tab color when not selected
                    "highlightbackground": self.get_bg_color(),  # All except tabs
                    "padding": [10, 2],  # padding text vs. horizontal tab and text vs. vertical tab
                    "font": self.notebook_font(),
                    "foreground": self.get_fg_color()
                },
                "map": {
                    "background": [("selected", self.get_bg_color_selected())],  # Tab color when selected
                    "expand": [("selected", [1, 1, 1, 0])]  # text margins
                }
            },
            "TNotebook.treearea": {'sticky': 'ns'},
            "Treeview": {
                "configure": {
                    "background": self.get_bg_color(),  # Your margin color
                    "fieldbackground": self.get_bg_color(),  # All except tabs
                    "foreground": self.get_fg_color(),
                },
                "map": {
                    "background": [("selected", self.get_bg_color_selected())],  # row color when selected
                }
            },
        }


class TomorrowTheme(DefaultTheme):

    @staticmethod
    def get_bg_color():
        return '#262a2d'

    @staticmethod
    def get_bg_color_selected():
        return '#2E2E2E'

    @staticmethod
    def get_fg_color():
        return '#bcc0c6'

    @staticmethod
    def get_tag_formatting():
        return {
            'comment': "#608B4E",
            'inbuilttype': "#A3D6A3",
            'keyword': "#4D9CD5",
            'type': "#39BCB0",
            'mcomment': "#616161",
            'mstring': "#ffd54f",
            'mconstant': "#7e57c2",
            'mkeyword': "#ff5722",
            'mstorage': "#e91e63",
            'mstoragetype': "#259b24",
            'mclass': "#8bc34a",
            'mfunction': "#24bb6d5",
            'marguments': "#fd971f",
            'mtagname': "#26a69a",
            'mtagattr': "#ff5722",
            'mlibfunc': "#00bcd4",
            'mlibconstamt': "#03a9f4",
            'mlibclass': "#607d8b",

        }
