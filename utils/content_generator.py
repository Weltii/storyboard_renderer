import os
from datetime import datetime
from layouts.abstract_layout import AbstractLayout, TemplateNotFound
from render_job import RenderJob
from statics import JobErrors, JobSteps, output_directory
from utils.save_files import save_tex_file


def compile_layout(render_job: RenderJob):
	if render_job.error_type is not JobErrors.VALID:
		return None

	content = __generate_content(render_job)
	if content:
		file_name = f"{render_job.storyboard.title}_{datetime.now().timestamp()}.tex"
		__save_file(file_name, content, render_job)


def __generate_content(render_job: RenderJob):
	render_job.step = JobSteps.GENERATE_TEX_DOC

	try:
		layout: AbstractLayout = render_job.layout()
		# generate the file content
		return layout.generate_file(render_job.storyboard)
	except TemplateNotFound:
		render_job.error_type = JobErrors.GENERATE_TEX_ERROR
		render_job.error_data = dict(
			message=f"The template file for the {render_job.layout} is not available."
		)
		return None
	except AttributeError:
		render_job.error_type = JobErrors.GENERATE_TEX_ERROR
		render_job.error_data = dict(
			message=f"The layout {render_job.layout} is no AbstractLayout"
		)
	except TypeError:
		render_job.error_type = JobErrors.GENERATE_TEX_ERROR
		render_job.error_data = dict(
			message=f"{render_job.layout} has the wrong type"
		)


def __save_file(file_name: str, file_content: str, render_job: RenderJob):
	try:
		# save content as tex file
		save_tex_file(file_name, file_content)
		render_job.tex_file_path = os.path.join(output_directory, file_name)
	except FileNotFoundError:
		render_job.error_type = JobErrors.GENERATE_TEX_ERROR
		render_job.error_data = dict(
			message="The file could not be saved."
		)
