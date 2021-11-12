#!/usr/bin/env python3
"""
This script is based on https://arxiv.org/pdf/1911.05817.pdf.
It generates all formulas from 4 up to level n for the lattice of bands.
Level 0 is bottom of Figure 1 on p.5. 
"""

import os
import sys
from var_gen import gen_varieties


sos_line = "\nformulas(sos).\n"
goal_line = "\nformulas(goals).\n"
end_line = "end_of_list.\n"
basic_str = ['(x * y) * z = x * (y * z).\n',  'x * x = x.\n']


def debug_print(v):
    for level, x in enumerate(v):
        print(f"level {level+3}:")
        print(x)


def gen_formula_even_level(n, vs):
    G = vs[0]
    
    ls = n//4 + 2
    if n//4 == (n+2)//4:   # lower of the 2
        pos1 = 2
        pos2 = 1
        us = ls
    else:
        pos1 = 1
        pos2 = 2
        us = ls + 1
    left = [list(reversed(G[us-2])) + G[ls-2], list(reversed(vs[pos1][us-2])) + vs[pos2][ls-2]]
    right = [list(reversed(G[ls-2])) + G[us-2], list(reversed(vs[pos2][ls-2])) + vs[pos1][us-2]]
    
    return [left, right]

   
def gen_formula_odd_level(n, vs):
    G, _, I = vs    # G, H, I as in the paper
    if n == 3:
        return [[G[2-2], I[2-2]], [[1, 2, 3, 1], [1, 3, 2, 1]], [list(reversed(G[2-2])), list(reversed(I[2-2]))]]
    
    ls = n // 4 + 2
    if (n+2)//4 == n//4:  # lower of the 2
        lpos = 1
        mpos = 2
        ms = ls
    else:
        lpos = 2
        mpos = 1
        ms = ls + 1
    left = [G[ls-2], vs[lpos][ls-2]]
    middle = [list(reversed(G[ms-2])) + G[ms-2], list(reversed(vs[mpos][ms-2])) + vs[mpos][ms-2]]
    right = [list(reversed(left[0])), list(reversed(left[1]))]
    return [left, middle, right]
    

def gen_formulas_level(n):
    vs = gen_varieties(n//4 + 4)
    if n % 2 == 0:
        formulas = gen_formula_even_level(n, vs)
    else:
        formulas = gen_formula_odd_level(n, vs)
    return formulas


def make_clause(clause_list):
    """ Construct strings that Mace4 understands: e.g. ((X3 * x1) * x2) from [2, 1, 2]
    Args:
        clause_list (list[int]): list of subscripts for clauses.
    Returns:
        (str): a string represents the clause
    """
    clause = f"x{clause_list[0]}"
    for y in range(1, len(clause_list)):
        if clause_list[y-1] == clause_list[y]:   # assume associativity and x^2 = x
            continue
        clause = f"({clause} * x{clause_list[y]})"
    return clause


def gen_formulas(n):
    return [gen_formulas_level(x) for x in range(3, n+1)]


def gen_mace4_formulas(n):
    formulas = gen_formulas(n)
    return [[f"{make_clause(item[0])} = {make_clause(item[1])}." for item in level] for level in formulas]


def write_file(out_dir, branch, mace4_formulas, level, top, bottom):
    """ writes out a mace4 input file. "bottom" level implies "top" level, so the "goal"
        is the "bottom" level clause so to find a model in the "bigger" algebra but not in
        the smaller algebra.
    Args:
        out_dir (str): output directory
        branch (int):  branch number, 1 to 4 (from left to right in Fig 1 of the paper)
        mace4_formulas (list): boiler-plate mace4 formulas
        level (int):   level in Fig 1 of the paper
        top (int):     index into top algebra clause
        bottom (int):  index into bottom algebra clause
    """
    fn = os.path.join(out_dir, f"level{level}_{branch}.in")
    with (open(fn, "w")) as fp:
        fp.write(sos_line)
        fp.writelines(basic_str)
        fp.write(f"\n{mace4_formulas[level-3][top]}\n")
        fp.write(end_line)
        fp.write(goal_line)
        fp.write(f"{mace4_formulas[level-1-3][bottom]}\n")
        fp.write(end_line)


def gen_mace4_files(n, out_dir):
    mace4_formulas = gen_mace4_formulas(n)
    debug_print(mace4_formulas)
    for level in range(4, n+1):
        write_file(out_dir, 1, mace4_formulas, level, 0, 0)
        if n % 2 == 0:
            write_file(out_dir, 2, mace4_formulas, level, 0, 1)
        else:
            write_file(out_dir, 2, mace4_formulas, level, 1, 0)
        write_file(out_dir, 3, mace4_formulas, level, 1, 1)
        write_file(out_dir, 4, mace4_formulas, level, -1, -1)
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 4
    if len(sys.argv) > 2:
        out_dir = sys.argv[2]
    else:
        out_dir = "."
    v = gen_mace4_files(n, out_dir)
    
