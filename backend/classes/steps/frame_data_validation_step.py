from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.layouts.Layouts import Layouts
from backend.utils.enums import Status, StepType

missing_data = "Frame_{}: {} is missing"
wrong_type = "Frame_{}: {} is from type {} instead of {}"


class FrameDataValidationStep(Step):
    @staticmethod
    def run(job: Job):
        # TODO add a regex matching for paths and if it's a path, check if the path exists
        if job.status is not Status.VALID:
            return
        job.step = StepType.VALIDATE_DATA
        required_data = getattr(Layouts, job.layout).value.get_required_frame_data()
        for index, frame in enumerate(job.project.storyboard.frames):
            for data in required_data:
                if not frame.get(data, False):
                    job.status = Status.INVALID_DATA
                    if not job.status_data.get("missing_data", False):
                        job.status_data["missing_data"] = dict()
                    job.status_data["missing_data"][str(index)] = missing_data.format(
                        str(index), data
                    )
                else:
                    type_a = type(frame.get(data))
                    type_b = required_data.get(data)
                    if type_a is not type_b:
                        job.status = Status.INVALID_DATA
                        if not job.status_data.get("wrong_data_type", False):
                            job.status_data["wrong_data_type"] = dict()
                        job.status_data["wrong_data_type"][
                            # the structure with a number as string in the dict is dirty
                            # todo Change number as string inside the dict!
                            str(index)
                        ] = wrong_type.format(
                            index, data, type_a.__name__, type_b.__name__
                        )
