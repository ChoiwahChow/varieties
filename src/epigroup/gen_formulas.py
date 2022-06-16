#!/usr/bin/env python3
"""
This script is based on special pairs of varieties and subvarieties, as given by semi.xlsx. 
It generates all formulas from the given spreadsheet 
The aim is to find a model in the variety but not in the subvariety.

Excel line starts with 1
First non (1,1) line: 229
Last line: 3649
"""

import os
import sys
from ast import literal_eval as make_tuple
from openpyxl import load_workbook


comment_lines = ['% The aim is to find a model in the epigroup but not in the subepigroup\n',
                 '% sos is the epigroup, and goals represent the subepigroup.\n']

sos_line = "\nformulas(sos).\n"
goal_line = "\nformulas(goals).\n"
end_line = "end_of_list.\n"
basic_str = """(x * y) * z = x * (y * z).
x' = x' * (x * x').
x * x' = x' * x.
"""
    


def write_file(out_dir, n, variety_formula, subvariety_formula):
    """ writes out a mace4 input file. 
    Args:
        out_dir (str): output directory
        n (int):  
    """
    fn = os.path.join(out_dir, f"epigroup_{n}.in")
    with (open(fn, "w")) as fp:
        fp.writelines(comment_lines)
        fp.write(sos_line)
        fp.writelines(basic_str)
        fp.write(f"\n{variety_formula}\n")
        fp.write(end_line)
        fp.write(goal_line)
        fp.write(f"{subvariety_formula}\n")
        fp.write(end_line)


def gen_formula(n):
    """
    Args:
        n (int): 
    """
    f = "(x*x)"
    for x in range(3, n+1):
        f = f"({f}*x)"
    return f"({f}*x)*x' = {f}."
        

def gen_mace4_files(start, end, out_dir):
    """
    Args:
        start (int): starting n
        end (int): ending (inclusive) n
        out_dir (str): output directory
    """
    subvariety = gen_formula(start-1)
    for n in range(start, end+1):
        variety = gen_formula(n)
        write_file(out_dir, n, variety, subvariety)
        subvariety = variety
    

if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    if start < 2 or start > end:
        print("<start must not be greater than end and must be greater than 2>.")
    else:
        if len(sys.argv) > 3:
            out_dir = sys.argv[3]
        else:
            out_dir = "."
        gen_mace4_files(start, end, out_dir)
    
