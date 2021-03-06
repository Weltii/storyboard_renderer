import os
from typing import List

from backend.classes.project import Project
from backend.classes.storyboard import Storyboard
from backend.layouts.abstract_layout import AbstractLayout
from backend.utils.enums import LayoutName
from backend.utils.utils import load_file_as_string


class EasyLayout(AbstractLayout):
    @staticmethod
    def get_name():
        return LayoutName.EASY_LAYOUT

    @staticmethod
    def get_description():
        return "A simple layout to visualize an image with text"

    template_path = os.path.join(
        os.path.dirname(__file__), "templates/easy_layout_template.tex"
    )

    @staticmethod
    def _generate_frames_string(frames: List) -> str:
        frames_per_page = 5
        ret = ""
        counter = 0
        if frames:
            # generate pages for the frames
            for frame in frames:
                if counter % frames_per_page is 0:
                    ret += "\\storyboardPage\n"
                ret += f"\t{EasyLayout._generate_frame_string(frame)}\n"
                counter += 1
            # fill missing frames
            for c in range((frames_per_page - len(frames)) % frames_per_page):
                # call with an empty dict to get a empty frame_string
                ret += f"\t{EasyLayout._generate_frame_string(dict())}\n"

        return ret

    @staticmethod
    def generate_file_string(project: Project):
        template = load_file_as_string(EasyLayout.template_path)
        template = template.replace("%*imagepath*", project.images_directory)
        template = template.replace("%*title*", project.storyboard.title)
        template = template.replace("%*author*", project.storyboard.author)
        template = template.replace(
            "%*frames*", EasyLayout._generate_frames_string(project.storyboard.frames)
        )
        return template

    @staticmethod
    def get_required_frame_data() -> dict:
        return dict(image=str, image_description=str)

    @staticmethod
    def _generate_frame_string(frame: dict) -> str:
        if frame:
            return (
                "{\\storyboardFrame{"
                + frame.get("image", 'data "image" is missing in this frame')
                + "}{"
                + frame.get(
                    "image_description",
                    'data "image_description" is missing in this frame',
                )
                + "}}"
            )
        return "{}"
