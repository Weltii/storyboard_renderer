import os
import unittest

from backend.classes.render_job import Job
from backend.classes.steps.compile_tex_step import CompileTexStep
from backend.classes.steps.generate_tex_file_step import GenerateTexFileStep
from backend.classes.storyboard import Storyboard
from backend.config import output_path, sample_data_path
from backend.utils.enums import Status, LayoutName
from backend.utils.utils import write_file

sample_image_path = os.path.join(sample_data_path, "sample_image.jpg")


def generate_storyboard():
    return Storyboard(
        title="ExampleTitle",
        author="Bernhard Brueckenpfeiler",
        frames=[dict(image=sample_image_path, image_description="Image description")],
    )


def remove_files(file_name_without_ending: str):
    endings = [".pdf", ".tex", ".aux", ".log"]
    for ending in endings:
        path = file_name_without_ending + ending
        if os.path.exists(path):
            os.remove(path)


def generate_example_tex_file(job: Job):
    GenerateTexFileStep.run(job)


class TestLatexBridge(unittest.TestCase):
    def test_compile_pdf_valid(self):
        job = Job(layout=LayoutName.EASY_LAYOUT.value, storyboard=generate_storyboard())
        generate_example_tex_file(job)
        CompileTexStep.run(job)
        self.assertEqual(job.status, Status.VALID)
        self.assertIsNotNone(job.pdf_file_path)
        self.assertTrue(os.path.exists(job.pdf_file_path))
        remove_files(job.tex_file_path.replace(".tex", ""))

    def test_compile_pdf_tex_file_not_found(self):
        job = Job(layout=LayoutName.EASY_LAYOUT.value, storyboard=generate_storyboard())
        job.tex_file_path = "/no/valid/tex/file.tex"
        error_message = f"The .tex file: {job.tex_file_path} cannot found!"
        CompileTexStep.run(job)
        self.assertEqual(job.status, Status.COMPILE_PDF_ERROR)
        self.assertEqual(job.status_data["message"], error_message)
        remove_files(job.tex_file_path.replace(".tex", ""))

    def test_compile_pdf_cannot_compile(self):
        job = Job(layout=LayoutName.EASY_LAYOUT.value, storyboard=generate_storyboard())
        error_message = f"The .pdf file cannot compiled with the tex file."
        base_file_name = "tex_file_not_found"
        base_file_path = os.path.join(output_path, base_file_name)
        job.tex_file_path = base_file_path + ".tex"

        write_file(job.tex_file_path, "nothing is in here!")

        CompileTexStep.run(job)
        self.assertEqual(job.status, Status.COMPILE_PDF_ERROR)
        self.assertEqual(job.status_data["message"], error_message)
        self.assertIsNotNone(job.status_data["log_file"])
        remove_files(base_file_path)


if __name__ == "__main__":
    unittest.main()
