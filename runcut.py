import sys
import os
import csv
import io

COLOR_RED   = "\033[1;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_RESET = "\033[0;0m"

def convert_run_num():
    if len(sys.argv) < 2:
        print(COLOR_RED + "No file provided!" + COLOR_RESET)
        exit()
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(COLOR_RED + "Input is not a file! Please input runcut.txt." + COLOR_RESET)
        exit()
    if not os.path.basename(filepath) == "runcut.txt":
        print(COLOR_RED + "Incorrect file input! Please input runcut.txt." + COLOR_RESET)
        exit()
    make_new_file(filepath)        
    
def make_new_file(filepath):
    with open(filepath, "rb") as file_raw:
        runcut_txt = io.TextIOWrapper(file_raw)
        csv_file = csv.DictReader(runcut_txt)
        csv_list = list(csv_file)
        for row in csv_list:
            if "block_id" not in row or not row["block_id"]:
                print(COLOR_RED + "Missing block_id values. The operation cannot be performed." + COLOR_RESET)
                return
        file_name = "runcut_syncro.txt"
        if os.path.exists(file_name):
            print(COLOR_RED + "File with name " + file_name + " already exists in directory; cannot create a new one. Move this file and try again." + COLOR_RESET)
            return
        new_file = open(file_name, "w")
        new_csv_writer = csv.DictWriter(new_file, fieldnames=csv_file.fieldnames)
        new_csv_writer.writeheader()
        for row in csv_list:
            row["run_number"] = row["block_id"]
            new_csv_writer.writerow(row)
        new_file.close()
        print(COLOR_GREEN + "Exported " + file_name + " with run_number set to block_id." + COLOR_RESET)

if __name__ == "__main__":
    convert_run_num()