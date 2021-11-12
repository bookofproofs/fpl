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
    def get_grammar_tags():
        return {
            "alias": "keyword",
            "all": "keyword",
            "and": "keyword",
            "assert": "keyword",
            "ass": "keyword",
            "assume": "keyword",
            "ax": "keyword",
            "axiom": "keyword",
            "case": "keyword",
            "cl": "keyword",
            "class": "keyword",
            "conj": "keyword",
            "conjecture": "keyword",
            "con": "keyword",
            "conclusion": "keyword",
            "cor": "keyword",
            "corollary": "keyword",
            "Comment": "comment",
            "else": "keyword",
            "end": "keyword",
            "ext": "keyword",
            "ex": "keyword",
            "ExistsHeader": "keyword",
            "false": "keyword",
            "func": "inbuilttype",
            "function": "inbuilttype",
            "IdStartsWithCap": "type",
            "iif": "keyword",
            "impl": "keyword",
            "ind": "keyword",
            "index": "keyword",
            "inf": "keyword",
            "inference": "keyword",
            "is": "keyword",
            "lem": "keyword",
            "lemma": "keyword",
            "loc": "keyword",
            "localization": "keyword",
            "LongComment": "comment",
            "loop": "keyword",
            "mand": "keyword",
            "mandatory": "keyword",
            "not": "keyword",
            "obj": "inbuilttype",
            "object": "inbuilttype",
            "opt": "keyword",
            "optional": "keyword",
            "or": "keyword",
            "post": "keyword",
            "postulate": "keyword",
            "pre": "keyword",
            "pred": "inbuilttype",
            "predicate": "inbuilttype",
            "premise": "keyword",
            "prf": "keyword",
            "proof": "keyword",
            "ProofIdentifier": "type",
            "prop": "keyword",
            "proposition": "keyword",
            "py": "keyword",
            "PythonIdentifier": "keyword",
            "qed": "keyword",
            "range": "keyword",
            "ret": "keyword",
            "return": "keyword",
            "rev": "keyword",
            "revoke": "keyword",
            "self": "keyword",
            "thm": "keyword",
            "theorem": "keyword",
            "th": "keyword",
            "theory": "keyword",
            "trivial": "keyword",
            "true": "keyword",
            "undef": "keyword",
            "undefined": "keyword",
            "uses": "keyword",
            "Variable": "variable",
            "xor": "keyword"
        }

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
