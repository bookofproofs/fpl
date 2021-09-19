"""
This class instantiates global names for all ide settings object in the configparser
that facilitate refactoring of these names in the project.
"""


class Settings:
    section_editor = "Editor"
    option_editor_tab_length = "tab length"
    preview_editor_tab_length = "Fpl\n{\n\tuses Fpl.Commons\n\ttheory\n\t{\n\t\t// do staff\n\t}\n}"
    section_paths = "Paths"
    option_paths_fpl_theories = "fpl theories"
    section_codereform = "Code Reformatting"
    option_codereform_1linecomppred = "one-line compound predicates"
    preview_codereform_1linecomppred_true = "and (Predicate1(),Predicate2())"
    preview_codereform_1linecomppred_false = "and\n(\n\tPredicate1(),\n\tPredicate2()\n)"

    @staticmethod
    def to_positive_integer(value: str):
        try:
            val = int(value)
            if val < 0:
                val = -val
            elif val == 0:
                val = 1
            return val
        except:
            return 1