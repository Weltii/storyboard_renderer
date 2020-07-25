from typing import Type
from statics import JobSteps, JobErrors
from storyboard import Storyboard


class RenderJob:
	def __init__(self, layout: Type, storyboard: Storyboard):
		self.storyboard = storyboard
		self.layout = layout
		self.step = JobSteps.READY_TO_START
		self.error_type = JobErrors.VALID
		self.error_data = dict()
		self.tex_file_path = ""
		self.pdf_file_path = ""

	def get_status_code(self):
		if self.error_type == JobErrors.INVALID_LAYOUT:
			return 404
		if self.error_type == JobErrors.INVALID_DATA:
			return 404
		if self.error_type == JobErrors.GENERATE_TEX_ERROR:
			return 500
		if self.error_type == JobErrors.COMPILE_PDF_ERROR:
			return 500
		if self.error_type == JobErrors.UNKNOWN_ERROR:
			return 500
		if self.error_type == JobErrors.VALID:
			return 200
		return 500

	
	def to_dict(self):
		return dict(
			# storyboard=self.storyboard.to_dict(),
			layout=self.layout.__name__,
			step=str(self.step),
			error_type=str(self.error_type),
			error_data=self.error_data,
			tex_file_path=self.tex_file_path,
			pdf_file_path=self.pdf_file_path
		)

