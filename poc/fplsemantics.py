from classes.Variable import Variable
from classes.IgnoreRules import IgnoreRules


class FPLSemantics(object):
    errors = None
    warnings = None
    parse_list = None
    _stack = None
    _minified = None
    _last_cst = None
    _context_stack = None  # used to distinguish different contexts while parsing and interpreting the same lexemes
    switcher = None

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.parse_list = []
        self._stack = []
        self._minified = ""
        self._last_cst = ""
        self._context_stack = []  # used to distinguish different contexts while parsing and interpreting the same lexemes

        self.switcher = {
            "Alias": self.inter_equals_cst,
            "alias": self.inter_equals_cst,
            "AliasedId": self.inter_equals_proceeding_ignored_rules,
            "All": self.inter_equals_cst,
            "all": self.inter_equals_cst,
            "Ampersand": self.inter_equals_cst,
            "AmpersandVariable": self.inter_equals_cst,
            "and": self.inter_equals_cst,
            "AnonymousDeclaration": self.inter_equals_cst,
            "AnonymousSignature": self.inter_equals_cst,
            "ArgumentIdentifier": self.inter_equals_cst,
            "ArgumentInference": self.inter_equals_cst,
            "ass": self.inter_equals_cst,
            "assert": self.inter_equals_cst,
            "AssertionStatement": self.inter_equals_cst,
            "Assignee": self.inter_equals_cst,
            "AssignmentStatement": self.inter_equals_cst,
            "assume": self.inter_equals_cst,
            "AssumedPredicate": self.inter_equals_cst,
            "AssumeHeader": self.inter_equals_cst,
            "At": self.inter_equals_cst,
            "AtList": self.inter_equals_proceeding_ignored_rules,
            "ax": self.inter_equals_cst,
            "Axiom": self.inter_equals_cst,
            "axiom": self.inter_equals_cst,
            "AxiomBlock": self.inter_equals_cst,
            "AxiomHeader": self.inter_equals_cst,
            "BuildingBlock": self.inter_equals_cst,
            "BuildingBlockList": self.inter_equals_cst,
            "CallModifier": self.inter_equals_cst,
            "case": self.inter_equals_cst,
            "CaseStatement": self.inter_equals_cst,
            "cl": self.inter_equals_cst,
            "class": self.inter_equals_cst,
            "ClassHeader": self.inter_equals_cst,
            "ClassInstance": self.inter_equals_cst,
            "ClosedOrOpenRange": self.inter_equals_cst,
            "Colon": self.inter_equals_cst,
            "ColonEqual": self.inter_equals_cst,
            "Comma": self.inter_equals_cst,
            "Comment": self.inter_equals_cst,
            "CompoundPredicate": self.inter_equals_cst,
            "con": self.inter_equals_cst,
            "conclusion": self.inter_equals_cst,
            "ConclusionBlock": self.inter_equals_cst,
            "ConclusionHeader": self.inter_equals_cst,
            "ConditionFollowedByResult": self.inter_equals_cst,
            "ConditionFollowedByResultList": self.inter_equals_cst,
            "conj": self.inter_equals_cst,
            "conjecture": self.inter_equals_cst,
            "Conjunction": self.inter_equals_cst,
            "Constructor": self.inter_equals_cst,
            "Coord": self.inter_equals_cst,
            "CoordInSignature": self.inter_equals_cst,
            "CoordList": self.inter_equals_cst,
            "cor": self.inter_equals_cst,
            "corollary": self.inter_equals_cst,
            "CW": self.inter_equals_proceeding_ignored_rules,
            "DefaultResult": self.inter_equals_cst,
            "Definition": self.inter_equals_cst,
            "DefinitionClass": self.inter_equals_cst,
            "DefinitionContent": self.inter_equals_cst,
            "DefinitionContentList": self.inter_equals_cst,
            "DefinitionFunctionalTerm": self.inter_equals_cst,
            "DefinitionPredicate": self.inter_equals_cst,
            "DefinitionProperty": self.inter_equals_cst,
            "DerivedPredicate": self.inter_equals_cst,
            "Digit": self.inter_equals_cst,
            "Disjunction": self.inter_equals_cst,
            "Dollar": self.inter_equals_cst,
            "Dot": self.inter_equals_cst,
            "EBNFBar": self.inter_equals_cst,
            "EBNFFactor": self.inter_equals_cst,
            "EBNFString": self.inter_equals_cst,
            "EBNFTerm": self.inter_equals_cst,
            "EBNFTransl": self.inter_equals_cst,
            "else": self.inter_equals_cst,
            "end": self.inter_equals_cst,
            "Entity": self.inter_equals_cst,
            "EntityWithCoord": self.inter_equals_cst,
            "Equivalence": self.inter_equals_cst,
            "ex": self.inter_equals_cst,
            "ExclamationMark": self.inter_equals_cst,
            "ExclusiveOr": self.inter_equals_cst,
            "Exists": self.inter_equals_cst,
            "ExistsHeader": self.inter_equals_cst,
            "ExistsTimesN": self.inter_equals_cst,
            "ext": self.inter_equals_cst,
            "extDigit": self.inter_equals_cst,
            "ExtensionBlock": self.inter_equals_cst,
            "ExtensionContent": self.inter_equals_cst,
            "ExtensionHeader": self.inter_equals_cst,
            "ExtensionTail": self.inter_equals_cst,
            "false": self.inter_equals_cst,
            "func": self.inter_equals_cst,
            "function": self.inter_equals_cst,
            "FunctionalTermDefinitionBlock": self.inter_equals_cst,
            "FunctionalTermHeader": self.inter_equals_cst,
            "FunctionalTermInstance": self.inter_equals_cst,
            "FunctionalTermSignature": self.inter_equals_cst,
            "GeneralType": self.inter_equals_cst,
            "Identifier": self.inter_equals_cst,
            "IdStartsWithCap": self.inter_equals_cst,
            "IdStartsWithSmallCase": self.inter_equals_cst,
            "iif": self.inter_equals_cst,
            "impl": self.inter_equals_cst,
            "Implication": self.inter_equals_cst,
            "ind": self.inter_equals_cst,
            "index": self.inter_equals_cst,
            "IndexHeader": self.inter_equals_cst,
            "IndexValue": self.inter_equals_cst,
            "inf": self.inter_equals_cst,
            "inference": self.inter_equals_cst,
            "InferenceHeader": self.inter_equals_cst,
            "InstanceBlock": self.inter_equals_cst,
            "is": self.inter_equals_cst,
            "IsOperator": self.inter_equals_cst,
            "IW": self.inter_equals_cst,
            "Justification": self.inter_equals_cst,
            "KeysOfVariadicVariable": self.inter_equals_cst,
            "LanguageCode": self.inter_equals_cst,
            "LeftBound": self.inter_equals_cst,
            "LeftBrace": self.inter_equals_cst,
            "LeftBracket": self.inter_equals_cst,
            "LeftParen": self.inter_equals_cst,
            "lem": self.inter_equals_cst,
            "lemma": self.inter_equals_cst,
            "loc": self.inter_equals_cst,
            "Localization": self.inter_equals_cst,
            "localization": self.inter_equals_cst,
            "LocalizationBlock": self.inter_equals_cst,
            "LocalizationHeader": self.inter_equals_cst,
            "LocalizationList": self.inter_equals_cst,
            "LongComment": self.inter_equals_cst,
            "LongTemplateHeader": self.inter_equals_cst,
            "loop": self.inter_equals_cst,
            "LoopStatement": self.inter_equals_cst,
            "mand": self.inter_equals_cst,
            "mandatory": self.inter_equals_cst,
            "Mapping": self.inter_equals_cst,
            "NamedVariableDeclaration": self.inter_equals_cst,
            "Namespace": self.inter_equals_cst,
            "NamespaceBlock": self.inter_equals_cst,
            "NamespaceIdentifier": self.inter_equals_proceeding_ignored_rules,
            "NamespaceModifier": self.inter_equals_cst,
            "Negation": self.inter_equals_cst,
            "not": self.inter_equals_cst,
            "obj": self.inter_equals_cst,
            "object": self.inter_equals_cst,
            "ObjectDefinitionBlock": self.inter_equals_cst,
            "ObjectHeader": self.inter_equals_cst,
            "opt": self.inter_equals_cst,
            "optional": self.inter_equals_cst,
            "or": self.inter_equals_cst,
            "ParamList": self.inter_equals_cst,
            "ParamTuple": self.inter_equals_cst,
            "ParenthesisedPredicate": self.inter_equals_cst,
            "Plus": self.inter_equals_cst,
            "post": self.inter_equals_cst,
            "postulate": self.inter_equals_cst,
            "pre": self.inter_equals_cst,
            "pred": self.inter_equals_cst,
            "predicate": self.inter_equals_cst,
            "Predicate": self.inter_equals_cst,
            "PredicateDefinitionBlock": self.inter_equals_cst,
            "PredicateHeader": self.inter_equals_cst,
            "PredicateIdentifier": self.inter_equals_proceeding_ignored_rules,
            "PredicateList": self.inter_equals_cst,
            "PredicateWithArguments": self.inter_equals_cst,
            "premise": self.inter_equals_cst,
            "PremiseBlock": self.inter_equals_cst,
            "PremiseConclusionBlock": self.inter_equals_cst,
            "PremiseHeader": self.inter_equals_cst,
            "PremiseOrOtherPredicate": self.inter_equals_cst,
            "prf": self.inter_equals_cst,
            "PrimePredicate": self.inter_equals_cst,
            "Proof": self.inter_equals_cst,
            "proof": self.inter_equals_cst,
            "ProofArgument": self.inter_equals_cst,
            "ProofArgumentList": self.inter_equals_cst,
            "ProofBlock": self.inter_equals_cst,
            "ProofHeadHeader": self.inter_equals_cst,
            "ProofIdentifier": self.inter_equals_cst,
            "prop": self.inter_equals_cst,
            "Property": self.inter_equals_cst,
            "PropertyHeader": self.inter_equals_cst,
            "PropertyList": self.inter_equals_cst,
            "proposition": self.inter_equals_cst,
            "py": self.inter_equals_cst,
            "PythonDelegate": self.inter_equals_cst,
            "PythonIdentifier": self.inter_equals_cst,
            "qed": self.inter_equals_cst,
            "QualifiedIdentifier": self.inter_equals_cst,
            "Range": self.inter_equals_cst,
            "range": self.inter_equals_cst,
            "RangeInSignature": self.inter_equals_cst,
            "RangeOrLoopBody": self.inter_equals_cst,
            "RangeStatement": self.inter_equals_cst,
            "ReferencedResultIdentifier": self.inter_equals_cst,
            "ret": self.inter_equals_cst,
            "return": self.inter_equals_cst,
            "ReturnHeader": self.inter_equals_cst,
            "ReturnStatement": self.inter_equals_cst,
            "rev": self.inter_equals_cst,
            "Revoke": self.inter_equals_cst,
            "revoke": self.inter_equals_cst,
            "RevokeHeader": self.inter_equals_cst,
            "RightBound": self.inter_equals_cst,
            "RightBrace": self.inter_equals_cst,
            "RightBracket": self.inter_equals_cst,
            "RightParen": self.inter_equals_cst,
            "RuleOfInference": self.inter_equals_cst,
            "RuleOfInferenceList": self.inter_equals_cst,
            "RulesOfInferenceBlock": self.inter_equals_cst,
            "self": self.inter_equals_cst,
            "SemiColon": self.inter_equals_cst,
            "Signature": self.inter_equals_cst,
            "Slash": self.inter_equals_cst,
            "Star": self.inter_equals_cst,
            "Statement": self.inter_equals_cst,
            "StatementList": self.inter_equals_cst,
            "SW": self.inter_equals_proceeding_ignored_rules,
            "template": self.inter_equals_cst,
            "TemplateHeader": self.inter_equals_cst,
            "th": self.inter_equals_cst,
            "theorem": self.inter_equals_cst,
            "TheoremLikeStatementOrConjecture": self.inter_equals_cst,
            "TheoremLikeStatementOrConjectureHeader": self.inter_equals_cst,
            "theory": self.inter_equals_cst,
            "TheoryBlock": self.inter_equals_cst,
            "TheoryHeader": self.inter_equals_cst,
            "thm": self.inter_equals_cst,
            "Tilde": self.inter_equals_cst,
            "To": self.inter_equals_cst,
            "tpl": self.inter_equals_cst,
            "Translation": self.inter_equals_cst,
            "TranslationList": self.inter_equals_cst,
            "trivial": self.inter_equals_cst,
            "true": self.inter_equals_cst,
            "TupleOfTypes": self.inter_equals_cst,
            "Type": self.inter_equals_cst,
            "TypeOrTupleOfTypes": self.inter_equals_cst,
            "TypeWithCoord": self.inter_equals_cst,
            "undef": self.inter_equals_cst,
            "undefined": self.inter_equals_cst,
            "UndefinedHeader": self.inter_equals_cst,
            "uses": self.inter_equals_cst,
            "UsesClause": self.inter_equals_cst,
            "Variable": self.inter_equals_proceeding_ignored_rules,
            "VariableDeclaration": self.inter_equals_cst,
            "VariableDeclarationList": self.inter_equals_cst,
            "VariableList": self.inter_equals_cst,
            "VariableSpecification": self.inter_equals_cst,
            "VariableSpecificationList": self.inter_equals_cst,
            "VariableType": self.inter_equals_cst,
            "VDash": self.inter_equals_cst,
            "WildcardTheoryNamespace": self.inter_equals_cst,
            "WildcardTheoryNamespaceList": self.inter_equals_cst,
            "XId": self.inter_equals_cst,
            "xor": self.inter_equals_cst,
        }

    @staticmethod
    def _debug():
        return True

    def get_minified(self):
        return self._minified

    def _default(self, ast):
        """
        If there’s no method matching the rule’s name, TatSu will invoke this method.
        :param ast: ast
        :return: ast
        """
        return ast

    def _minify(self, context):
        """
        Builds up a minified representation of the parsed fpl file during the parsing process
        :param context: parsing context
        :return:
        """
        rule = context.rule[0]
        if self._minified.find("func InverseOf(x:tplSetElem)->tplSetElem{retVal") > -1:
            # print("")
            pass
        if isinstance(context.cst, str):
            if rule == "Comment":
                pass
            elif rule == "CommentWhitespaceList":
                pass
            elif rule == "LongComment":
                pass
            elif rule == "IW":
                pass
            elif rule == "CW":
                pass
            elif rule == "Entity":
                self._last_cst = context.cst
            elif rule == "SW":
                self._minified += " "
            elif rule == "RightParen":
                self._minified += ")"
            elif rule == "RightBrace":
                self._minified += "}"
            elif rule == "RightChevron":
                self._minified += ">"
            elif rule == "tpl" and self._last_cst[0:3] == context.cst:
                self._last_cst = context.cst
            else:
                if self._last_cst == context.cst:
                    # prevent repeating of the parsed text because of nested productions
                    pass
                else:
                    self._last_cst = context.cst
                    # replace long versions by short versions
                    if context.cst == "assume":
                        self._minified += "ass"
                    elif context.cst == "axiom":
                        self._minified += "ax"
                    elif context.cst == "class":
                        self._minified += "cl"
                    elif context.cst == "conclusion":
                        self._minified += "con"
                    elif context.cst == "conjecture":
                        self._minified += "conj"
                    elif context.cst == "corollary":
                        self._minified += "cor"
                    elif context.cst == "function":
                        self._minified += "func"
                    elif context.cst == "inference":
                        self._minified += "inf"
                    elif context.cst == "lemma":
                        self._minified += "lem"
                    elif context.cst == "mandatory":
                        self._minified += "mand"
                    elif context.cst == "premise":
                        self._minified += "pre"
                    elif context.cst == "object":
                        self._minified += "obj"
                    elif context.cst == "optional":
                        self._minified += "opt"
                    elif context.cst == "predicate":
                        self._minified += "pred"
                    elif context.cst == "premise":
                        self._minified += "pre"
                    elif context.cst == "postulate":
                        self._minified += "post"
                    elif context.cst == "proof":
                        self._minified += "prf"
                    elif context.cst == "proposition":
                        self._minified += "prop"
                    elif context.cst == "return":
                        self._minified += "ret"
                    elif context.cst == "revoke":
                        self._minified += "ref"
                    elif context.cst == "syntax":
                        self._minified += "syn"
                    elif context.cst == "template":
                        self._minified += "tpl"
                    elif context.cst == "theorem":
                        self._minified += "thm"
                    elif context.cst == "theory":
                        self._minified += "th"
                    elif context.cst == "undefined":
                        self._minified += "undef"
                    else:
                        self._minified += context.cst

    def _postproc(self, context, ast):
        """
        This TatSu method will be called after each rule is processed.
        In contrast to _default, this method will receive the current parsing context as parameter:
        :param context: parsing context
        :param ast: ast
        :return: ast
        """

        # minify
        self._minify(context)
        d = dict()
        d["rule"] = context.rule[0]
        d["cst"] = context.cst
        d["pos"] = context.pos
        d["col"] = context.tokenizer.col
        d["line"] = context.tokenizer.line
        self.interpret_switcher(d, context)
        self.parse_list.append(d)
        return ast

    def interpret_switcher(self, parsing_info, context):
        rule = parsing_info["rule"]
        func = self.switcher.get(rule, lambda: "Invalid rule")
        # call the function depending on the rule in the switcher and modify its interpretation
        func(parsing_info, context)

    """
    All interpretation delegates
    """

    @staticmethod
    def inter_equals_cst(parsing_info: dict, context):
        """
        This delegate simply copies the cst as interpretation
        :param parsing_info: parsing info
        :param context: parsing context
        :return: None
        """
        parsing_info['inter'] = context.cst

    def inter_equals_proceeding_ignored_rules(self, parsing_info: dict, context):
        """
        This delegate removes all rules from parsing_list that can be ignored because the interpretation of
        the current rule is a string concatenation of the interpretations of to be ignored rules
        :param parsing_info: parsing info
        :param context: parsing context
        :return: None
        """
        ignore_proceeding_rules = IgnoreRules(self.parse_list, parsing_info['rule'])
        # the processed interpretation of the proceeding rules is not the interpretation of the current rule
        parsing_info['inter'] = ignore_proceeding_rules.inter()
        # replace the complex cst (e.g. lists and dictionaries) by None to save memory. We won't need it any more.
        parsing_info['cst'] = None

    def interpret(self, d, context):
        """
        Old: this method was completely replaced the method interpret_switcher. We keep it for reference only
        """
        inter = None  # to be calculated interpretation, depending on the rule
        rule = d["rule"]
        if rule == "IdStartsWithSmallCase":
            inter = context.cst
        elif rule == "Decimal":
            inter = context.cst
        elif rule == "definition" or rule == "def":
            inter = context.cst
        elif rule == "DefinitionHeader":
            inter = self._stack.pop()  # copy of "definition" or "def"
            self._context_stack.append("def")  # mark the beginning of a Definition
        elif rule == "IdStartsWithCap":
            inter = context.cst
        elif rule == "NumberOrCamelCaseId":
            inter = self._stack.pop()  # copy of "CamelCaseId" or "Decimal"
        elif rule == "object" or "obj":
            inter = context.cst
        elif rule == "":
            inter = context.cst
        elif rule == "ObjectHeader":
            inter = self._stack.pop()  # copy of "object" or "obj" or "template" or "tpl"
            if self.is_parsing_context("def") and (inter == "object" or inter == "obj"):
                self._context_stack.append("obj")  # mark the beginning of DefinitionObject
            elif self.is_parsing_context("def") and (inter == "template" or inter == "tpl"):
                self._context_stack.append("tpl")  # mark the beginning of DefinitionObject using a generic type
        elif rule == "ObjectType":
            inter = self._stack.pop()  # copy of "PascalCaseId"
        elif rule == "ObjVariableType":
            inter = self._stack.pop()  # copy of ObjectHeader or ObjectType
            if self.is_parsing_context("def", "obj", "PredicateIdentifier") \
                    or self.is_parsing_context("def", "tpl", "PredicateIdentifier"):
                self._context_stack.append("ObjVariableType")  # continue the beginning of DefinitionObject
                # at this stage, we know that
        elif rule == "IdStartsWithCap":
            inter = context.cst
        elif rule == "PredicateIdentifier":
            inter = self._stack.pop()  # copy of "PascalCaseId"
            if self.is_parsing_context("def", "obj") or self.is_parsing_context("def", "tpl"):
                self._context_stack.append("PredicateIdentifier")  # continue the beginning of DefinitionObject
        elif rule == "tpl":
            inter = context.cst
        elif rule == "template":
            inter = context.cst
        elif rule == "Variable":
            inter = Variable(self._stack.pop())
        d['inter'] = inter
        self._stack.append(inter)

    def is_parsing_context(self, *pars):
        """
        Check if the current parsing context ends with some given flags
        :param pars: list of keys
        :return: True, iif the context's tail corresponds to the keys in their order
        """
        if len(self._context_stack) < len(pars):
            return False
        else:
            is_context = True  # assume the context is there
            pos = len(self._context_stack) - len(pars)
            for x in pars:
                is_context = is_context and (x == self._context_stack[pos]['key'])
                if not is_context:
                    break
                pos += 1
            return is_context

    def push_context(self, key, value):
        """
        Pushes the context on a stack
        :param key: key of the context
        :param value: value of the context
        :return: None
        """
        d = dict()
        d['key'] = key
        d['val'] = value
        self._context_stack.append(d)

    def pop_context(self):
        """
        pops the last context from the stack
        :return: a dict with d['key'] == <key>, d['val'] == <val>
        """
        if len(self._context_stack) > 0:
            return self._context_stack.pop()
        else:
            return None
