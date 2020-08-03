import os
import unittest
from datetime import datetime

from backend.classes.storyboard import Storyboard
from backend.project_handler import ProjectHandler
from backend.sample_data.sample_generator import generate_sample_project, remove_project
from backend.utils.utils import load_file_as_string, DirectoryIsNotEmpty


class TestProjectHandler(unittest.TestCase):
    def test_save_project_current_project(self):
        project_handler = ProjectHandler()
        project = generate_sample_project()
        project_handler.current_project = project

        storyboard = Storyboard.generate_from_file(os.path.join(project.path, "storyboard.json"))
        self.assertEqual(project.storyboard, storyboard)

        project.storyboard.title = "Is now different"
        project_handler.save_project()

        storyboard_after = Storyboard.generate_from_file(os.path.join(project.path, "storyboard.json"))
        self.assertEqual(project.storyboard, storyboard_after)
        self.assertNotEqual(storyboard_after, storyboard)

        remove_project(project_handler.current_project.path)

    def test_load_project_valid_path(self):
        project_handler = ProjectHandler()
        path = generate_sample_project().path
        project_handler.load_project(path)

        self.assertIsNotNone(project_handler.current_project)

        remove_project(path)

    def test_load_project_invalid_path(self):
        project_handler = ProjectHandler()
        with self.assertRaises(FileNotFoundError):
            project_handler.load_project("/not/a/valid/project/path")

    def test_load_project_has_current_project(self):
        project_handler = ProjectHandler()
        project = generate_sample_project()
        project_handler.current_project = project

        self.assertIsNone(project_handler.load_project(project.path))

    def test_create_new_project_valid_path(self):
        project_handler = ProjectHandler()
        path = f"/tmp/test_project_{str(datetime.now().timestamp()).replace('.', '_')}"
        os.mkdir(path)
        project_handler.create_new_project(path)

        self.assertIsNotNone(project_handler.current_project)

        remove_project(path)

    def test_create_new_project_invalid_path(self):
        project_handler = ProjectHandler()
        with self.assertRaises(DirectoryIsNotEmpty):
            project_handler.create_new_project("/not/a/valid/project/path")

    def test_create_new_project_has_current_project(self):
        project_handler = ProjectHandler()
        path = f"/tmp/test_project_{str(datetime.now().timestamp()).replace('.', '_')}"
        os.mkdir(path)
        project_handler.load_project(generate_sample_project().path)

        self.assertIsNone(project_handler.create_new_project(path))

        remove_project(project_handler.current_project.path)
        remove_project(path)


if __name__ == '__main__':
    unittest.main()
