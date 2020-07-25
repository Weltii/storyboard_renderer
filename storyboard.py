from pydantic import BaseModel
from typing import List


class Storyboard(BaseModel):
    title: str
    author: str
    frames: List[dict]

    def to_dict(self):
        return dict(
            title=self.title,
            author=self.author,
            frames=self.frames
        )