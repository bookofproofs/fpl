# The dictionary has the following meaning:
#   as long as the proceeding rules of the dictionary key is one of the list elements of the dictionary value,
#   they will be removed from the parse_list and the interpretation of the dictionary key rule will be
#   replaced by a concatenation of the interpretations of the removed proceeding rules
# Thus, while the EBNF rules create a complex AST, it can be simplified by a node with a one-string interpretation
ignorable_rules = {
    # AtList   ::= '@'+
    'AtList': ['At'],
    # AliasedId  ::= IdStartsWithCap ( '.' IdStartsWithCap )+
    'AliasedId': ['IdStartsWithCap', 'Dot'],
    # CW ::= IW | Comment | LongComment
    'CW': ['IW', 'Comment', 'LongComment'],
    # NamespaceIdentifier ::= IdStartsWithCap ( '.' IdStartsWithCap )*
    'NamespaceIdentifier': ['IdStartsWithCap', 'Dot'],
    # PredicateIdentifier ::= AliasedId | IdStartsWithCap
    'PredicateIdentifier': ['IdStartsWithCap', 'AliasedId'],
    # SW ::= IW
    'SW': ['IW'],
    # Variable ::= IdStartsWithSmallCase
    'Variable': ['IdStartsWithSmallCase']
}

"""
Shortens the parse_list by removing all interpretations of ignorable rules depending on the  
dict "ignorable_rules" and the rule name
"""


class IgnoreRules:
    # interpretation of the last after removing ignored rules from the parselist
    _myInter = ""

    def __init__(self, parse_list: list, rule: str):
        can_be_ignored = parse_list[-1]["rule"] in ignorable_rules[rule]
        while can_be_ignored:
            parse_list[-1]["rule"]
            self._myInter = parse_list[-1]['inter'] + self._myInter
            # remove ignored rule
            parse_list.pop()
            if len(parse_list) > 0:
                can_be_ignored = parse_list[-1]["rule"] in ignorable_rules[rule]
            else:
                can_be_ignored = False

    def inter(self):
        return self._myInter
