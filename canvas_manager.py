from canvasapi import Canvas
import os
from rich.progress import Progress, SpinnerColumn, TextColumn

class CanvasManager:
    def __init__(self, api_url, api_key, course_id):
        self.canvas = Canvas(api_url, api_key)
        self.course = self.canvas.get_course(course_id)
        self.course_id = course_id

    def download_all_submissions(self, assignment_id, target_folder):
        assignment = self.course.get_assignment(assignment_id)

        submissions = assignment.get_submissions()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[green] Downloading submissions...")

            for submission in submissions:
                user = self.course.get_user(submission.user_id)

                name = user.name

                progress.update(task, description=f"[green] Downloading {name}...")

                # each submission has attachments; download and place in folder
                for attachment in submission.attachments:
                    progress.update(task, description=f"[green] Downloading {attachment} from {name}...")

                    attachment.download(os.path.join(target_folder, f"{name.replace(" ", "")}_{submission.user_id}_{attachment}"))


                if len(submission.attachments) == 0:
                    print("No assignments found for", name)
                else:
                    print("Downloaded", name)

    def upload_grades(self, assignment_id, grade_csv):
        assignment = self.course.get_assignment(assignment_id)


        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[green] Downloading submissions...")

            with open(grade_csv) as grade_file:
                for line in grade_file:
                    cols = line.split(",")

                    file_name = cols[0]
                    grade = cols[1]

                    (name, user_id, _) = self.parse_downloaded_name(file_name)

                    if len(name) == 0:
                        continue

                    submission = assignment.get_submission(user_id)

                    # TODO: add submission logic here

                    progress.update(task, description=f"[green] Assigning grade {grade.strip()} to {name.strip()}...")

    def parse_downloaded_name(self, file_name):
        split = file_name.split("_")

        if len(split) != 3:
            return ("", "", "") 

        name = split[0]
        user_id = split[1]
        original_file_name = split[2]

        return (name, user_id, original_file_name)

