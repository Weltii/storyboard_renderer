import os
import unittest

from latex_bridge import compile_latex
from layouts.movie_layout import MovieLayout
from render_job import RenderJob
from statics import JobErrors, output_directory
from utils.content_generator import compile_layout


def generate_storyboard():
	return dict(
		title="ExampleTitle",
		author="Bernhard Brueckenpfeiler",
		frames=[
			dict(
				scene="001",
				setting="001",
				section="001",
				timecode="00:00:00:01",
				image="None",
				image_description="Image description",
				audio_description="Audio description",
				setting_size="near",
				perspective="normal",
				focal_length=85,
				camera_movement="static",
				camera_support="Tripod",
				fx="-"
			)
		]
	)


def remove_files(file_name_without_ending: str):
	endings = [".pdf", ".tex", ".aux", ".log"]
	for ending in endings:
		path = file_name_without_ending + ending
		if os.path.exists(path):
			os.remove(path)


class TestLatexBridge(unittest.TestCase):
	def test_compile_pdf_valid(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		compile_layout(render_job)
		compile_latex(render_job)

		self.assertEqual(render_job.error_type, JobErrors.VALID)
		self.assertIsNotNone(render_job.pdf)
		self.assertTrue(os.path.exists(render_job.pdf))
		remove_files(render_job.tex_file_path.replace(".tex", ""))

	def test_compile_pdf_tex_file_not_found(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		render_job.tex_file_path = "/not/file/exists"
		error_message = f"The .tex file: {render_job.tex_file_path} cannot found!"
		compile_latex(render_job)
		self.assertEqual(render_job.error_type, JobErrors.COMPILE_PDF_ERROR)
		self.assertEqual(render_job.error_data["message"], error_message)
		remove_files(render_job.tex_file_path.replace(".tex", ""))

	def test_compile_pdf_cannot_compile(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		error_message = f"The .pdf file cannot compiled with the tex file."
		base_file_name = "tex_file_not_found"
		base_file_path = os.path.join(output_directory, base_file_name)
		render_job.tex_file_path = base_file_path + ".tex"

		with open(render_job.tex_file_path, "w") as tex_file:
			tex_file.write("nothing is in here!")

		compile_latex(render_job)
		self.assertEqual(render_job.error_type, JobErrors.COMPILE_PDF_ERROR)
		self.assertEqual(render_job.error_data["message"], error_message)
		self.assertIsNotNone(render_job.error_data["log_file"])
		remove_files(base_file_path)


if __name__ == '__main__':
	unittest.main()
