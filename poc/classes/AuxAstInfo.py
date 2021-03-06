class AuxAstInfo:
    rule = None
    cst = None
    pos = None
    line = None
    col = None
    mainType = None

    def __init__(self, context):
        self.mainType = "R"
        self.rule = context.rule[0]
        self.cst = context.cst
        self.pos = context.pos
        self.col = context.tokenizer.col
        self.line = context.tokenizer.line+1

    def __str__(self):
        return str(self.rule) + ":" + str(self.line + 1) + ":" + str(self.col) + ":" + str(self.pos)

    def to_tuple(self):
        return self.rule, self.line + 1, self.col, self.pos
