import unittest

from layouts.abstract_layout import AbstractLayout
from render_job import RenderJob
from statics import JobErrors
from utils.validate_data import validate_data


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
	return RenderJob(TestLayout, storyboard)


class TestValidateData(unittest.TestCase):
	def test_valid_default_data(self):
		job = gen_job(dict(
			title="Test Title",
			author="Bernhard Brückenpfeiler",
			frames=[]
		))
		validate_data(job)
		self.assertEqual(job.error_type, JobErrors.VALID)

	def test_missing_default_data(self):
		job = gen_job(dict(
			author="Bernhard Brückenpfeiler",
			frames=[]
		))
		validate_data(job)
		self.assertEqual(job.error_type, JobErrors.INVALID_DATA)
		self.assertEqual(job.error_data['title'], 'title is missing!')

	def test_invalid_default_data_type(self):
		job = gen_job(dict(
			title="Test Title",
			author=42,
			frames="Bernhard Brückenpfeiler"
		))
		validate_data(job)
		self.assertEqual(job.error_type, JobErrors.INVALID_DATA)
		self.assertEqual(job.error_data['author'], "author has the wrong type, it must be 'str', but it is 'int'")
		self.assertEqual(job.error_data['frames'], "frames has the wrong type, it must be 'list', but it is 'str'")

	def test_valid_frame_data(self):
		job = gen_job(dict(
			title="Test Title",
			author="Bernhard Brückenpfeiler",
			frames=get_frames(2)
		))
		validate_data(job)
		self.assertEqual(job.error_type, JobErrors.VALID)

	def test_missing_data(self):
		job = gen_job(dict(
			title="Test Title",
			author="Bernhard Brückenpfeiler",
			frames=get_frames(0, 1)
		))
		validate_data(job)
		self.assertEqual(job.error_type, JobErrors.INVALID_DATA)
		self.assertEqual(job.error_data['frames']['0']['data_2'], 'data_2 is missing!')
		self.assertEqual(job.error_data['frames']['0']['data_3'], 'data_3 is missing!')

	def test_invalid_data_types(self):
		job = gen_job(dict(
			title="Test Title",
			author="Bernhard Brückenpfeiler",
			frames=get_frames(0, 0, 1)
		))
		validate_data(job)
		self.assertEqual(job.error_type, JobErrors.INVALID_DATA)
		self.assertEqual(job.error_data['frames']['0']['data_1'],
										 "data_1 has the wrong type, it must be 'str', but it is 'int'")
		self.assertEqual(job.error_data['frames']['0']['data_2'],
										 "data_2 has the wrong type, it must be 'int', but it is 'str'")


if __name__ == '__main__':
	unittest.main()
