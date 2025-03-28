# canvas-grade-uploader

A utility CLI for automatically uploading grades to Canvas. Primarily used to assist in grading ECE2035: Programming for Hardware/Software Systems.

# Requirements 

- A Canvas account with instructor privileges for a course 
- Python 3

# Installation

The `requirements.txt` file contains a list of all needed dependencies for this project. You can install them automatically using the following command at the base of the repository:

```
pip install -r requirements.txt
```

# Commands 

```
# download all submissions into a particular directory
# files will have the format UserName_UserID_OriginalFileName.OriginalFileExtension
python main.py download <course ID> <assignment ID> <path/to/destination/folder>

# upload all grades to canvascli
python main.py upload <course ID> <assignment ID> <path/to/grades/csv>

# autograde assignments; can be any amount of seeds provided
python main.py grade <path/to/submissions/folder> <path/to/elf/file> <seed-1> <seed-2> <...> <seed-n>
```

# CSV Format

This parser works off of the following CSV format:

```
name,grade,<any extra stats also separated by commas>
```

Where `name` consists of the same format as the download:

```
UserName_UserID_OriginalFileName.OriginalFileExtension
```

Example:

```
BobRoss_192833_SomeFile.asm
```

Upon uploading to Canvas, a comment will be automatically generated under the token user's name with a list of all extra statistics found in the CSV, as shown in the following example:


<p align="center">
  <img src="https://github.com/user-attachments/assets/8efb5583-23b0-4924-9632-f0120e259679" />
</p>




# Setup 

## Course IDs 

`./course_ids.txt` should contain a newline-separated list of Canvas Course IDs to pull assignments from. 

## Environmental Variables

The following need to be set in the `.env` file. A format example is present in `.env.example`:

```sh
CANVAS_BASE_URL = "" # base url for canvas, e.g. https://gatech.instructure.com 

CANVAS_ACCESS_TOKEN = "" # Canvas access token

EMULATOR_PATH="" # Path to riscvemulator executable
```

For acquiring a canvas access token, take a look at https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312
