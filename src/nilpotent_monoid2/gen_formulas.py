#!/usr/bin/env python3
"""
This script is based on https://arxiv.org/pdf/1911.05817.pdf. 
It generates all formulas from 4 up to level n for the lattice of subvarieties of nilpotent monoid of order 2 (denoted by N_1_2).
Level 0 is bottom of Figure 13 on p.40. 
Each level, except level 0 and level 1, has 2 nodes.  Level 0 and level 1 each has one node, and the top level also has one node.
Each node on the upper ladder has 2 subvarieties, and each node on the lower ladder has one subvariety
The aim is to find a model in the variety but not in the subvariety.

Input level must be at least 2.
"""

import os
import sys


comment_lines = ['% This Mace4 inputs file is based on the paper https://arxiv.org/pdf/1911.05817.pdf\n',
                 '% Figure 13 on page 40 shows the lattice of subvarieties of N_1_2.\n',
                 '% Level 0 is the bottom row (with only one node 0), top level also has only one node N1_2, \n',
                 '% next level has one node, but all other levels have 2 nodes\n',
                 '% Each line represent a branch, is either a left branch or a right branch.\n',
                 '% The top ladder has both left and right branches, but the bottom ladder has only right branches.'
                 '% The top end of the branch (line) is a variety, and the bottom end of the branch is a subvariety,',
                 '% The aim is to find a model in the variety but not in the subvariety\n',
                 '% sos is the variety, and goals represent the subvariety.\n']
sos_line = "\nformulas(sos).\n"
goal_line = "\nformulas(goals).\n"
end_line = "end_of_list.\n"
basic_str = ['(x * y) * z = x * (y * z).\n',  '(x * x) * x = x * x.\n', 'x * y = y * x.']


def debug_print(level, ladder, branch, v):
    print(f"level {level}, {ladder}, {branch}: {v}")


def make_clause_lower(level):
    """ Construct strings that Mace4 understands: e.g. (x1 * x2) * x3 for the lower ladder of a particular level
    Args:
        level: the level for which the lower clauses are to be generated
    Returns:
        (List[str]): a list of 2 strings representing the lower clauses, e.g ["x1 * x2", "y1 * y2"]
    """
    left_clause = "x1 * x2"
    right_clause = "y1 * y2"
    for w in range(2, level+1):
        left_clause = f"({left_clause}) * x{w+1}"
        right_clause = f"({right_clause}) * y{w+1}"
    return [left_clause, right_clause]


def make_clause_upper(level):
    """ Construct strings that Mace4 understands: e.g. (x1 * x2) * x3 for the upper ladder of a particular level
    Args:
        level: the level for which the clauses for the upper ladder are to be generated
    Returns:
        (List[str]): a list of 2 strings representing the lower clauses,  e.g ["(x1 * x1) * x2", "x1 * x2"]. 
    """
    left_clause = "x1 * x1"
    right_clause = "x1"
    for w in range(2, level+1):
        left_clause = f"({left_clause}) * x{w}"
        right_clause = f"({right_clause}) * x{w}"
    return [left_clause, right_clause]


def gen_mace4_formulas_lower(level):
    """ generate mace4 formula for lower ladder in Fig. 13 on page 40 of the paper
    Args:
        level: the level for which the Mace4 formulas are to be generated for the lower ladder
    Returns:
        (List[List[str]]): a list of 2 items. The first is empty, the second is the formulas for the right branch
        e.g. [[], ['(x1 * x2) * x3 = (y1 * y2) * y3', 'x1 * x2 = y1 * y2']]
    """
    lower = make_clause_lower(level)
    lower_sub = make_clause_lower(level - 1)
    return [[], [f"{lower[0]} = {lower[1]}.", f"{lower_sub[0]} = {lower_sub[1]}." ]]


def gen_mace4_formulas_upper(level):
    """ generate mace4 formula for lower ladder in Fig. 13 on page 40 of the paper
    Args:
        level: the level for which the Mace4 formulas are to be generated for the lower ladder
    Returns:
        (List[List[str]]): a list of 2 items. The first is the formulas for the left branch,
        the second is the formulas for the right branch
        e.g. [['(x1 * x1) * x2 = x1 * x2', 'x1 * x2 = y1 * y2'], ['(x1 * x1) * x2 = x1 * x2', 'x1 * x1 = x1']]
        For each branch, the first item has the formulas for the variety, and the second, the subvariety
    """
    upper = make_clause_upper(level)
    upper_sub = make_clause_upper(level - 1)
    lower_sub = make_clause_lower(level - 1)
    return [[f"{upper[0]} = {upper[1]}.", f"{lower_sub[0]} = {lower_sub[1]}." ],
            [f"{upper[0]} = {upper[1]}.", f"{upper_sub[0]} = {upper_sub[1]}." ]]


def write_file(out_dir, level, ladder, branch, mace_formulas):
    """ writes out a mace4 input file. "bottom" level implies "top" level, so the "goal"
        is the "bottom" level clause so to find a model in the "bigger" algebra but not in
        the smaller algebra.
    Args:
        out_dir (str): output directory
        level (int):   level in Fig 13 of the paper on page 40
        ladder (str):  upper or lower ladder in Fig. 13 of page 40 of the paper
        branch (str):  branch string, left or right (see Fig. 13 on page 40 of the paper)
        mace_formulas(List[str]): a list, first item is the string for sos, second item is goals
    """
    fn = os.path.join(out_dir, f"level{level}_{ladder}_{branch}.in")
    with (open(fn, "w")) as fp:
        fp.writelines(comment_lines)
        fp.write(sos_line)
        fp.writelines(basic_str)
        fp.write(f"\n{mace_formulas[0]}\n")
        fp.write(end_line)
        fp.write(goal_line)
        fp.write(f"{mace_formulas[1]}\n")
        fp.write(end_line)


def gen_mace4_files(n1, n2, out_dir):
    """
    """
    for level in range(n1, n2+1):
        upper = gen_mace4_formulas_upper(level)
        write_file(out_dir, level, "upper", "right", upper[1])
        write_file(out_dir, level, "upper", "left", upper[0])

        lower = gen_mace4_formulas_lower(level)
        write_file(out_dir, level, "lower", "right", lower[1])
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        n1 = int(sys.argv[1])
        n2 = int(sys.argv[2])
    else:
        n1 = 2
        n2 = 2
    if n1 < 2 or n2 < 2 or n1 > n2:
        print("Levels must be at least 2, and <from level> must not be greater than <to level>.")
    else:
        if len(sys.argv) > 3:
            out_dir = sys.argv[3]
        else:
            out_dir = "."
        v = gen_mace4_files(n1, n2, out_dir)
    
