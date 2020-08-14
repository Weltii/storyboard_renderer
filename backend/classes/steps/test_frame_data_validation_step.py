import os
import unittest

from backend.classes.project import Project
from backend.classes.render_job import Job
from backend.classes.steps.frame_data_validation_step import FrameDataValidationStep
from backend.classes.storyboard import Storyboard
from backend.config import sample_data_path
from backend.utils.enums import LayoutName, Status

sample_image_path = os.path.join(sample_data_path, "sample_image.jpg")


def generate_storyboard():
    return Storyboard(title="test title", author="Bernhard Brueckenpfeiler", frames=[])


def generate_project():
    return Project(path="", storyboard=generate_storyboard())


class TestFrameDataValidationStep(unittest.TestCase):
    def test_run_valid_frame_data(self):
        project = generate_project()
        job = Job(layout=LayoutName.EASY_LAYOUT.value, project=project)
        for x in range(2):
            job.project.storyboard.frames.append(
                dict(image=sample_image_path, image_description="image_description")
            )
        FrameDataValidationStep.run(job)
        self.assertEqual(job.status, Status.VALID)

    def test_run_data_is_missing(self):
        error_layout = "{} is missing"
        expected_data = [
            dict(index=0, message=error_layout.format("image_description")),
            dict(index=1, message=error_layout.format("image")),
            dict(index=2, message=error_layout.format("image")),
            dict(index=2, message=error_layout.format("image_description")),
        ]
        project = generate_project()
        job = Job(layout=LayoutName.EASY_LAYOUT.value, project=project)
        job.project.storyboard.frames.append(dict(image="path_to_file"))
        job.project.storyboard.frames.append(
            dict(image_description="image_description")
        )
        job.project.storyboard.frames.append(dict())
        FrameDataValidationStep.run(job)
        self.assertEqual(job.status, Status.INVALID_DATA)
        for index in range(len(expected_data)):
            ed = expected_data[index]
            self.assertEqual(job.status_data["missing_data"][index], dict(
                index=ed["index"],
                frame=ed["index"] + 1,
                message=ed["message"]
            ))

    def test_run_data_has_wrong_type(self):
        error_layout = "{} is from type {} instead of {}"
        project = generate_project()
        job = Job(layout=LayoutName.EASY_LAYOUT.value, project=project)
        job.project.storyboard.frames.append(
            dict(image=120, image_description="image_description")
        )
        job.project.storyboard.frames.append(
            dict(image="path_to_file", image_description=120)
        )
        FrameDataValidationStep.run(job)
        self.assertEqual(job.status, Status.INVALID_DATA)
        self.assertEqual(
            job.status_data["wrong_data_type"][0],
            dict(
                index=0,
                frame=1,
                message=error_layout.format("image", int.__name__, str.__name__)
            )
        )
        self.assertEqual(
            job.status_data["wrong_data_type"][1],
            dict(
                index=1,
                frame=2,
                message=error_layout.format("image_description", int.__name__, str.__name__)
            )
        )

    def test_run_data_mixed_errors(self):
        wrong_type_error = "{} is from type {} instead of {}"
        missing_data_error = "{} is missing"
        project = generate_project()
        job = Job(layout=LayoutName.EASY_LAYOUT.value, project=project)
        job.project.storyboard.frames.append(dict(image=120))
        job.project.storyboard.frames.append(
            dict(image="path_to_file", image_description=120)
        )
        FrameDataValidationStep.run(job)
        self.assertEqual(job.status, Status.INVALID_DATA)
        self.assertEqual(
            job.status_data["missing_data"][0],
            dict(
                index=0,
                frame=1,
                message=missing_data_error.format("image_description", int.__name__, str.__name__)
            )
        )
        self.assertEqual(
            job.status_data["wrong_data_type"][1],
            dict(
                index=1,
                frame=2,
                message=wrong_type_error.format("image_description", int.__name__, str.__name__)
            )
        )


if __name__ == "__main__":
    unittest.main()
