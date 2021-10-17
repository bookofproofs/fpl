class AuxAstInfo:

    def __init__(self, context):
        self.mainType = "R"  # rule (others are E=Error, W=Warning)
        self.rule = context.rule[0]
        self.cst = context.cst
        self.pos = context.pos
        self.col = context.tokenizer.col
        self.line = context.tokenizer.line+1

    def __str__(self):
        return str(self.rule) + ":" + str(self.line) + ":" + str(self.col) + ":" + str(self.pos)

    def to_tuple(self):
        return self.rule, self.line, self.col, self.pos
