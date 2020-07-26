from backend.classes.render_job import Job
from backend.classes.step import Step
from backend.layouts.Layouts import Layouts
from backend.utils.enums import Status

missing_data = "Frame_{}: {} is missing"
wrong_type = "Frame_{}: {} is from type {} instead of {}"


class FrameDataValidationStep(Step):
    @staticmethod
    def run(job: Job):
        required_data = getattr(Layouts, job.layout).value.get_required_frame_data()
        for index, frame in enumerate(job.storyboard.frames):
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
                            str(index)
                        ] = wrong_type.format(
                            index, data, type_a.__name__, type_b.__name__
                        )
