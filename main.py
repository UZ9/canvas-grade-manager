import click
from dotenv import load_dotenv
import os
from canvas_manager import CanvasManager
from autograder import grade_assignments, save_class_results

load_dotenv()

CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")
CANVAS_API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")

def choice(text):
    print(text, "[Y\\n]")

    choice = input().lower()

    if (choice is not None and choice == "") or choice == "y":
        return True

    return False

@click.group()
def cli():
    pass

@click.command()
@click.argument("submission_folder")
@click.argument("elf_path")
@click.argument("seeds", nargs=-1)
def grade(submission_folder, elf_path, seeds):
    save_class_results(grade_assignments(submission_folder, elf_path, seeds))

@click.command()
@click.argument("course_id")
@click.argument("assignment_id")
@click.argument("destination_folder")
def download(course_id, assignment_id, destination_folder):
    manager = CanvasManager(CANVAS_BASE_URL, CANVAS_API_KEY, course_id)

    course = manager.course

    assignment = course.get_assignment(assignment_id)

    # Confirm course selection 
    if choice(f"Confirm: download all submissions for assignment '{assignment.name}' in course '{course.name}'"):
        manager.download_all_submissions(assignment, destination_folder)
    else:
        print("Cancelled download")

@click.command()
@click.argument("course_id")
@click.argument("assignment_id")
@click.argument("grades_csv_file")
def upload(course_id, assignment_id, grades_csv_file):
    manager = CanvasManager(CANVAS_BASE_URL, CANVAS_API_KEY, course_id)

    course = manager.course

    assignment = course.get_assignment(assignment_id)

    # Confirm course selection 
    if choice(f"Confirm: upload all submissions for assignment '{assignment.name}' in course '{course.name}'"):
        manager.upload_grades(assignment_id, grades_csv_file)
        click.echo("Successfully uploaded all submissions.")
    else:
        print("Cancelled upload")

cli.add_command(download)
cli.add_command(upload)
cli.add_command(grade)

if __name__ == "__main__":
    cli()
