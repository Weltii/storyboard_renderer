import json
import os
import unittest
from shutil import copyfile, rmtree

from backend.classes.project import Project
from backend.classes.storyboard import Storyboard
from backend.config import sample_data_path
from backend.utils.utils import (
    StoryboardFileNotFound,
    write_file,
    InvalidStoryboard,
    DirectoryIsNotEmpty,
)

project_folder_path = os.path.join(
    "/tmp/", f"temporary_test_folder_{str(hash('test_directory'))}"
)
image_folder_path = os.path.join(project_folder_path, "images")


def generate_temporary_project_folder(
    copy_storyboard: bool = True, copy_images: bool = True
):
    os.mkdir(project_folder_path)
    if copy_storyboard:
        copyfile(
            os.path.join(sample_data_path, "sample_storyboard.json"),
            os.path.join(project_folder_path, "storyboard.json"),
        )
    if copy_images:
        os.mkdir(image_folder_path)
        copyfile(
            os.path.join(sample_data_path, "sample_image.jpg"),
            os.path.join(image_folder_path, "sample_image_1.jpg"),
        )
        copyfile(
            os.path.join(sample_data_path, "sample_image_2.png"),
            os.path.join(image_folder_path, "sample_image_2.png"),
        )


def remove_temporary_project_folder():
    rmtree(project_folder_path)


class TestProject(unittest.TestCase):
    def test_init(self):
        storyboard = Storyboard(
            title="test storyboard", author="Bernhard Brueckenpfeiler", frames=[]
        )
        generate_temporary_project_folder(False, False)
        project = Project(path=project_folder_path, storyboard=storyboard)
        self.assertIsNotNone(project)
        self.assertEqual(project.path, project_folder_path)
        self.assertEqual(project.storyboard, storyboard)
        self.assertEqual(project.image_hashes, [])
        self.assertEqual(project.images_directory, os.path.join(project_folder_path, "images"))
        self.assertEqual(project.output_directory, os.path.join(project_folder_path, "output"))
        remove_temporary_project_folder()

    def test_generate_image_hashes(self):
        generate_temporary_project_folder()
        storyboard = Storyboard(
            title="test storyboard", author="Bernhard Brueckenpfeiler", frames=[]
        )
        project = Project(path=project_folder_path, storyboard=storyboard)
        expected_image_hashes = [
            dict(file_type=".png", hash="00087e7ffffe2c00", file_name="sample_image_2"),
            dict(file_type=".jpg", hash="7f3f1e0c003e381f", file_name="sample_image_1"),
        ]
        self.assertEquals(project.image_hashes, expected_image_hashes)
        remove_temporary_project_folder()

    @unittest.skip("Not implemented")
    def test_save_project(self):
        generate_temporary_project_folder()
        expected_storyboard = Storyboard(
            title="test storyboard", author="Bernhard Brueckenpfeiler", frames=[]
        )
        project = Project.load_from_path(project_folder_path)
        project.storyboard = expected_storyboard
        project.save_project()
        storyboard = Storyboard.generate_from_file(
            os.path.join(project_folder_path, "storyboard.json")
        )
        self.assertEquals(storyboard, expected_storyboard)
        remove_temporary_project_folder()

    # load_from_path

    def test_load_from_path_valid_load_directory_path(self):
        generate_temporary_project_folder()
        project = Project.load_from_path(project_folder_path)
        self.assertIsNotNone(project)
        remove_temporary_project_folder()

    def test_load_from_path_valid_load_storyboard_file_path(self):
        generate_temporary_project_folder()
        project = Project.load_from_path(
            os.path.join(project_folder_path, "storyboard.json")
        )
        self.assertIsNotNone(project)
        remove_temporary_project_folder()

    def test_load_from_path_invalid_path_not_found(self):
        with self.assertRaises(FileNotFoundError):
            Project.load_from_path(project_folder_path)

    def test_load_from_path_invalid_storyboard_not_found(self):
        generate_temporary_project_folder(False, True)
        with self.assertRaises(StoryboardFileNotFound):
            Project.load_from_path(project_folder_path)
        remove_temporary_project_folder()

    def test_load_from_path_invalid_invalid_storyboard(self):
        generate_temporary_project_folder(False, True)
        string = json.dumps(dict(a="Hello World!"))
        write_file(os.path.join(project_folder_path, "storyboard.json"), string)
        with self.assertRaises(InvalidStoryboard):
            Project.load_from_path(project_folder_path)
        remove_temporary_project_folder()

    # generate_new_project

    def test_generate_new_project_valid(self):
        generate_temporary_project_folder(False, False)
        project = Project.generate_new_project(project_folder_path)
        self.assertIsNotNone(project)
        remove_temporary_project_folder()

    def test_generate_new_project_invalid_directory_is_not_empty(self):
        generate_temporary_project_folder()
        with self.assertRaises(DirectoryIsNotEmpty):
            Project.generate_new_project(project_folder_path)
        remove_temporary_project_folder()


if __name__ == "__main__":
    unittest.main()
