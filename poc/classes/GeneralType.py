from classes.AuxInterpretation import AuxInterpretation
import fplerror

# The list has the following meaning:
#   As long as the proceeding rules of GeneralType is one of the list elements,
#   they will be removed from the parse_list and the interpretation of the GeneralType will be
#   replaced by the object GeneralType
aggr_rules_GeneralType = {'CallModifier', 'Type', 'IndexHeader', 'TypeWithCoord'}


class GeneralType(AuxInterpretation):
    __objects = dict()

    def __init__(self, parse_list: list, inter: AuxInterpretation):
        self.clone(inter)
        self.__set = set()
        self.__objects['CallModifier'] = None
        self.__objects['Type'] = None
        self.__objects['TypeHasCoord'] = False

        can_be_ignored = parse_list[-1].rule_name() in aggr_rules_GeneralType
        while can_be_ignored:
            rule = parse_list[-1].rule_name()
            if rule == "CallModifier":
                self.__objects['CallModifier'] = parse_list[-1].get_interpretation()
            else:
                self.__objects['Type'] = parse_list[-1].get_interpretation()
                if rule == 'TypeWithCoord':
                    self.__objects['TypeHasCoord'] = True

            # remove ignored rule
            parse_list.pop()
            if len(parse_list) > 0:
                can_be_ignored = parse_list[-1].rule_name() in aggr_rules_GeneralType
            else:
                can_be_ignored = False
        self.set_interpretation(self.__objects)
