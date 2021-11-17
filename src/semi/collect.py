#!/usr/bin/env python3
"""
This script is based on special pairs of varieties and subvarieties, as given by semi.xlsx.
It looks at the output files to collect data such as the minimum order that
has a model in a variety but not in a subvariety.

First non (1,1) line: 229
Last line: 3642
"""

import os
import sys



def extract_data(file_path):
    order = -1
    error = ""
    with (open(file_path)) as fp:
        line = fp.readline()
        if line.startswith("interpretation("):
            pos = line.find(",")
            order = int(line[16:pos])
        elif line.startswith("Current CPU time: " ):
            pos1 = line.find("(total CPU time: ")
            pos2 = line.rfind(" seconds")
            cpu_time = int(line[pos1, pos2])
        elif line.startswith("For domain size "):
            domain_size = int(line[16:-1])
        elif line.startswith("Exiting with failure."):
            error = "Exiting with failure"
        elif "(max_megs_no)" in line:
            error = "max_megs_no"
        elif "(max_sec_no)" in line:
            error = "max_sec_no"                  

    if error == "":
        return (order, cpu_time, error)
    else:
        return (domain_size, cpu_time, error)


if __name__ == "__main__":
    excel_file = sys.argv[1]
    n1 = int(sys.argv[2])
    n2 = int(sys.argv[3])
    if n1 < 1 or n1 > n2:
        print("<from excel row> must not be greater than <to excel row>.")
    else:
        if len(sys.argv) > 4:
            out_dir = sys.argv[4]
        else:
            out_dir = "."
        v = gen_mace4_files(excel_file, range(n1, n2+1), out_dir)
