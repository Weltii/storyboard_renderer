import os
from enum import Enum
from layouts.movie_layout import MovieLayout


class JobSteps(Enum):
	READY_TO_START = "ready_to_start"
	VALIDATE_LAYOUT = "validate_layout"
	VALIDATE_DATA = "validate_data"
	GENERATE_TEX_DOC = "generate_tex_doc"
	COMPILE_PDF = "compile_pdf"
	FINISH = "finish"


class JobErrors(Enum):
	INVALID_LAYOUT = "invalid_layout"
	INVALID_DATA = "invalid_data"
	GENERATE_TEX_ERROR = "generate_tex_error"
	COMPILE_PDF_ERROR = "compile_pdf_error"
	UNKNOWN_ERROR = "unknown_error"
	VALID = "valid"


class DefaultStoryboardData(Enum):
	TITLE = "title"
	AUTHOR = "author"
	FRAMES = "frames"


class DefaultStoryboardDataTypes(Enum):
	TITLE = "str"
	AUTHOR = "str"
	FRAMES = "list"


def get_default_storyboard_data_type(data_name: DefaultStoryboardData):
	if data_name == DefaultStoryboardData.TITLE:
		return DefaultStoryboardDataTypes.TITLE
	if data_name == DefaultStoryboardData.AUTHOR:
		return DefaultStoryboardDataTypes.AUTHOR
	if data_name == DefaultStoryboardData.FRAMES:
		return DefaultStoryboardDataTypes.FRAMES
	return "Wrong key!"


Layouts = [
	MovieLayout
]

output_directory = path = os.path.join(os.path.dirname(__file__), "output")
