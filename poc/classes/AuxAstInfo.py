"""
An class für retrieving key information from context objects during the parsing process of TatSu
that will be useful for the FPL Interpreter.
"""


class AuxAstInfo:

    def __init__(self, context, name_of_file):
        self.mainType = "R"  # rule (others are E=Error, W=Warning)
        self.rule = context.rule[0]
        self.cst = context.cst
        self.pos = context.pos
        self.col = context.tokenizer.col
        self.line = context.tokenizer.line + 1
        self.file = name_of_file
        # calculate the length of the cst for later correcting the parsing position (being at the end of the rule)
        # to its beginning
        self.length_cst = 0
        if type(context.cst) is str:
            self.length_cst = len(str(context.cst))

    def __str__(self):
        return str(self.rule) + ":" + self.pos_to_str()
    
    def to_tuple(self):
        return self.rule, self.line, self.col, self.pos

    def pos_to_str(self):
        return str(self.line) + "." + str(self.col)
