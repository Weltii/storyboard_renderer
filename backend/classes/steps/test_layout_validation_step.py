import unittest

from backend.classes.render_job import Job
from backend.classes.steps.layout_validation_step import LayoutValidationStep
from backend.classes.storyboard import Storyboard
from backend.utils.enums import LayoutName

storyboard = Storyboard(
    title="test title", author="Bernhard Brueckenpfeiler", frames=[]
)


class TestLayoutValidationStep(unittest.TestCase):
    def test_run_with_valid_layout(self):
        job = Job(layout=LayoutName.EASY_LAYOUT.value, storyboard=storyboard)
        self.assertTrue(LayoutValidationStep.run(job))

    def test_run_with_invalid_layout(self):
        job = Job(layout="SuperHeroLayout", storyboard=storyboard)
        self.assertFalse(LayoutValidationStep.run(job))


if __name__ == "__main__":
    unittest.main()
