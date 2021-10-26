import re

"""
Converts the fpl_tatsu_format.ebnf tatsu format into a tree-sitter javascript grammar
The converted file is named fpl_tree_sitter_grammar.js.
Please do not edit this file since it will be overwritten the next time you start convert().
"""


class OutputLines(list):
    _indent = 0

    def increase_indent(self):
        self._indent += 2

    def decrease_indent(self):
        self._indent -= 2

    def append_line(self, text):
        self.append(self._indent * ' ' + text + "\n")

    def generate_grammar(self, fpl_grammar):
        regexp_rules = re.compile("[ \t]*([a-zA-z]+)[ ]*=(.*?);", re.S | re.M)
        for match in re.finditer(regexp_rules, fpl_grammar):
            rule_name = match.group(1)
            rule_def = match.group(2).strip()
            rule_def = rule_def.replace("\n", " ")
            if rule_name == "SemiColon":
                # regexp_rules will fail in recognizing the FPL terminal ";", handle this case separately
                self.append_line(rule_name + ": $ => \";\",")
            else:
                self.append_line(rule_name + ": $ => " + self.replace(rule_def, rule_name) + ", ")

    def replace(self, rule_def, rule_name):
        ret = ""
        rule_def = rule_def.strip()
        if rule_def[0] == "(" and rule_def[-1] == ")":
            i = self.look_for_closing("(", rule_def)
            if i >= len(rule_def):
                # create alternative
                split = rule_def[1:-2].strip().split("|")
                ret = "choice("
                precedence = 0
                for chunk in split:
                    chunk = chunk.strip()
                    ret += self.replace(chunk, rule_name) + ", "
                    '''
                    # add left associativity precedence for some lists
                    if rule_name in ["NamespaceIdentifier", "WildcardTheoryNamespace", "WildcardTheoryNamespaceList",
                                     "RuleOfInferenceList", "BuildingBlockList", "PredicateIdentifier",
                                     "PrimePredicate", "Identifier", "LocalizationList", 
                                     "VariableList", "VariableSpecificationList",
                                     "PropertyList", "VariableSpecification", "CommentWhitespaceList", "PredicateList",
                                     "ConditionFollowedByResultList", "Range", "TranslationList", "RangeInSignature",
                                     "VariableType", "Type", "ProofArgumentList"]:
                        precedence += 1
                        # higher precedence than the proceeding
                        if rule_name in ["Type", "VariableSpecification"]:
                            precedence += 1
                        ret += "prec.left(" + str(precedence) + "," + self.replace(chunk, rule_name) + "), "
                    else:
                        ret += self.replace(chunk, rule_name) + ", "
                    '''
                ret = ret[:-2] + ")"
            else:
                ret = self.create_sequence(rule_def, rule_name)
        elif rule_def[0] == "{" and rule_def[-2:] == "}*":
            i = self.look_for_closing("{", rule_def)
            if i >= len(rule_def):
                # create repeat
                split = self.split_preserving_paranthesis(rule_def[1:-2].strip())
                ret = "repeat("
                if len(split) > 1:
                    ret += "seq("
                for chunk in split:
                    ret += self.replace(chunk, rule_name) + ", "
                ret = ret[:-2] + ")"
                if len(split) > 1:
                    ret += ")"
            else:
                ret = self.create_sequence(rule_def, rule_name)
        elif rule_def[0] == "{" and rule_def[-2:] == "}+":
            i = self.look_for_closing("{", rule_def)
            if i >= len(rule_def):
                # create repeat1
                split = self.split_preserving_paranthesis(rule_def[1:-2].strip())
                ret = "repeat1("
                if len(split) > 1:
                    ret += "seq("
                for chunk in split:
                    ret += self.replace(chunk, rule_name) + ", "
                ret = ret[:-2] + ")"
                if len(split) > 1:
                    ret += ")"
            else:
                ret = self.create_sequence(rule_def, rule_name)
        elif rule_def[0] == "/" and rule_def[-1] == "/":
            # todo: Unfortunately, tree-sitter grammars do not yet support
            #  look-around, including look-ahead and look-behind
            # the regex /((?!:end).)*/ of the FPL rule ExtensionContent has to be replaced by something similar
            # but unfortunately not equivalent. The work-around would be to program an external scanner for tree-sitter
            # in C (see https://github.com/tree-sitter/tree-sitter-cli/issues/53)
            if rule_name == 'ExtensionContent':
                ret = '/.*/'
            else:
                ret = rule_def
        elif rule_def[0] == "\"" and rule_def[-1] == "\"":
            ret = rule_def
        elif rule_def[0] == "[" and rule_def[-1] == "]":
            i = self.look_for_closing("[", rule_def)
            if i >= len(rule_def):
                # create a choice
                split = self.split_preserving_paranthesis(rule_def[1:-1].strip())
                ret = "optional("
                if len(split) > 1:
                    ret += "seq("
                for chunk in split:
                    ret += self.replace(chunk, rule_name) + ", "
                ret = ret[:-2] + ")"
                if len(split) > 1:
                    ret += ")"
            else:
                ret = self.create_sequence(rule_def, rule_name)
        elif " " in rule_def:
            ret = self.create_sequence(rule_def, rule_name)
        else:
            ret = "$." + rule_def
        return ret

    def create_sequence(self, rule_def, rule_name):
        # create a sequence
        split = self.split_preserving_paranthesis(rule_def.strip())
        ret = "seq("
        for chunk in split:
            ret += self.replace(chunk, rule_name) + ", "
        ret = ret[:-2] + ")"
        return ret

    def look_for_closing(self, opening, rule_def):
        closing = ")"
        if opening == "(":
            pass
        elif opening == "[":
            closing = "]"
        else:
            closing = "}"

        count = 1
        i = 0
        while count > 0:
            i += 1
            if rule_def[i] == closing:
                count -= 1
            elif rule_def[i] == opening:
                count += 1
        i += 1
        if closing == "}":
            # add one character for ebnf repetitions "+" or "*" after "}"
            i += 2
        return i

    def split_preserving_paranthesis(self, rule_def):
        split = list()
        token = ""
        while len(rule_def) > 0:
            char = rule_def[0]
            if char != "(" and char != "{" and char != "[":
                if char == " ":
                    if token and token != "$":
                        split.append(token.strip())
                        token = ""
                    else:
                        rule_def = rule_def[1:]
                else:
                    # consume
                    token += char
                    rule_def = rule_def[1:]
            else:
                if token and token != "$":
                    split.append(token.strip())
                    token = ""
                i = self.look_for_closing(char, rule_def)
                token = rule_def[:i]
                rule_def = rule_def[i:].strip()
                split.append(token.strip())
                token = ""
        if token != "" and token != "$":
            split.append(token.strip())
        return split

    def add_conflicts(self):
        self.append_line("conflicts: $ => [")
        self.increase_indent()
        self.append_line("[$.NamespaceBlock],")
        self.append_line("[$.NamespaceIdentifier],")
        self.append_line("[$.WildcardTheoryNamespace],")
        self.append_line("[$.WildcardTheoryNamespaceList],")
        self.append_line("[$.RuleOfInferenceList],")
        self.append_line("[$.BuildingBlockList],")
        self.append_line("[$.AliasedId, $.PredicateIdentifier],")
        self.append_line("[$.PredicateWithArguments, $.PrimePredicate],")
        self.append_line("[$.AssignmentStatement, $.Identifier],")
        self.append_line("[$.LocalizationList],")
        self.append_line("[$.TheoryBlock],")
        self.append_line("[$.AliasedId],")
        self.append_line("[$.VariableList],")
        self.append_line("[$.VariableList, $.Entity],")
        self.append_line("[$.VariableSpecificationList],")
        self.append_line("[$.PropertyList],")
        self.append_line("[$.PredicateList],")
        self.append_line("[$.ConditionFollowedByResultList],")
        self.append_line("[$.Range],")
        self.append_line("[$.CoordList, $.Range],")
        self.append_line("[$.Coord, $.Identifier],")
        self.append_line("[$.Coord, $.Identifier, $.AssignmentStatement],")
        self.append_line("[$.TranslationList],")
        self.append_line("[$.PremiseBlock],")
        self.append_line("[$.PremiseConclusionBlock],")
        self.append_line("[$.FunctionalTermDefinitionBlock, $.Property, $.VariableSpecificationList],")
        self.append_line("[$.FunctionalTermDefinitionBlock, $.Property],")
        self.append_line("[$.CoordList],")
        self.append_line("[$.RangeInSignature],")
        self.append_line("[$.Type, $.Identifier],")
        self.append_line("[$.Property],")
        self.append_line("[$.FunctionalTermDefinitionBlock],")
        self.append_line("[$.DefinitionPredicate, $.Type],")
        self.append_line("[$.FunctionalTermSignature, $.Type],")
        self.append_line("[$.VariableSpecification, $.PrimePredicate],")
        self.append_line("[$.PredicateDefinitionBlock, $.VariableSpecificationList],")
        self.append_line("[$.ProofArgumentList],")
        self.append_line("[$.PredicateDefinitionBlock],")
        self.append_line("[$.AxiomBlock, $.VariableSpecificationList],")
        self.append_line("[$.AxiomBlock],")
        self.append_line("[$.ProofBlock],")
        self.append_line("[$.StatementList],")
        self.append_line("[$.EBNFTransl],")
        self.append_line("[$.EBNFTerm],")
        self.append_line("[$.DefinitionContentList],")
        self.append_line("[$.ObjectDefinitionBlock, $.Property, $.VariableSpecificationList],")
        self.append_line("[$.ObjectDefinitionBlock, $.Property],")
        self.append_line("[$.Justification],")
        self.append_line("[$.ObjectDefinitionBlock],")
        self.decrease_indent()
        self.append_line("],")


def convert(input_file, output_file):
    output_lines = OutputLines()
    output_lines.append_line("/* THIS IS AN AUTOMATICALLY GENERATED FILE VIA THE tree_sitter_converter.py UTILITY */")
    output_lines.append_line("/* IT CONTAINS THE CURRENT FPL GRAMMAR TO BE USED WITH tree-sitter */")
    output_lines.append_line("")
    output_lines.append_line("")
    output_lines.append_line("module.exports = grammar({")
    output_lines.increase_indent()
    output_lines.append_line("name: 'fpl',")
    output_lines.add_conflicts()
    output_lines.append_line("rules: {")
    output_lines.increase_indent()

    input_file_content = open(input_file, 'r')
    fpl_grammar = input_file_content.read()

    output_lines.generate_grammar(fpl_grammar)
    output_lines.decrease_indent()
    output_lines.append_line("    }")
    output_lines.decrease_indent()
    output_lines.append_line("});")

    output = open(output_file, 'w')
    output.writelines(output_lines)
    output.close()

    output = open("D:/Test/tree-sitter-fpl/grammar.js", 'w')
    output.writelines(output_lines)
    output.close()


convert("../../grammar/fpl_tatsu_format.ebnf", "../../grammar/fpl_tree_sitter_grammar.js")
