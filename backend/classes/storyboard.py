import json
import os

from pydantic import BaseModel
from typing import List

from backend.utils.utils import load_file_as_string


class Storyboard(BaseModel):
    title: str
    author: str
    frames: List = []

    @staticmethod
    def is_valid_storyboard_dict(json_dict: dict):
        for attr in ["title", "author", "frames"]:
            if not json_dict.get(attr, False):
                return False
        return True

    def to_dict(self) -> dict:
        return dict(title=self.title, author=self.author, frames=self.frames)

    @staticmethod
    def generate_from_file(path: str):
        if os.path.exists(path):
            return Storyboard.generate_from_string(load_file_as_string(path))
        else:
            raise FileNotFoundError

    @staticmethod
    def generate_from_string(string: str):
        json_dict = json.loads(string)
        if Storyboard.is_valid_storyboard_dict(json_dict):
            return Storyboard(
                title=json_dict["title"],
                author=json_dict["author"],
                frames=json_dict["frames"],
            )
