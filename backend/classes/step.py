from abc import ABC, abstractmethod

from backend.utils.enums import StepType
from backend.classes.render_job import Job


class Step(ABC):
    def __init__(self, step: StepType):
        self.step = step

    @staticmethod
    @abstractmethod
    def run(job: Job):
        pass
