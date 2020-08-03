import base64
import os
import unittest

from backend.config import sample_data_path
from backend.utils.utils import (
    base64_image_add_type,
    remove_base64_info,
    generate_file_hash,
    get_directory_of_file,
)

with open(os.path.join(sample_data_path, "sample_image_2.png"), "rb") as image_file:
    base64_string = base64.b64encode(image_file.read())


class TestUtils(unittest.TestCase):
    def test_base64_image_add_type(self):
        image_type = ".png"
        expected_string = f"data:image/png;base64,{base64_string}"
        output = base64_image_add_type(base64_string, image_type)
        self.assertEqual(output, expected_string)

    @unittest.skip("Strange string change here, check this!")  # TODO check the error!
    def test_remove_base64_info(self):
        input_string = f"data:image/png;base64,{base64_string}"
        output = remove_base64_info(input_string)
        self.assertEqual(output, base64_string)

    def test_generate_file_hash(self):
        file_path = os.path.join(sample_data_path, "sample_image_2.png")
        expected_info = dict(
            file_type=".png", hash="00087e7ffffe2c00", file_name="sample_image_2"
        )
        output = generate_file_hash(file_path)
        self.assertEqual(expected_info["file_type"], output["file_type"])
        self.assertEqual(expected_info["file_name"], output["file_name"])
        self.assertEqual(str(output["hash"]), expected_info["hash"])

    def test_get_directory_of_file(self):
        path = "/home/test/xy/test.txt"
        expected_path = "/home/test/xy"
        output = get_directory_of_file(path)
        self.assertEqual(output, expected_path)


if __name__ == "__main__":
    unittest.main()
