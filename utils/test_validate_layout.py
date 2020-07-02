import unittest

from layouts.abstract_layout import AbstractLayout
from layouts.movie_layout import MovieLayout
from render_job import RenderJob
from statics import JobErrors
from utils.validate_layout import validate_layout


class LayoutWhichIsNotInTheLayoutList(AbstractLayout):
	def generate_file(self, storyboard: dict):
		pass

	@staticmethod
	def get_required_frame_data() -> dict:
		pass


class TextValidateLayout(unittest.TestCase):
	def test_layout_found(self):
		job = RenderJob(MovieLayout, dict())
		validate_layout(job)
		self.assertEqual(job.error_type, JobErrors.VALID)

	def test_layout_found(self):
		job = RenderJob(LayoutWhichIsNotInTheLayoutList, dict())
		validate_layout(job)
		self.assertEqual(job.error_type, JobErrors.INVALID_LAYOUT)

	def test_layout_found(self):
		job = RenderJob(None, dict())
		validate_layout(job)
		self.assertEqual(job.error_type, JobErrors.INVALID_LAYOUT)


if __name__ == '__main__':
	unittest.main()
