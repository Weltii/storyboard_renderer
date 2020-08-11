from typing import List, Type

from backend.classes.steps.compile_tex_step import CompileTexStep
from backend.classes.steps.frame_data_validation_step import FrameDataValidationStep
from backend.classes.steps.generate_tex_file_step import GenerateTexFileStep
from backend.classes.steps.layout_validation_step import LayoutValidationStep
from backend.utils.enums import Status, StepType
from backend.classes.render_job import Job
from backend.classes.step import Step


class JobWorker:
    # List of steps
    steps: List[Step] = [
        LayoutValidationStep(),
        FrameDataValidationStep(),
        GenerateTexFileStep(),
        CompileTexStep(),
    ]
    validate_frames_step: List[Step] = {FrameDataValidationStep()}

    @staticmethod
    def run_job(job: Job, steps: List[Step] = None):
        if not steps:
            job.status_data[
                "job_worker_error"
            ] = "The specified list of steps, is empty or None. The default list will used instead!"
            steps = JobWorker.steps
        for step in steps:
            if job.status is Status.VALID:
                step.run(job)

        if job.status is Status.VALID:
            job.step = StepType.FINISHED
