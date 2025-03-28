# Credit: Diego Fratta for original autograder script
# Modifications: Moving to CLI, ENV-based arguments, logging additions, new file format parsing

import subprocess
import os
import re
import sys
import csv
import json
from dotenv import load_dotenv

load_dotenv()

EMULATOR_COMMAND = "runBatch"
EMULATOR_PATH = os.getenv("EMULATOR_PATH")

def run_grader(filename, elf, seed):
    print([EMULATOR_PATH, EMULATOR_COMMAND, filename, elf, str(seed)])
    return subprocess.run([EMULATOR_PATH, EMULATOR_COMMAND, filename, elf, str(seed)], text=True, capture_output=True)

def grade_assignments(submission_folder, elf_file, seeds):
    class_results = [] 

    for filename in os.listdir(submission_folder):
        file_path = os.path.join(submission_folder, filename)

        if not filename.endswith(".asm"):
            print(f"Skipping {filename}")
            continue 

        if not os.path.isfile(file_path):
            continue

        # format of file:
        # Name_CanvasUserID_OriginalFileName.<extension
        (name, canvas_id, original_file_name) = filename.split("_")

        passed = 0
        had_errors = False

        di = 0
        si = 0
        regs = 0
        mem = 0

        for seed in seeds:
            try: 
                result = run_grader(file_path, elf_file, seed)
            except Exception as e:
                print(f"[ERROR] Encountered the following exception when parsing {file_path}: {e}")

                sys.exit()

            try:
                result_json = json.loads(result.stdout)
            except Exception as e:
                print(f"[ERROR] Encountered the following exception when parsing JSON {result.stdout}: {e}")

            result_json = result_json["body"]

            # if the STDOUT contains "passed" the the test case passed
            if '"passed":true' in result.stdout:
                passed += 1
                di += int(result_json["di"])
                si += int(result_json["si"])
                regs += int(result_json["regs"])
                mem += int(result_json["mem"])

            # if the value after "numErrors" is not 0, set an another variable true
            # typical STDOUT would be "numErrors: 0"
            if '"numErrors":0' not in result.stdout:
                hadErrors = True
        
        if(had_errors):
            print(f"{name} passed {passed}/{seeds.__len__()} test cases with errors")
        else:
            print(f"{name} passed {passed}/{seeds.__len__()} test cases")

        if passed != 0:
            di /= passed 
            si /= passed 
            regs /= passed 
            mem /= passed

        class_results.append((filename, (passed/seeds.__len__())*100, di, si, regs, mem, had_errors))

        # TODO: Currently batchRun only returns a single "passed" boolean if ALL seeds pass. This should 
        # be replaced in the emulator with an integeger [0, n], where n is the number of seeds passed.
        # until  then, we have one last autograder run for getting average stats

    return class_results

def save_class_results(results):
    with open("grades.csv", "w") as f:
        csv_writer = csv.writer(f)

        # write names for grader to understand 
        f.write("Student Name, Grade,Dynamic Instructions,Static Instructions,Registers Used,Memory Used,Has Errors\n")

        for data in results:
            csv_writer.writerow(data)

    print(f"Successfuly saved {len(results)} grade results to grades.csv")
