# The dictionary has the following meaning:
#   as long as the proceeding rules of the dictionary key is one of the list elements of the dictionary value,
#   they will be removed from the parse_list and the interpretation of the dictionary key rule will be
#   replaced by a concatenation of the interpretations of the removed proceeding rules
# Thus, while the EBNF rules create a complex AST, it can be simplified by a node with a one-string interpretation
aggr_rules_text = {
    # AtList   ::= '@'+
    'AtList': {'At'},
    # AliasedId  ::= IdStartsWithCap ( '.' IdStartsWithCap )+
    'AliasedId': {'IdStartsWithCap', 'Dot'},
    # CallModifier ::= '*' | '+'
    'CallModifier': {'Star', 'Plus'},
    # CW ::= IW | Comment | LongComment
    'CW': {'IW', 'Comment', 'LongComment'},
    # FunctionalTermHeader ::= 'function' | 'func'
    'FunctionalTermHeader': {'function', 'func'},
    # IndexHeader ::= 'index' | 'ind'
    'IndexHeader': {'index', 'ind'},
    # LeftBound ::= '[' '!'?
    'LeftBound': {'LeftBracket', 'ExclamationMark'},
    # RightBound ::= '!'? ']'
    'RightBound': {'RightBracket', 'ExclamationMark'},
    # LongTemplateHeader ::= TemplateHeader ( IdStartsWithCap | Digit )
    'LongTemplateHeader': {'TemplateHeader', 'IdStartsWithCap', 'Digit'},
    # ObjectHeader ::= 'object' | 'obj' | LongTemplateHeader | TemplateHeader
    'ObjectHeader': {'object', 'obj', 'LongTemplateHeader', 'TemplateHeader'},
    # NamespaceIdentifier ::= IdStartsWithCap ( '.' IdStartsWithCap )*
    'NamespaceIdentifier': {'IdStartsWithCap', 'Dot'},
    # PredicateIdentifier ::= AliasedId | IdStartsWithCap
    'PredicateIdentifier': {'IdStartsWithCap', 'AliasedId'},
    # PredicateHeader ::= 'predicate' | 'pred'
    'PredicateHeader': {'predicate', 'pred'},
    # SW ::= IW
    'SW': {'IW'},
    # TemplateHeader ::= 'template' | 'tpl'
    'TemplateHeader': {'template', 'tpl'},
    # Type ::= PredicateIdentifier | XId | PredicateHeader | FunctionalTermHeader | ObjectHeader
    'Type': {'PredicateIdentifier', 'XId', 'PredicateHeader', 'FunctionalTermHeader', 'ObjectHeader'},
    # Variable ::= IdStartsWithSmallCase
    'Variable': {'IdStartsWithSmallCase'},
    # XId ::= '@' 'ext' IdStartsWithCap
    'XId': {'IdStartsWithCap', 'At', 'ext'},
}

"""
Shortens the parse_list by removing all interpretations of ignorable rules depending on the  
dict "ignorable_rules" and the rule name
"""


class AuxAggrRulesText:
    # interpretation of the last after removing ignored rules from the parse_list
    _myInter = ""

    def __init__(self, parse_list: list, rule: str):
        can_be_ignored = parse_list[-1].rule_name() in aggr_rules_text[rule]
        while can_be_ignored:
            self._myInter = parse_list[-1].get_interpretation() + self._myInter
            # remove ignored rule
            parse_list.pop()
            if len(parse_list) > 0:
                can_be_ignored = parse_list[-1].rule_name() in aggr_rules_text[rule]
            else:
                can_be_ignored = False

    def inter(self):
        return self._myInter


