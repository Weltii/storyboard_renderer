import unittest

from layouts.abstract_layout import AbstractLayout
from layouts.movie_layout import MovieLayout
from render_job import RenderJob
from render_job_worker import JobWorker
from statics import JobErrors


def get_frames(valid_frames: int = 1, missing_data_frames: int = 0, invalid_type_frame: int = 0):
	correct_frame = dict(
		data_1="data_1",
		data_2=41,
		data_3="data_3"
	)
	missing_data = dict(
		data_1="data_1"
	)
	invalid_type = dict(
		data_1=123,
		data_2="data_2",
		data_3="data_3"
	)

	frames = []
	for c in range(valid_frames):
		frames.append(correct_frame)
	for c in range(missing_data_frames):
		frames.append(missing_data)
	for c in range(invalid_type_frame):
		frames.append(invalid_type)
	return frames


class TestLayout(AbstractLayout):
	@staticmethod
	def get_required_frame_data() -> dict:
		return dict(
			data_1=str,
			data_2=int,
			data_3=str
		)

	def generate_file(self, storyboard: dict):
		# can be ignored for the test
		pass


def gen_job(storyboard: dict):
	return RenderJob(MovieLayout, storyboard)


class TestRenderJobWorker(unittest.TestCase):
	def test_something(self):
		job = gen_job(dict(
			title="Test Title",
			author="Bernhard Brückenpfeiler",
			frames=get_frames(2, 0)
		))
		job_worker = JobWorker()
		job_worker.run_job(job)
		self.assertEqual(job.error_type, JobErrors.VALID)


if __name__ == '__main__':
	unittest.main()
