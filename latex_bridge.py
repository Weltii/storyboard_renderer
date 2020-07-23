import os
import subprocess

from render_job import RenderJob
from statics import output_directory, JobErrors, JobSteps


def compile_latex(render_job: RenderJob):
	if render_job.error_type is not JobErrors.VALID:
		return
	render_job.step = JobSteps.COMPILE_PDF
	if not os.path.exists(render_job.tex_file_path):
		render_job.error_type = JobErrors.COMPILE_PDF_ERROR
		render_job.error_data = dict(
			message=f"The .tex file: {render_job.tex_file_path} cannot found!"
		)
		return

	base_file_path = f"{render_job.tex_file_path.replace('.tex', '')}"
	log_file_path = base_file_path + ".log"
	pdf_file_path = base_file_path + ".pdf"
	cmd = [f"lualatex", f"-output-directory={output_directory}", "-interaction=nonstopmode",
				 f"{render_job.tex_file_path}"]
	subprocess.run(cmd, stdout=subprocess.PIPE)

	if os.path.exists(pdf_file_path):
		render_job.pdf = pdf_file_path
	else:
		render_job.error_type = JobErrors.COMPILE_PDF_ERROR
		with open(log_file_path, 'r') as log_file:
			log_file_content = log_file.read()
		render_job.error_data = dict(
			message=f"The .pdf file cannot compiled with the tex file.",
			log_file=log_file_content
		)
