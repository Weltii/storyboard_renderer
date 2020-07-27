from datetime import datetime

from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.layouts.Layouts import Layouts
from backend.layouts.abstract_layout import AbstractLayout
from backend.utils.enums import Status
from backend.utils.utils import save_tex_file, CustomFileExistsError


class GenerateTexFileStep(Step):
    @staticmethod
    def get_file_name(title: str):
        return f"{title}_{datetime.now().timestamp()}.tex".replace(" ", "_")

    @staticmethod
    def run(job: Job):
        layout: AbstractLayout = getattr(Layouts, job.layout, False).value
        file_string = layout.generate_file_string(job.storyboard)
        try:
            save_path = save_tex_file(
                GenerateTexFileStep.get_file_name(job.storyboard.title), file_string
            )
            job.tex_file_path = save_path
        except CustomFileExistsError as exception:
            job.status = Status.GENERATE_TEX_ERROR
            job.status_data[
                "message"
            ] = f"Cannot save the .tex file, path {exception.path} already exists"
