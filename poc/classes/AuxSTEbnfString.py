from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTEbnfString(AuxSTOutline):

    def __init__(self):
        super().__init__(parent=None, outline=AuxSTConstants.ebnf_string)  # noqa
        self.string = ""
