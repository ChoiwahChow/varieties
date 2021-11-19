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
    file_base_name = os.path.basename(file_path)
    names = file_base_name.split("_")
    line_no = int(names[0])
    subvariety = (int(names[1]), int(names[2]))
    variety = (int(names[4]), int(names[5].split(".")[0]))
    last_cpu_time = 0
    cpu_time = 0
    this_cpu_time = 0
    with (open(file_path)) as fp:
        for line in fp.readlines():
            if line.startswith("interpretation("):
                pos = line.find(",")
                order = int(line[16:pos])
            elif line.startswith("Current CPU time: " ):
                pos1 = line.find("(total CPU time: ")
                pos2 = line.rfind(" seconds")
                last_cpu_time = cpu_time
                cpu_time = float(line[pos1+16:pos2])
            elif line.startswith("For domain size "):
                domain_size = int(line[16:-2])
            elif line.startswith("Exiting with failure."):
                error = "Exiting with failure"
            elif line.startswith("Process ") and "(max_megs_no)" in line:
                error = "max_megs_no"
            elif line.startswith("Process ") and "(max_sec_no)" in line:
                error = "max_sec_no"
            elif line.startswith("Process ") and "(max_models)" in line:
                error = "max_models"
            elif line.startswith("Fatal error:  palloc,"):
                error = "out of memory"          
    if error == "max_models":
        this_cpu_time = round(cpu_time - last_cpu_time, 2)
    if error == "":
        return (line_no, subvariety, variety, order, this_cpu_time, cpu_time, error)
    else:
        return (line_no, subvariety, variety, domain_size, this_cpu_time, cpu_time, error)


def extract_all_data(out_dir):
    all_results = list()
    for file in os.listdir(out_dir):
        results = extract_data(os.path.join(out_dir, file))
        all_results.append(results)
    all_results.sort(key=lambda x:x[0])
    for item in all_results:
        print(item)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    else:
        out_dir = "."
    v = extract_all_data(out_dir)
