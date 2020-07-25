from typing import Type
from statics import JobSteps, JobErrors
from storyboard import Storyboard


class Job:
    def __init__(self, layout: Type, storyboard: Storyboard):
        self.storyboard = storyboard
        self.layout = layout
        self.step = JobSteps.READY_TO_START
        self.status = JobErrors.VALID
        self.status_data = dict()
        self.tex_file_path = ""
        self.pdf_file_path = ""

    def get_status_code(self):
        if self.status == JobErrors.INVALID_LAYOUT:
            return 404
        if self.status == JobErrors.INVALID_DATA:
            return 404
        if self.status == JobErrors.GENERATE_TEX_ERROR:
            return 500
        if self.status == JobErrors.COMPILE_PDF_ERROR:
            return 500
        if self.status == JobErrors.UNKNOWN_ERROR:
            return 500
        if self.status == JobErrors.VALID:
            return 200
        return 500

    def __dict__(self):
        return dict(
            # storyboard=self.storyboard.to_dict(),
            layout=self.layout.__name__,
            step=str(self.step),
            error_type=str(self.status),
            error_data=self.status_data,
            tex_file_path=self.tex_file_path,
            pdf_file_path=self.pdf_file_path,
        )
