import os
import unittest

from layouts.movie_layout import MovieLayout
from render_job import RenderJob
from statics import JobErrors, output_directory
from utils.content_generator import __generate_content as generate_content, compile_layout, __save_file as save_file


def generate_storyboard():
	return dict(
		title="ExampleTitle",
		author="Bernhard Brückenpfeiler",
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


class TestContentGenerator(unittest.TestCase):
	def test_invalid_render_job(self):
		error_data_message = "Data is invalid"
		render_job = RenderJob(MovieLayout, None)
		render_job.error_type = JobErrors.INVALID_DATA
		render_job.error_data = dict(
			message=error_data_message
		)
		compile_layout(render_job)
		self.assertEqual(render_job.error_data["message"], error_data_message)

	def test_generate_content_valid(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		content = generate_content(render_job)
		self.assertNotEqual(content, None)
		self.assertEqual(render_job.error_type, JobErrors.VALID)

	@unittest.skip("No simple way found to manipulate the path -.-")
	def test_generate_content_template_not_found(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		error_message = f"The template file for the {render_job.layout} is not available."
		# manipulate the template path
		print(render_job.layout.template_file_path)
		render_job.layout.template_file_path = ""
		print(render_job.layout.template_file_path)
		generate_content(render_job)
		self.assertEqual(render_job.error_type, JobErrors.GENERATE_TEX_ERROR)
		self.assertEqual(render_job.error_data["message"], error_message)

	def test_generate_content_layout_attribute_error(self):
		render_job = RenderJob(str, generate_storyboard())
		error_message = f"The layout {str} is no AbstractLayout"
		generate_content(render_job)
		self.assertEqual(render_job.error_type, JobErrors.GENERATE_TEX_ERROR)
		self.assertEqual(render_job.error_data["message"], error_message)

	def test_generate_content_layout_type_error(self):
		render_job = RenderJob(type, generate_storyboard())
		error_message = f"{type} has the wrong type"
		generate_content(render_job)
		self.assertEqual(render_job.error_type, JobErrors.GENERATE_TEX_ERROR)
		self.assertEqual(render_job.error_data["message"], error_message)

	def test_save_file_valid(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		file_name = "test_file.tex"
		content = "testing the file content"
		file_path = os.path.join(output_directory, file_name)
		save_file(file_name, content, render_job)
		self.assertTrue(os.path.exists(file_path))
		self.assertEqual(render_job.tex_file_path, file_path)
		os.remove(file_path)

	@unittest.skip("No simple way found to manipulate the path -.-")
	def test_save_file_file_not_found_error(self):
		render_job = RenderJob(MovieLayout, generate_storyboard())
		file_name = "test_file.tex"
		content = "testing the file content"
		error_message = "The file could not be saved."
		output_directory = ""
		save_file(file_name, content, render_job)
		self.assertEqual(render_job.error_type, JobErrors.GENERATE_TEX_ERROR)
		self.assertEqual(render_job.error_data["message"], error_message)


if __name__ == '__main__':
	unittest.main()
