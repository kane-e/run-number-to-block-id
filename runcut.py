import sys
import os
import csv
import io

COLOR_RED   = "\033[1;31m"
COLOR_BLUE  = "\033[1;34m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_run_num():
    filepath = sys.argv[1]
    if len(sys.argv) < 2:
        print(COLOR_RED + "No filename provided!" + COLOR_RESET)
        exit()
    if not os.path.isfile(filepath):
        print(COLOR_RED + "File does not exist!" + COLOR_RESET)
    blockid_map = make_blockid_map(filepath)
    if not os.path.basename(filepath) == 'runcut.txt':
        print(COLOR_RED + "Incorrect file input! Please input runcut.txt" + COLOR_RESET)
        exit()
    make_new_file(filepath, blockid_map)

def make_blockid_map(filepath):
    block_id_map = {}
    with open(filepath, "rb") as runcut_file_raw:
        runcut_txt = io.TextIOWrapper(runcut_file_raw)
        runcut_csv = csv.DictReader(runcut_txt)
        for row in runcut_csv:
            if "block_id" not in row or not row["block_id"]:
                print(COLOR_BLUE + "no block_id values are present and therefore the operation cannot be performed" + COLOR_RESET)
            block_id_map[row['run_number']] = row['block_id']
    return(block_id_map)

def make_new_file(filepath, blockid_map, field_names=["run_number"]):
    with open(filepath, "rb") as file_raw:
        runcut_txt = io.TextIOWrapper(file_raw)
        csvfile = csv.DictReader(runcut_txt)
        file_name = 'runcut2.txt'
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again. Skipping..." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csvfile.fieldnames)
        new_csv_writer.writeheader()
        for row in csvfile:
            row_copy = row.copy()
            for field_name in field_names:
                print(row[field_name])
                if row[field_name] not in blockid_map:
                    print(COLOR_BLUE + "Invalid field name " + field_name + " for file " + file_name + ", skipping this file" + COLOR_RESET)
                    return
                found_block_id = row_copy[field_name]
                row_copy[field_name] = blockid_map[found_block_id] if found_block_id in blockid_map else found_block_id
            new_csv_writer.writerow(row_copy)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with run_number set to block_id" + COLOR_RESET)

if __name__ == "__main__":
    convert_run_num()