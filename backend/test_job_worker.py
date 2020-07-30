import os
import unittest
from typing import List

from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.classes.steps.compile_tex_step import CompileTexStep
from backend.classes.steps.frame_data_validation_step import FrameDataValidationStep
from backend.classes.steps.generate_tex_file_step import GenerateTexFileStep
from backend.classes.steps.layout_validation_step import LayoutValidationStep
from backend.classes.storyboard import Storyboard
from backend.config import sample_data_path
from backend.job_worker import JobWorker
from backend.utils.enums import LayoutName, Status, StepType


def generate_storyboard():
    frame = dict(
        image=os.path.join(sample_data_path, "sample_image.jpg"),
        image_description="image description"
    )
    return Storyboard(
        title="test storyboard",
        author="Bernhard Brueckpfeiler",
        frames=[frame, frame, frame]
    )


def generate_job():
    return Job(layout=LayoutName.EASY_LAYOUT.value, storyboard=generate_storyboard())


def remove_files(file_name_without_ending: str):
    endings = [".pdf", ".tex", ".aux", ".log"]
    for ending in endings:
        path = file_name_without_ending + ending
        if os.path.exists(path):
            os.remove(path)


class TestJobWorker(unittest.TestCase):
    def test_job_worker_without_errors(self):
        job = generate_job()
        JobWorker.run_job(job, [
            LayoutValidationStep(),
            FrameDataValidationStep(),
            GenerateTexFileStep(),
            CompileTexStep()
        ])
        self.assertEqual(job.status, Status.VALID)
        self.assertEqual(job.status_data, dict())
        self.assertEqual(job.step, StepType.FINISHED)
        remove_files(job.tex_file_path.replace(".tex", ""))

    def test_job_worker_empty_step_list(self):
        job = generate_job()
        JobWorker.run_job(job)
        self.assertEqual(job.status, Status.VALID)
        self.assertEqual(
            job.status_data["job_worker_error"],
            "The specified list of steps, is empty or None. The default list will used instead!"
        )
        self.assertEqual(job.step, StepType.FINISHED)
        remove_files(job.tex_file_path.replace(".tex", ""))

    def test_job_worker_run_with_error(self):
        job = generate_job()
        job.storyboard.frames[0] = dict(
            image=12,
        )
        JobWorker.run_job(job, [
            LayoutValidationStep(),
            FrameDataValidationStep(),
            GenerateTexFileStep(),
            CompileTexStep()
        ])
        self.assertEqual(job.status, Status.INVALID_DATA)
        self.assertEqual(job.status_data, dict(
            missing_data={
                # the structure with a number as string in the dict is dirty
                # todo Change number as string inside the dict!
                "0": "Frame_0: image_description is missing"
            },
            wrong_data_type={
                # the structure with a number as string in the dict is dirty
                # todo Change number as string inside the dict!
                "0": "Frame_0: image is from type int instead of str"
            },
        ))
        self.assertEqual(job.step, StepType.VALIDATE_DATA)


if __name__ == "__main__":
    unittest.main()
