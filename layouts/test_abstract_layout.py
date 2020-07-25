import unittest

from layouts.movie_layout import MovieLayout


def get_frames(correct_frames: int, incorrect_frames: int):
	correct_frame = dict(
			scene="",
			setting="",
			section="",
			timecode="",
			image="",
			image_description="",
			audio_description="",
			setting_size="",
			perspective="",
			focal_length="",
			camera_movement="",
			camera_support="",
			fx=""
		)
	incorrect_frame = dict(
		scene="",
		setting="",
		section="",
		timecode="",
		image="",
		image_description="",
		audio_description="",
		setting_size="",
		perspective="",
		focal_length="",
		camera_movement="",
		camera_support=""
		# fx is missing
	)

	frames = []
	for c in range(correct_frames):
		frames.append(correct_frame)
	for c in range(incorrect_frames):
		frames.append(incorrect_frame)
	return frames


class MyTestCase(unittest.TestCase):
	def test_check_frames(self):
		layout = MovieLayout()
		missing_data_1 = layout.check_frames(get_frames(1, 1))
		missing_data_2 = layout.check_frames(get_frames(1, 0))
		self.assertEqual(missing_data_1.has_missing_data(), True)
		self.assertEqual(missing_data_2.has_missing_data(), False)

	def test_check_frames_find_right_data(self):
		layout = MovieLayout()
		missing_data = layout.check_frames(get_frames(1, 1))
		self.assertEqual(missing_data.invalid_data[0].frame_number, 1)
		self.assertEqual(missing_data.invalid_data[0].invalid_data, ["fx"])


if __name__ == '__main__':
	unittest.main()
