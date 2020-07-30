import os
import subprocess

from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.config import output_path, latex_compiler
from backend.utils.enums import Status


class CompileTexStep(Step):
    @staticmethod
    def run(job: Job):
        if job.status is not Status.VALID:
            return
        # job.step = Step.COMPILE_PDF
        if not os.path.exists(job.tex_file_path):
            job.status = Status.COMPILE_PDF_ERROR
            job.status_data = dict(
                message=f"The .tex file: {job.tex_file_path} cannot found!"
            )
            return

        base_file_path = f"{job.tex_file_path.replace('.tex', '')}"
        log_file_path = base_file_path + ".log"
        pdf_file_path = base_file_path + ".pdf"
        cmd = [
            f"{latex_compiler}",
            f"-output-directory={output_path}",
            "-interaction=nonstopmode",
            f"{job.tex_file_path}",
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE)

        if os.path.exists(pdf_file_path):
            job.pdf_file_path = pdf_file_path
        else:
            job.status = Status.COMPILE_PDF_ERROR
            with open(log_file_path, "r") as log_file:
                log_file_content = log_file.read()
            job.status_data = dict(
                message=f"The .pdf file cannot compiled with the tex file.",
                log_file=log_file_content,
            )
