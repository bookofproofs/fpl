class AuxAstInfo:
    rule = None
    cst = None
    pos = None
    line = None
    col = None

    def __init__(self, context):
        self.rule = context.rule[0]
        self.cst = context.cst
        self.pos = context.pos
        self.col = context.tokenizer.col
        self.line = context.tokenizer.line