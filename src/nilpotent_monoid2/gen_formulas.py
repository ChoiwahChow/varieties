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
                 '% There are 2 sequences, left and right, in the "ladder-shaped" diagram.\n',
                 '% Level 1 is the bottom row, top level also has only one node N1_2, \n',
                 '% next level has one node, but all other levels have 2 nodes\n',
                 '% Each line represent an implication from lower level to higher level, or from left to right.\n',
                 '% The top (or right) end of the branch (line) is a variety, and the bottom (or left) end of the branch is a subvariety,\n',
                 '% The aim is to find a model in the variety but not in the subvariety\n',
                 '% sos is the variety, and goals represent the subvariety.\n']
sos_line = "\nformulas(sos).\n"
goal_line = "\nformulas(goals).\n"
end_line = "end_of_list.\n"
basic_str = ['(x * y) * z = x * (y * z).\n',  '(x * x) * x = x * x.\n', 'x * y = y * x.\n']


def make_clause_left(level):
    """ Construct strings that Mace4 understands: e.g. (x1 * x2) * x3 for the left sequence of a particular level
    Args:
        level: the level for which the left clauses (2 of them, left and right) are to be generated
    Returns:
        (List[str]): a list of 2 strings representing the 2 clauses, e.g ["x1 * x2", "y1 * y2"]
    """
    left_clause = "x1 * x2"
    right_clause = "y1 * y2"
    for w in range(3, level+1):  # note: we skip level 1 for the left branch
        left_clause = f"({left_clause}) * x{w+1}"
        right_clause = f"({right_clause}) * y{w+1}"
    return [left_clause, right_clause]


def make_clause_right(level):
    """ Construct strings that Mace4 understands: e.g. (x1 * x2) * x3 for the right sequence of a particular level
    Args:
        level: the level for which the clauses for the right sequence are to be generated
    Returns:
        (List[str]): a list of 2 strings representing the 2 clauses,  e.g ["(x1 * x1) * x2", "x1 * x2"]. 
    """
    left_clause = "x1 * x1"
    right_clause = "x1"
    for w in range(2, level+1):
        left_clause = f"({left_clause}) * x{w}"
        right_clause = f"({right_clause}) * x{w}"
    return [left_clause, right_clause]


def gen_mace4_formulas_left(level):
    """ generate mace4 formula for left sequence in Fig. 13 on page 40 of the paper
    Args:
        level: the level for which the Mace4 formulas are to be generated for the left sequence
    Returns:
        (List[List[str]]): a list of 2 items. The first is empty, the second is the formulas for the left branch
        e.g. [[], ['(x1 * x2) * x3 = (y1 * y2) * y3', 'x1 * x2 = y1 * y2']]
    """
    lower = make_clause_left(level)
    lower_sub = make_clause_left(level - 1)
    return [[], [f"{lower[0]} = {lower[1]}.", f"{lower_sub[0]} = {lower_sub[1]}." ]]


def gen_mace4_formulas_right(level):
    """ generate mace4 formula for lower ladder in Fig. 13 on page 40 of the paper
    Args:
        level: the level for which the Mace4 formulas are to be generated for the lower ladder
    Returns:
        (List[List[str]]): a list of 2 items. The first is the formulas for the left branch,
        the second is the formulas for the right branch
        e.g. [['(x1 * x1) * x2 = x1 * x2', 'x1 * x2 = y1 * y2'], ['(x1 * x1) * x2 = x1 * x2', 'x1 * x1 = x1']]
        For each branch, the first item has the formulas for the variety, and the second, the subvariety
    """
    upper = make_clause_right(level)
    upper_sub = make_clause_right(level - 1)
    left_sub = make_clause_left(level - 1)
    return [[f"{upper[0]} = {upper[1]}.", f"{left_sub[0]} = {left_sub[1]}." ],
            [f"{upper[0]} = {upper[1]}.", f"{upper_sub[0]} = {upper_sub[1]}." ]]


def write_file(out_dir, level, mace_formulas):
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
    fn = os.path.join(out_dir, f"level{level}.in")
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
    """ Generate all Mace4 input files from level n1 (level starts with 1) to n2 for both left sequence and right sequence
        in Figure 13, page 40 of the paper.  But left sequence is only generated for level 3 and above
        Left sequence L1 (0), L2 (x1x2 = y1y2), L3 (x1x2x3 = y1y2y3, ...
        Right sequence R1 (x1^2 = x1), R2 (x1^2x2 = x1x2), ...
    """
    for level in range(n1, n2+1):
        right = gen_mace4_formulas_right(level)
        write_file(out_dir, f"R{level-1}_implies_R{level}", right[1])
        write_file(out_dir, f"L{level}_implies_R{level}", right[0])

    n1 = max(n1, 3)
    for level in range(n1, n2+1):
        left = gen_mace4_formulas_left(level)
        write_file(out_dir, f"L{level-1}_implies_L{level}", left[1])
    

if __name__ == "__main__":
    if len(sys.argv) > 2:
        n1 = int(sys.argv[1])
        n2 = int(sys.argv[2])
    else:
        n1 = 3
        n2 = 4
    if n1 < 2 or n1 > n2:
        print("Levels must be at least 2, and starting level must not be greater than ending level.")
    else:
        if len(sys.argv) > 3:
            out_dir = sys.argv[3]
        else:
            out_dir = "."
        v = gen_mace4_files(n1, n2, out_dir)
    
