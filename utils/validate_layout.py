from render_job import RenderJob
from statics import Layouts, JobErrors


def validate_layout(job: RenderJob):
	if job.layout is None:
		job.error_type = JobErrors.INVALID_LAYOUT
		job.error_data = f"Layout is empty!"
	elif job.layout not in Layouts:
		job.error_type = JobErrors.INVALID_LAYOUT
		job.error_data = f"Layout {job.layout.__name__} not found!"