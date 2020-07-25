from typing import List

from backend.utils.enums import Status, StepType
from backend.classes.render_job import Job
from backend.classes.step import Step


class JobWorker:
    # List of steps
    steps: List[Step] = [

    ]

    def run_job(self, job: Job, steps: List[Step] = None):
        if not steps:
            steps = self.steps
        for step in steps:
            if job.status is Status.VALID:
                step.run(job)

        if job.status is Status.VALID:
            job.step = StepType.FINISHED
