# canvas-grade-uploader

A utility CLI for automatically uploading grades to Canvas. Primarily used to assist in grading ECE2035: Programming for Hardware/Software Systems.

# Commands 

```
# download all submissions into a particular directory
# files will have the format UserName_UserID_OriginalFileName.OriginalFileExtension
canvascli download <course ID> <assignment ID> <path/to/destination/folder>

# upload all grades to canvascli
canvascli upload-submissions <course ID> <assignment ID> <path/to/grades/csv>
```

# CSV Format

This parser works off of the following CSV format:

```
name,grade
```

Where `name` consists of the same format as the download:

```
UserName_UserID_OriginalFileName.OriginalFileExtension
```

Example:

```
BobRoss_192833_SomeFile.asm
```

# Setup 

## Course IDs 

`./course_ids.txt` should contain a newline-separated list of Canvas Course IDs to pull assignments from. 

## Environmental Variables

The following need to be set in the `.env` file. A format example is present in `.env.example`:

```sh
CANVAS_BASE_URL = "" # base url for canvas, e.g. https://gatech.instructure.com 

CANVAS_ACCESS_TOKEN = "" # Canvas access token
```

For acquiring a canvas access token, take a look at https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312
