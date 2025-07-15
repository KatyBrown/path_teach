from PyQt5.QtWidgets import QApplication, QFileDialog
import glob
import os
import sys
from datetime import datetime
import pandas as pd
import unidecode
import re
import shutil


def remove_non_ascii(text):
    '''
    Removes non-ascii characters from a string - just used so special
    characters in names don't break it.
    '''
    return ''.join(i for i in text if ord(i) < 128)


def clean_string(string):
    '''
    Remove punctutation etc from a string - used to clean student names -
    for comparison with the table only.
    '''
    string = unidecode.unidecode(string)
    string = re.sub(r'[^\w\s]', "_", string)
    string = remove_non_ascii(string)
    string = string.strip("_")
    string = string.strip().replace(" ", "_").replace("__", "_")
    return (string)


def get_basic_error_dict():
    '''
    Errors which prevent the tool from running - no input, no output,
    repeated IDs.
    '''
    return {
        1: 'Output folder must be specified',
        2: 'Input folder must be specified',
        3: 'Student list must be specified',
        4: 'Non-unique student IDs in student table:'}


def get_folder_error_dict(folder):
    '''
    Errors on the contents of a folder - internal file not found or too many
    files found.
    '''
    return {
        5: f'{folder}\tNot processed - Not a directory',
        6: f'{folder}\tNot processed - No matching files found',
        7: f'{folder}\tNot processed - Too many matching files found',
    }


def get_file_error_dict(vals):
    '''
    Errors affecting individual files - students not found in the student
    list or mismatched IDs.
    '''
    return {
        8: f'{vals[0]}\tNot processed \
- last name {vals[1]} not found in student list',
        9: f"{vals[0]}\tNot processed \
- ID {vals[1]} doesn't match ID {vals[2]} found in student list"
    }


def get_file_warn_dict(filepath, val1, val2):
    '''
    Warning for an individual file - if there is more than one student with
    the same surname.
    '''
    return {
        1: f'{filepath}\t\
Student name {val1} has more than one entry, using {val2}'
    }


def process_error(n, log, vals=None):
    '''
    Generates the error message, logs it and exits or continues as needed.
    Only errors 1-4 will raise an error - otherwise it just continues to the
    next file.
    '''
    if n <= 4:
        # Get the error message dictionary
        errors = get_basic_error_dict()
        # Access the relevant error
        message = errors[n]
        if n <= 3:
            # Adds consitent formatting to the error messages
            long_message = f"ERROR - {message}\tERROR {n}\n"
            # Write to the log file and close it
            if log:
                log.write(f"{long_message}\n")
                log.close()
            # Raise an error and show the error message
            raise RuntimeError(long_message)
        else:
            # List of IDs involved in the error
            ids = ",".join(vals)
            # Adds consitent formatting to the error messages
            long_message = f"ERROR - {message} {ids}\tERROR {n}\n"
            # Write to the log file and close it
            log.write(f"{long_message}\n")
            log.close()
            # Raise an error and show the error message
            raise RuntimeError(long_message)
    elif n >= 5:
        if n == 5 or n == 6 or n == 7:
            # Get the folder error message dictionary
            errors = get_folder_error_dict(vals)
        else:
            # Get the file error message dictionary
            errors = get_file_error_dict(vals)
        # Access the relevant error
        message = errors[n]
        # Format an error message
        long_message = f"{message}\tERROR {n}\n"
        # Show the error and write it to the log file
        print(long_message.strip())
        log.write(long_message)


def process_warn(n, log, val=None):
    '''
    Generates a warning message - the file is still processed but a warning
    is written to the output file.
    '''
    # Get the warning message dictionary
    warns = get_file_warn_dict(val[0], val[1], val[2])
    # Find and format the warning message
    message = warns[n]
    long_message = f"{message}\tWARN {n}\n"
    # Show the warning and write it to the log file
    print(long_message.strip())
    log.write(long_message)


def choose_folder_qt():
    '''
    Opens system dialogues to find the input and output directories and
    the student lookup table.
    '''
    # Initiates the PyQt object needed to use system diaglogues
    app = QApplication(sys.argv)

    # Ask for and store the input folder
    in_folder = QFileDialog.getExistingDirectory(
        None, "Select folder containing student documents")

    # Ask for and store the output folder
    out_folder = QFileDialog.getExistingDirectory(
        None, "Create a different folder for the clean files")

    # Ask for and store the student lookup table
    student_tab = QFileDialog.getOpenFileName(
        None, "Select table of student names and IDs")[0]

    return in_folder, out_folder, student_tab


def get_contents(folder, log):
    files = glob.glob(f"{folder}/*")
    subdirs = []
    for file in files:
        if os.path.isdir(file):
            subdirs.append(file)
        else:
            process_error(5, log, vals=file)
    return (subdirs)


def copy_files(list_subfolds, out_folder, students, log):
    anonD = dict()
    for lastname, ID in zip(students['lastname_clean'],
                            students['Anon']):
        anonD.setdefault(lastname, set())
        anonD[lastname].add(ID)

    for subfold in list_subfolds:
        print(f"Processing folder {subfold}")
        nam = subfold.split("/")[-1]
        pattern = r'^[A-Z](?:\.[A-Z])*\.'
        clean_nam = re.sub(pattern, "", nam)
        lastname = clean_string(clean_nam.split("_")[0])

        contents = os.listdir(subfold)
        x = 0
        file_found = None
        for c in contents:
            if clean_nam in c:
                file_found = c
                x += 1
        if x < 1:
            process_error(6, log, vals=subfold)
            continue
        elif x > 1:
            process_error(7, log, vals=subfold)
            continue
        else:
            id_from_file = file_found.split("_")[-1].split(".")[0]
            y = 0
            if lastname in set(students['lastname_clean']):
                IDs = anonD[lastname]
                if id_from_file in IDs:
                    y += 1
                    if len(IDs) > 1:
                        process_warn(1, log, val=[f"{subfold}/{file_found}",
                                                  lastname,
                                                  id_from_file])
            else:
                process_error(8, log, vals=[f"{subfold}/{file_found}",
                                            lastname, ""])
                continue
            if y == 0:
                IDD = ",".join(IDs)
                process_error(9, log, vals=[f"{subfold}/{file_found}",
                                            id_from_file, IDD])
                continue
            else:
                suffix = file_found.split(".")[-1]
                newname = f"{out_folder}/{id_from_file}.{suffix}"
                shutil.copy(f"{subfold}/{file_found}", newname)


def main():
    in_folder, out_folder, student_tab = choose_folder_qt()
    if not os.path.exists(out_folder):
        process_error(1, log=None)

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H:%M:%S")
    log = open(f"{out_folder}/logfile_{timestamp}.txt", "w")

    if not os.path.exists(in_folder):
        process_error(2, log)
    if not os.path.exists(student_tab):
        process_error(3, log)

    students = pd.read_csv(student_tab, sep="\t").drop_duplicates()
    if len(set(students['Anon'])) != len(students):
        dups = set(students['Anon'][students['Anon'].duplicated()])
        process_error(4, log, vals=dups)
    students['lastname_clean'] = [
        clean_string(x) for x in students['LastName']]
    list_subfolds = get_contents(in_folder, log)
    copy_files(list_subfolds, out_folder, students, log)
    log.close()


if __name__ == "__main__":
    main()
