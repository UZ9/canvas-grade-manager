# canvas-grade-uploader

A utility CLI for automatically uploading grades to Canvas. Primarily used to assist in grading ECE2035: Programming for Hardware/Software Systems.

# Commands 

```
# download all submissions into a particular directory
canvascli download-submissions <assignment ID> <destination-folder>

# download all submissions into a particular directory
canvascli upload-submissions <csv-file>
```

# CSV Format

This parser works off of the following CSV format:

```
name,rubricItem1,rubricItem2,rubricItem3
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
