#!/usr/bin/env python3
"""
This script is based on special pairs of varieties and subvarieties, as given by semi.xlsx.
It looks at the output files to collect data such as the minimum order that
has a model in a variety but not in a subvariety.

First non (1,1) line: 229
Last line: 3648
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
                error = f"Exiting with failure, last domain size: {domain_size}"
            elif line.startswith("Process ") and "(max_megs_no)" in line:
                error = f"exceeded memory limit, last domain size: {domain_size}"
            elif line.startswith("Process ") and "(max_sec_no)" in line:
                error = f"exceeded time limit, last domain size: {domain_size}"
            elif line.startswith("Process ") and "(max_models)" in line:
                error = f"found a model of order {order}"
            elif line.startswith(f"Fatal error:  palloc"):
                error = f"out of memory, last domain size: {domain_size}"
            elif line.startswith("Killed"):
                error = f"Killed, last domain size: {domain_size}"           
    this_cpu_time = round(cpu_time - last_cpu_time, 2)
    if error.startswith("found a model of order"):
        return (line_no, subvariety, variety, order, this_cpu_time, cpu_time, error)
    else:
        return (line_no, subvariety, variety, domain_size, "", cpu_time, error)


def extract_all_data(out_dir):
    all_results = list()
    for file in os.listdir(out_dir):
        results = extract_data(os.path.join(out_dir, file))
        all_results.append(results)
    all_results.sort(key=lambda x:x[0])
    for item in all_results:
        print(item)
    return all_results
        
        
def compose_csv_file(results, start, end, csv_file_path):
    """
    (3641, (8, 2), (5, 54), 3, 0.0, 0.0, 'max_models')
    """
    res = {item[0]: item[1:] for item in results}
    with (open(csv_file_path, "w")) as fp:
        fp.write('"Subvariety"," => ","Variety","Last order","Time spent on last order (s)","Total time from order 2 (s)","Comment"\n')
        for idx in range(start, end+1):
            r = res.get(idx, None)
            if r is None:
                fp.write('," => ",,,,,\n')
            else:
                fp.write(f'"{r[0]}"," => ","{r[1]}",{r[2]},{r[3]},{r[4]},"{r[5]}"\n')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    else:
        out_dir = "."
    csv_file_path = "sem.csv"
    if len(sys.argv) > 2:
        csv_file_path = sys.argv[2]
    v = extract_all_data(out_dir)
    compose_csv_file(v, 1, 3648, csv_file_path)
