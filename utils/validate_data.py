from typing import Type

from render_job import RenderJob
from statics import DefaultStoryboardData, JobErrors, DefaultStoryboardDataTypes, get_default_storyboard_data_type, \
	JobSteps

is_missing = "{} is missing!"
has_wrong_type = "{} has the wrong type, it must be '{}', but it is '{}'"


def validate_data(job: RenderJob):
	job.step = JobSteps.VALIDATE_DATA
	required_data = job.layout().get_required_frame_data()
	invalid_data = dict()
	storyboard: dict = job.storyboard

	for data in DefaultStoryboardData:
		if data.value not in storyboard:
			invalid_data[data.value] = is_missing.format(data.value)
		elif type(storyboard[data.value]).__name__ != get_default_storyboard_data_type(data).value:
			invalid_data[
				data.value] = has_wrong_type.format(data.value, get_default_storyboard_data_type(data).value,
																						type(storyboard[data.value]).__name__)

	a = type(storyboard[DefaultStoryboardData.FRAMES.value]).__name__
	b = get_default_storyboard_data_type(DefaultStoryboardData.FRAMES).value
	if DefaultStoryboardData.FRAMES.value in storyboard and a == b:

		invalid_frames = dict()
		for frameIndex, frame in enumerate(storyboard["frames"]):
			invalid_frame = dict()
			for data in required_data:
				if data not in frame:
					invalid_frame[data] = is_missing.format(data)
				else:
					if type(frame[data]).__name__ != required_data[data].__name__:
						invalid_frame[
							data] = has_wrong_type.format(data, required_data[data].__name__, type(frame[data]).__name__)
			if len(invalid_frame.keys()) > 0:
				invalid_frames[f"{frameIndex}"] = invalid_frame
		if len(invalid_frames.keys()) > 0:
			invalid_data["frames"] = invalid_frames

	if len(invalid_data.keys()) > 0:
		job.error_type = JobErrors.INVALID_DATA
		job.error_data = invalid_data
