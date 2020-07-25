from render_job import RenderJob
from statics import (
    DefaultStoryboardData,
    JobErrors,
    get_default_storyboard_data_type,
    JobSteps,
)
from storyboard import Storyboard

is_missing = "{} is missing!"
has_wrong_type = "{} has the wrong type, it must be '{}', but it is '{}'"
string_is_empty = "Attribute {} is empty!"


def validate_data(job: RenderJob):
    job.step = JobSteps.VALIDATE_DATA
    required_data = job.layout().get_required_frame_data()
    invalid_data = dict()
    storyboard: Storyboard = job.storyboard

    for data in DefaultStoryboardData:
        data_value = getattr(storyboard, str(data.value)) if hasattr(storyboard, str(data.value)) else None
        # check if the value is from type str, that the value is not empty
        if type(data_value) is str and not data_value:
            invalid_data[data.value] = string_is_empty.format(data.value)

    a = type(getattr(storyboard, "frames")).__name__
    b = get_default_storyboard_data_type(DefaultStoryboardData.FRAMES).value
    if hasattr(storyboard, DefaultStoryboardData.FRAMES.value) and a == b:
        invalid_frames = dict()
        for frameIndex, frame in enumerate(getattr(storyboard, "frames")):
            invalid_frame = dict()
            for data in required_data:
                if data not in frame:
                    invalid_frame[data] = is_missing.format(data)
                else:
                    if type(frame[data]).__name__ != required_data[data].__name__:
                        invalid_frame[data] = has_wrong_type.format(
                            data,
                            required_data[data].__name__,
                            type(frame[data]).__name__,
                        )
            if len(invalid_frame.keys()) > 0:
                invalid_frames[f"{frameIndex}"] = invalid_frame
        if len(invalid_frames.keys()) > 0:
            invalid_data["frames"] = invalid_frames

    if len(invalid_data.keys()) > 0:
        job.error_type = JobErrors.INVALID_DATA
        job.error_data = invalid_data
