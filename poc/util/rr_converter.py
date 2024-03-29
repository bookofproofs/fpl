import re

"""
Converts the fpl_tatsu_format.ebnf tatsu format into a WC3 notation
that is compatible with the Railroad Diagram generator. 
The converted file is named fpl_rr_format.ebnf.
Please do not edit this file since it will be overwritten the next time you start convert().
"""


def convert(input_file, output_file):
    input_file_content = open(input_file, 'r')
    input_lines = input_file_content.readlines()
    output_lines = list()
    output_lines.append("/* THIS IS AN AUTOMATICALLY GENERATED FILE VIA THE rr_converter.py UTILITY */\n")
    output_lines.append("/* IT CONTAINS THE CURRENT FPL GRAMMAR TO BE USED WITH THE Railroad Diagram Generator */\n")
    output_lines.append("\n")
    output_lines.append("\n")
    regexp = re.compile(r"[a-z0-9\_]+\:")
    for line in input_lines:
        # ignore tatsu grammar directives and separator input lines
        if line.strip() == ";":
            line = line.replace(";", "")
        line = line.replace("[ ", "(").replace(" ]", ")?")  # syntax für optional productions
        line = line.replace("}*", ")*")  # syntax für choice productions
        line = line.replace("}+", ")+")  # syntax für choice productions
        line = line.replace("{ ", "( ").replace("} ", ") ")  # syntax für choice productions
        if line.strip() != "" and "@name" not in line and "@@" not in line and "----" not in line:
            if "# " in line:
                line = "/* " + line.strip()[2:] + " */\n"
            elif line.strip()[0] == "/" and line.strip()[-1] == "/":
                line = "regular_expression '" + line.strip() + "'\n"  # syntax for regex
            # skip all annotations
            if not regexp.search(line):
                line = line.replace("$", "")
                if line.find(":=") == -1:
                    output_lines.append(line.replace("=", "::="))
                else:
                    # prevent replacing "=" inside the assignment
                    output_lines.append(line)
    output = open(output_file, 'w')
    output.writelines(output_lines)
    output.close()


convert("../../grammar/fpl_tatsu_format.ebnf", "../../grammar/fpl_rr_format.ebnf")
