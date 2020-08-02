from pydantic import BaseModel
from typing import List


class Storyboard(BaseModel):
    title: str
    author: str
    frames: List = []

    def to_dict(self) -> dict:
        return dict(title=self.title, author=self.author, frames=self.frames)
