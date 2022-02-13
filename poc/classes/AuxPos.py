class AuxPos:

    def __init__(self):
        self.pos = 0
        self.line = 0
        self.col = 0

    def __str__(self):
        return str(self.line) + "." + str(self.col)

    def correct_offset(self, offset: int):
        self.pos -= offset
        self.col -= offset
