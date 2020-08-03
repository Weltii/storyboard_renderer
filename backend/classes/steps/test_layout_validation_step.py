import unittest

from backend.classes.render_job import Job
from backend.classes.steps.layout_validation_step import LayoutValidationStep
from backend.classes.storyboard import Storyboard
from backend.sample_data.sample_generator import generate_sample_project
from backend.utils.enums import LayoutName

storyboard = Storyboard(
    title="test title", author="Bernhard Brueckenpfeiler", frames=[]
)


class TestLayoutValidationStep(unittest.TestCase):
    def test_run_with_valid_layout(self):
        job = Job(layout=LayoutName.EASY_LAYOUT.value, project=generate_sample_project())
        self.assertTrue(LayoutValidationStep.run(job))

    def test_run_with_invalid_layout(self):
        job = Job(layout="SuperHeroLayout", project=generate_sample_project())
        self.assertFalse(LayoutValidationStep.run(job))


if __name__ == "__main__":
    unittest.main()
