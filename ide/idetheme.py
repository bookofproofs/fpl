class Theme:

    def get_bg_color(self):
        return '#362f2e'

    def get_fg_color(self):
        return '#d2ded1'

    def editor_font(self):
        return ('consolas', '11')

    def line_number_font(self):
        return ('consolas', '11')

    def get_grammar_tags(self):
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

    def get_tag_formatting(self):
        # tp cancer Color Palette (from https://www.color-hex.com/color-palette/111278, by tsphilip)
        return {
            'comment': "#93e9be",
            'inbuilttype': "#e5c3c6",
            'keyword': "#ff7e47",
            'type': "#00cccc",
            'variable': "#ffdb58"
        }

