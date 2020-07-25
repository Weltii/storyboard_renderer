from enum import Enum


class StepType(Enum):
    READY_TO_START = "ready_to_start"
    VALIDATE_LAYOUT = "validate_layout"
    VALIDATE_DATA = "validate_data"
    GENERATE_TEX_DOC = "generate_tex_doc"
    COMPILE_PDF = "compile_pdf"
    FINISHED = "finished"


class Status(Enum):
    INVALID_LAYOUT = "invalid_layout"
    INVALID_DATA = "invalid_data"
    GENERATE_TEX_ERROR = "generate_tex_error"
    COMPILE_PDF_ERROR = "compile_pdf_error"
    UNKNOWN_ERROR = "unknown_error"
    VALID = "valid"
