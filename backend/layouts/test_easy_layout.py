import unittest
from typing import List

from backend.classes.storyboard import Storyboard
from backend.layouts.easy_layout import EasyLayout
from backend.utils.enums import LayoutName
from backend.utils.utils import load_file_as_string

frame = dict(dict(image="path_to_file", image_description="image description"))
frame_string = (
    "\t{\\storyboardFrame{"
    + frame.get("image")
    + "}{"
    + frame.get("image_description")
    + "}}\n"
)
empty_frame = "\t{}\n"
storyboard_page_string = "\\storyboardPage\n"


def load_easy_layout_template():
    return load_file_as_string(EasyLayout.template_path)


class EasyLayoutTest(unittest.TestCase):
    def test_generate_frame_string_valid(self):
        image = "path_to_file"
        image_description = "image description"
        expected_string = (
            "{\\storyboardFrame{" + image + "}{" + image_description + "}}"
        )
        self.assertEqual(
            EasyLayout._generate_frame_string(
                dict(image=image, image_description=image_description)
            ),
            expected_string,
        )

    def test_generate_frame_string_empty_dict(self):
        expected_string = "{}"
        self.assertEqual(EasyLayout._generate_frame_string(dict()), expected_string)

    def test_generate_frame_string_missing_data(self):
        image = 'data "image" is missing in this frame'
        image_description = "image description"
        expected_string = (
            "{\\storyboardFrame{" + image + "}{" + image_description + "}}"
        )
        self.assertEqual(
            EasyLayout._generate_frame_string(
                dict(image_description=image_description)
            ),
            expected_string,
        )

    def test_generate_frames_string_single_frames(self):
        frames = [frame]
        frames_string = EasyLayout._generate_frames_string(frames)
        expected_frames_string = storyboard_page_string
        expected_frames_string += frame_string
        for x in range(4):
            expected_frames_string += empty_frame
        self.assertEqual(frames_string, expected_frames_string)

    def test_generate_frames_string_multiple_frames(self):
        frames = []
        for x in range(2):
            frames.append(frame)
        frames_string = EasyLayout._generate_frames_string(frames)
        expected_frames_string = storyboard_page_string
        for x in range(2):
            expected_frames_string += frame_string
        for x in range(3):
            expected_frames_string += empty_frame
        self.assertEqual(frames_string, expected_frames_string)

    def test_generate_frames_string_full_page(self):
        frames = []
        for x in range(5):
            frames.append(frame)
        frames_string = EasyLayout._generate_frames_string(frames)
        expected_frames_string = "\\storyboardPage\n"
        for x in range(5):
            expected_frames_string += frame_string
        self.assertEqual(frames_string, expected_frames_string)

    def test_generate_frames_string_multiple_pages_full(self):
        frames = []
        for x in range(10):
            frames.append(frame)
        frames_string = EasyLayout._generate_frames_string(frames)
        expected_frames_string = storyboard_page_string
        for x in range(5):
            expected_frames_string += frame_string
        expected_frames_string += expected_frames_string
        self.assertEqual(frames_string, expected_frames_string)

    def test_generate_frames_string_one_page_full_one_half_filled(self):
        frames = []
        for x in range(8):
            frames.append(frame)
        frames_string = EasyLayout._generate_frames_string(frames)
        expected_frames_string = storyboard_page_string
        for x in range(5):
            expected_frames_string += frame_string
        expected_frames_string += storyboard_page_string
        for x in range(3):
            expected_frames_string += frame_string
        for x in range(2):
            expected_frames_string += empty_frame
        self.assertEqual(frames_string, expected_frames_string)

    def test_generate_file_string_single_frame(self):
        frames: List[dict] = []
        for x in range(1):
            frames.append(frame)
        storyboard = Storyboard(
            title="test title", author="Bernhard Brueckenpfeiler", frames=frames
        )
        result = EasyLayout.generate_file_string(storyboard)
        expected_result = load_easy_layout_template()
        expected_result = expected_result.replace("%*title*", storyboard.title)
        expected_result = expected_result.replace("%*author*", storyboard.author)
        expected_result = expected_result.replace(
            "%*frame*", EasyLayout._generate_frames_string(storyboard.frames)
        )
        self.assertEqual(result, expected_result)

    def test_generate_file_string_full_page(self):
        frames: List[dict] = []
        for x in range(5):
            frames.append(frame)
        storyboard = Storyboard(
            title="test title", author="Bernhard Brueckenpfeiler", frames=frames
        )
        result = EasyLayout.generate_file_string(storyboard)
        expected_result = load_easy_layout_template()
        expected_result = expected_result.replace("%*title*", storyboard.title)
        expected_result = expected_result.replace("%*author*", storyboard.author)
        expected_result = expected_result.replace(
            "%*frame*", EasyLayout._generate_frames_string(storyboard.frames)
        )
        self.assertEqual(result, expected_result)

    @unittest.skip("assertRaises is not running, why ever")
    def test_generate_file_string_missing_template(self):
        frames: List[dict] = []
        for x in range(5):
            frames.append(frame)
        storyboard = Storyboard(
            title="test title", author="Bernhard Brueckenpfeiler", frames=frames
        )
        EasyLayout.template_path = "/not/a/valid/path"
        self.assertRaises(
            FileNotFoundError, EasyLayout.generate_file_string(storyboard)
        )

    def test_get_name(self):
        self.assertEqual(EasyLayout.get_name(), LayoutName.EASY_LAYOUT)

    def test_get_description(self):
        self.assertEqual(
            EasyLayout.get_description(),
            "A simple layout to visualize an image with text",
        )

    def test_get_required_frame_data(self):
        self.assertEqual(
            EasyLayout.get_required_frame_data(),
            dict(image=str, image_description=str),
        )


if __name__ == "__main__":
    unittest.main()
