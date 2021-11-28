#!/usr/bin/env python3
"""
This script is based on conditions on groups
The aim is to find a model that is a group by does not satisfy the special condition.

"""

import os
import sys
from ast import literal_eval as make_tuple
from openpyxl import load_workbook


comment_lines = ['% The aim is to find a model in a group by does not satisfy the special condition\n']

sos_line = "\nformulas(sos).\n"
goal_line = "\nformulas(goals).\n"
end_line = "end_of_list.\n"
group_strs = ["(x * y) * z = x * (y * z).\n", "1 * x = x.\n", "x * 1 = x.\n",
             "x' * x = 1.\n", "x * x' = 1.\n"]
commute_clause = "a * b = b * a."


def write_file(out_dir, id_string, additional_cond, basic_comp, power):
    """ writes out a mace4 input file. 
    Args:
        out_dir (str): output directory
        id_string (str): basic condition string
        additional_cond (str): additional condition
        basic_comp (str): basic component
        power (int):  power to apply to id_sting
    """
    clause = basic_comp
    all_clauses = list()
    for _ in range(2, power+1):
        clause = f"({clause}) * {basic_comp}"
        all_clauses.append(f"{clause} = 1.\n")
    fn = os.path.join(out_dir, f"group_{id_string}_{power}.in")
    with (open(fn, "w")) as fp:
        fp.writelines(comment_lines)
        fp.write(sos_line)
        fp.writelines(group_strs)
        fp.write(end_line)
        fp.write(goal_line)
        fp.write(f"{additional_cond}\n")
        fp.writelines(all_clauses)
        fp.write(end_line)


def gen_mace4_files(out_dir, level_from, level_to):
    """
    Args:
        out_dir (str): output directory
        level_from   (int): power level start
        level_to   (int): power level end, inclusive
    """
    for n in range(level_from, level_to+1):
        write_file(out_dir, "ab", commute_clause, "(a*b)", n)
    

if __name__ == "__main__":
    # e.g. ./src/groups/gen_formulas.py 2 9 inputs_group
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    if len(sys.argv) > 3:
        out_dir = sys.argv[3]
    else:
        out_dir = "."
    v = gen_mace4_files(out_dir, n1, n2)
    
