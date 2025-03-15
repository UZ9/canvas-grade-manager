from canvasapi import Canvas
import os
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn, TimeElapsedColumn, TimeRemainingColumn

class CanvasManager:
    def __init__(self, api_url, api_key, course_id):
        self.canvas = Canvas(api_url, api_key)
        self.course = self.canvas.get_course(course_id)
        self.course_id = course_id

    def download_all_submissions(self, assignment, target_folder):
        submissions = assignment.get_submissions()

        no_submission_users = []

        # first fetch the number of students in the canvas; this unfortunately cannot be done in one request 
        # as canvas limits the API response to 100 items for any request, requiring pagination 
        submission_count = 0

        # we can use the submission count to know the current progress of downloading; this is technically 
        # not needed, but the slight overhead to see the exact progress seems to be woth it
        for submission in submissions:
            submission_count += 1

        with Progress(
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            transient=True
        ) as progress:
            task = progress.add_task("[green] Downloading submissions...", total=submission_count)

            for submission in submissions:
                user = self.course.get_user(submission.user_id)

                name = user.name

                # names are by default First Name Last Name, reverse this order to Last Name First Name
                name = " ".join(name.split(" ")[::-1])

                progress.update(task, description=f"[green] Downloading {name}...")

                # each submission has attachments; download and place in folder
                for attachment in submission.attachments:
                    progress.update(task, advance=1)
                    progress.update(task, description=f"[green] Downloading {attachment} from {name}...")

                    attachment.download(os.path.join(target_folder, f"{name.replace(" ", "").replace("_", "")}_{submission.user_id}_{str(attachment).replace("_", "")}"))


                if len(submission.attachments) == 0:
                    print("No assignments found for", name)
                    no_submission_users.append(name)
                else:
                    print("Downloaded", name)

        print("Students with no submission:")

        for student in no_submission_users:
            print("-", student)

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

                    # TODO: add submission logic here; currently left blank
                    # to not accidentally nuke everyone's grade

                    progress.update(task, description=f"[green] Assigning grade {grade.strip()} to {name.strip()}...")

    def parse_downloaded_name(self, file_name):
        split = file_name.split("_")

        if len(split) != 3:
            return ("", "", "") 

        name = split[0]
        user_id = split[1]
        original_file_name = split[2]

        return (name, user_id, original_file_name)
