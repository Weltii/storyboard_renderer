from pydantic import BaseModel

from backend.classes.storyboard import Storyboard
from backend.utils.enums import StepType, Status


class Job(BaseModel):
    storyboard: Storyboard
    layout: str
    step: StepType = StepType.READY_TO_START
    status: Status = Status.VALID
    status_data: dict = dict()
    tex_file_path: str = ""
    pdf_file_path: str = ""

    def get_status_code(self):
        if self.status == Status.INVALID_LAYOUT:
            return 404
        if self.status == Status.INVALID_DATA:
            return 404
        if self.status == Status.GENERATE_TEX_ERROR:
            return 500
        if self.status == Status.COMPILE_PDF_ERROR:
            return 500
        if self.status == Status.UNKNOWN_ERROR:
            return 500
        if self.status == Status.VALID:
            return 200
        return 500

    def to_dict(self):
        return dict(
            # storyboard=self.storyboard.to_dict(),
            layout=self.layout,
            step=str(self.step),
            error_type=str(self.status),
            error_data=self.status_data,
            tex_file_path=self.tex_file_path,
            pdf_file_path=self.pdf_file_path,
        )
