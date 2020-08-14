from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.layouts.Layouts import Layouts
from backend.utils.enums import Status, StepType

missing_data = "{} is missing"
wrong_type = "{} is from type {} instead of {}"


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
                        job.status_data["missing_data"] = []
                    job.status_data["missing_data"].append(dict(
                        index=index,
                        frame=index + 1,
                        message=missing_data.format(data)
                    ))
                else:
                    type_a = type(frame.get(data))
                    type_b = required_data.get(data)
                    if type_a is not type_b:
                        job.status = Status.INVALID_DATA
                        if not job.status_data.get("wrong_data_type", False):
                            job.status_data["wrong_data_type"] = []
                        job.status_data["wrong_data_type"].append(dict(
                            index=index,
                            frame=index + 1,
                            message=wrong_type.format(data, type_a.__name__, type_b.__name__)
                        ))
