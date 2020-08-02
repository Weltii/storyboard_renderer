from abc import ABC, abstractmethod

from backend.utils.enums import StepType
from backend.classes.render_job import Job


class Step(ABC):
    @staticmethod
    @abstractmethod
    def run(job: Job):
        pass
