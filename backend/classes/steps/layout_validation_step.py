from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.utils.enums import LayoutName, LayoutNameReverse


class LayoutValidationStep(Step):
    @staticmethod
    def run(job: Job):
        if hasattr(LayoutNameReverse, job.layout):
            return hasattr(LayoutName, getattr(LayoutNameReverse, job.layout).value)
        return False
