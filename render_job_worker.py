from abc import ABC, abstractmethod
from typing import List

from latex_bridge import compile_latex
from render_job import RenderJob
from statics import JobErrors, JobSteps
from utils.content_generator import compile_layout
from utils.validate_data import validate_data
from utils.validate_layout import validate_layout


class JobWorker:
	steps: List = [
		validate_layout,
		validate_data,
		compile_layout,
		compile_latex
	]

	def run_job(self, job: RenderJob):
		for step in self.steps:
			if job.error_type == JobErrors.VALID:
				step(job)
			else:
				break
		if job.error_type == JobErrors.VALID:
			job.step = JobSteps.FINISH
