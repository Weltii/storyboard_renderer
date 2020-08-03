import json
import os
import unittest

from backend.classes.storyboard import Storyboard
from backend.config import sample_data_path
from backend.utils.utils import write_file


def generate_storyboard():
    return Storyboard(
        title="test storyboard",
        author="Bernhard Brueckenpfeiler",
        frames=[
            dict(
                image=os.path.join(sample_data_path, "sample_image.jpg"),
                image_description="image_description",
            )
        ],
    )


class TestStoryboard(unittest.TestCase):
    def test_is_valid_storyboard_dict_valid(self):
        storyboard_dict = dict(
            title="test storyboard",
            author="Bernhard Brueckenpfeiler",
            frames=[
                dict(
                    image=os.path.join(sample_data_path, "sample_image.jpg"),
                    image_description="image_description",
                )
            ],
        )
        is_valid = Storyboard.is_valid_storyboard_dict(storyboard_dict)
        self.assertTrue(is_valid)

    def test_is_valid_storyboard_dict_invalid(self):
        storyboard_dict = dict(
            title="test storyboard",
            missing_author="Bernhard Brueckenpfeiler",
            frames=[
                dict(
                    image=os.path.join(sample_data_path, "sample_image.jpg"),
                    image_description="image_description",
                )
            ],
        )
        is_valid = Storyboard.is_valid_storyboard_dict(storyboard_dict)
        self.assertFalse(is_valid)

    def test_to_dict(self):
        expected_storyboard_dict = dict(
            title="test storyboard",
            author="Bernhard Brueckenpfeiler",
            frames=[
                dict(
                    image=os.path.join(sample_data_path, "sample_image.jpg"),
                    image_description="image_description",
                )
            ],
        )
        storyboard_dict = generate_storyboard().to_dict()
        self.assertEqual(storyboard_dict, expected_storyboard_dict)

    def test_generate_from_string_valid(self):
        json_string = json.dumps(
            dict(
                title="test storyboard",
                author="Bernhard Brueckenpfeiler",
                frames=[
                    dict(
                        image=os.path.join(sample_data_path, "sample_image.jpg"),
                        image_description="image_description",
                    )
                ],
            )
        )
        storyboard = Storyboard.generate_from_string(json_string)
        self.assertEqual(storyboard, generate_storyboard())

    def test_generate_from_string_invalid(self):
        json_string = json.dumps(
            dict(
                title="test storyboard",
                missing_author="Bernhard Brueckenpfeiler",
                frames=[
                    dict(
                        image=os.path.join(sample_data_path, "sample_image.jpg"),
                        image_description="image_description",
                    )
                ],
            )
        )
        storyboard = Storyboard.generate_from_string(json_string)
        self.assertIsNone(storyboard)

    def test_generate_from_file_valid(self):
        json_string = json.dumps(
            dict(
                title="test storyboard",
                author="Bernhard Brueckenpfeiler",
                frames=[
                    dict(
                        image=os.path.join(sample_data_path, "sample_image.jpg"),
                        image_description="image_description",
                    )
                ],
            )
        )
        storyboard_file_path = os.path.join(
            "/tmp/", f"temporary_test_file_{str(hash('test_directory'))}.json"
        )
        write_file(storyboard_file_path, json_string)

        storyboard = Storyboard.generate_from_file(storyboard_file_path)
        self.assertEqual(storyboard, generate_storyboard())

    def test_generate_from_file_invalid(self):
        json_string = json.dumps(
            dict(
                title="test storyboard",
                missing_author="Bernhard Brueckenpfeiler",
                frames=[
                    dict(
                        image=os.path.join(sample_data_path, "sample_image.jpg"),
                        image_description="image_description",
                    )
                ],
            )
        )
        storyboard_file_path = os.path.join(
            "/tmp/", f"temporary_test_file_{str(hash('test_directory'))}.json"
        )
        write_file(storyboard_file_path, json_string)

        storyboard = Storyboard.generate_from_file(storyboard_file_path)
        self.assertIsNone(storyboard)


if __name__ == "__main__":
    unittest.main()
