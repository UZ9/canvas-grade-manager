import click
from dotenv import load_dotenv
import os
from canvas_manager import CanvasManager

load_dotenv()

CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")
CANVAS_API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")

@click.group()
def cli():
    pass

@click.command()
@click.argument("course_id")
@click.argument("assignment_id")
@click.argument("destination_folder")
def download(course_id, assignment_id, destination_folder):
    manager = CanvasManager(CANVAS_BASE_URL, CANVAS_API_KEY, course_id)

    manager.download_all_submissions(assignment_id, destination_folder)
    
    click.echo("Successfully downloaded all submissions.")

@click.command()
@click.argument("course_id")
@click.argument("assignment_id")
@click.argument("grades_csv_file")
def upload(course_id, assignment_id, grades_csv_file):
    manager = CanvasManager(CANVAS_BASE_URL, CANVAS_API_KEY, course_id)

    manager.upload_grades(assignment_id, grades_csv_file)
    
    click.echo("Successfully uploaded all submissions.")

cli.add_command(download)
cli.add_command(upload)

if __name__ == "__main__":
    cli()
