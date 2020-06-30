import unittest

from layouts.movie_layout import MovieLayout


def get_storyboard(frame_length):
	frame = dict(
		scene="001",
		setting="001",
		section="001",
		timecode="00:00:00:01",
		image="./example_image.png",
		image_description="image description",
		audio_description="audio description",
		setting_size="near",
		perspective="bird perspective",
		focal_length="85",
		camera_movement="Static",
		camera_support="Tripod",
		fx="-"
	)
	frames = []
	for x in range(frame_length):
		frames.append(frame)

	return dict(
		title="",
		author="",
		frames=frames
	)


frame_string = \
			"\n\t{\storyboardFrame" \
			"\n\t\t{\storyboardFrameHead" \
			"\n\t\t\t{001}" \
			"\n\t\t\t{001}" \
			"\n\t\t\t{001}" \
			"\n\t\t\t{00:00:00:01}" \
			"\n\t\t}" \
			"\n\t\t{\storyboardFrameContent" \
			"\n\t\t\t{./example_image.png}" \
			"\n\t\t\t{image description}" \
			"\n\t\t\t{audio description}" \
			"\n\t\t}" \
			"\n\t\t{\storyboardFrameFooter" \
			"\n\t\t\t{near}" \
			"\n\t\t\t{bird perspective}" \
			"\n\t\t\t{85}" \
			"\n\t\t\t{Static}" \
			"\n\t\t\t{Tripod}" \
			"\n\t\t\t{-}" \
			"\n\t\t}" \
			"\n\t}"


class MyTestCase(unittest.TestCase):
	def test_generate_frame(self):
		layout = MovieLayout()
		frame = get_storyboard(1)["frames"][0]
		self.assertEqual(layout.generate_frame(frame), frame_string)

	def test_generate_frames(self):
		layout = MovieLayout()
		frames = layout.generate_frames(get_storyboard(2))
		expected = "" \
							 "\storyboardPage" \
							 f"{frame_string}" \
							 f"{frame_string}"
		self.assertEqual(frames, expected)

	def test_generate_frames_odd_frame_count(self):
		layout = MovieLayout()
		frames = layout.generate_frames(get_storyboard(2))
		frames += "\storyboardPage" \
							"\n\t{}"
		expected = "" \
							 "\storyboardPage" \
							 f"{frame_string}" \
							 f"{frame_string}" \
							 "\storyboardPage" \
							 "\n\t{}"
		self.assertEqual(frames, expected)
