#!/usr/bin/env python3
"""
Run mace4 on all files (as inputs to Mace4) given in a directory, except for those
that have successfully been run (i.e. models found) previously, as shown in the
output files in a specific output directory. 
"""
import sys
import os
import time
import subprocess
import threading


max_threads = 3
thread_slots = [None] * max_threads
results = dict()


def thread_available(thread_count, thread_slots):
    for x in range(thread_count):
        if thread_slots[x] is None:
            return x
    return None


def all_done(thread_slots):
    for x in range(len(thread_slots)):
        if thread_slots[x] is not None:
            return False
    return True


def wait_for_slot(num_threads, thread_slots, sleep_time):
    busy = True
    while busy:
        x = thread_available(num_threads, thread_slots)
        if x is None:
            time.sleep(sleep_time)
        else:
            return x
            

def run_mace4(slot, key, mace_infile, outfile):
    cp = subprocess.run(f'mace4 -t 3600 -b 20000 -f {mace_infile} > {outfile} 2>&1', capture_output=True, shell=True)
    # results[key] = cp.stdout.read() + "   " + cp.stderr.read()
    thread_slots[slot] = None
    

def already_complete(outfile):
    cp = subprocess.run(f'tail {outfile} | grep "Exiting with 1 model." | wc -l', capture_output=True, shell=True)  
    print(cp.stdout)  
    if cp.stdout.decode("utf-8") == "1\n":
        return True
    else:
        return False
            

def run_process(num_threads, output_dir, inputs_dir, input_files):
    for in_file in input_files:
        components = in_file.split("_")
        outfile = f"{output_dir}/{in_file}.out"
        if already_complete(outfile):
            continue
        slot_id = wait_for_slot(num_threads, thread_slots, 1);
        thread_slots[slot_id] = threading.Thread(target=run_mace4, args=(slot_id, components[0], os.path.join(inputs_dir, in_file), outfile))
        thread_slots[slot_id].start()


if __name__ == "__main__":
    # e.g. .src/semi/run_variety.py inputs outputs
    inputs_dir = sys.argv[1]
    outputs_dir = sys.argv[2]
    run_process(max_threads, outputs_dir, inputs_dir, os.listdir(inputs_dir))
