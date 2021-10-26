from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.Xid import Xid


class ContextXid:
    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        type_info = Xid(i.parse_list, parsing_info)
        i.parse_list.append(type_info)
