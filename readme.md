#### `scripts/clean_file_names.py`

This script will take a folder containing files with names formatted as e.g.

`B.Ahmed_30192844_assignsubmission_file/B.Ahmed_30192844_assignsubmission_file_7859K.docx`

(examples in the folder example_student_scripts)
and copy them to a new folder, named only with the anonymous ID, e.g.
`7859K.docx`

It requires a table of student names and IDs in a tab delimited file, formatted as follows:

| First Name | Last Name | Anon     |
|------------|-----------|--------|
| Bao        | Ahmed     | 7859K  |
| Carlos     | Zhang     | 7892T  |
| Daria      | Patel     | 7820X  |
| Eshan      | O'Neill   | 7843M  |
| Farida     | Taylor    | 7804Z  |

An example table is in the file example_student_table.tsv

To run the code directly in Python, use the following syntax:
`python scripts/clean_file_names.py`

For this method, the following packages need to be installed:
* `pandas`
* `unidecode`
* `pyqt5`


Alternatively, download `clean_file_names.exe` from [the GitHub release](https://github.com/KatyBrown/path_teach/releases/latest) and double-click on it. This automatically provides the required packages.

A pop-up will ask for the input folder - this is the folder containing the unformatted files.

A second pop-up will ask for the output folder - this is where the reformatted files will be copied and where the log file will be found.

A third pop-up will ask for the student table - this is the tab delimited table described above.

The script will then rename and copy each file, unless it encounters an error. Errors are output to a file named `logfile_xyz.txt` in the output folder, where xyz is the current date and time.

Error codes:
* 1 - Invalid output folder
* 2 - Invalid input folder
* 3 - Invalid student table
* 4 - More than one student name with the same ID
* 5 - Subfolder can't be opened
* 6 - No matching files found in the subfolder
* 7 - Too many matching files found in the subfolder
* 8 - Student last name not found in table
* 9 - Mismatch between ID in file name and ID in student table


#### `scripts/remove_notes.py` 

This script removes the notes panel from Powerpoint presentations in a specified folder and outputs clean copies of the files into a new folder.

All files which need to be processed should be in a single folder and named as `.pptx`.

To run the code directly in Python, use the following syntax:
`python scripts/remove_notes.py`

For this method, the following packages need to be installed:
* `python-pptx`
* `pyqt5`

Alternatively, download `remove_notes.exe` from [the GitHub release](https://github.com/KatyBrown/path_teach/releases/latest) and double-click on it. This automatically provides the required packages.

A pop-up will ask for the input folder - this is the folder containing the unformatted files.

A second pop-up will ask for the output folder - this is where the reformatted files will be copied.

The script will then make a copy of each file in the input folder, with the notes panel removed, in the output folder.