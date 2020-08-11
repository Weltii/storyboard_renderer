import json
import os
from shutil import copyfile
from typing import List, Any

from pydantic import BaseModel

from backend.classes.storyboard import Storyboard
from backend.config import supported_image_types, sample_data_path
from backend.utils.utils import (
    load_file_as_string,
    generate_file_hash,
    StoryboardFileNotFound,
    InvalidStoryboard,
    DirectoryIsNotEmpty,
    get_directory_of_file,
    write_file,
)


class Project(BaseModel):
    path: str
    storyboard: Storyboard
    image_hashes: List[dict] = None
    images_directory: str = None
    output_directory: str = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.image_hashes = []
        self.images_directory = os.path.join(self.path, "images/")
        self.generate_image_hashes()
        self.output_directory = os.path.join(self.path, "output/")

    def generate_image_hashes(self):
        if not os.path.exists(self.images_directory):
            os.mkdir(self.images_directory)
        else:
            for file in os.listdir(self.images_directory):
                info = generate_file_hash(os.path.join(self.images_directory, file))
                if info["file_type"] in supported_image_types:
                    self.image_hashes.append(info)

    def save_project(self):
        if self.storyboard:
            write_file(
                os.path.join(self.path, "storyboard.json"),
                json.dumps(self.storyboard.to_dict(), indent=2),
            )

    @staticmethod
    def load_from_path(path: str):
        if not os.path.exists(path):
            raise FileNotFoundError

        storyboard: Storyboard

        if os.path.isdir(path):
            tmp_storyboard_path = os.path.join(path, "storyboard.json")
            if not os.path.exists(tmp_storyboard_path):
                raise StoryboardFileNotFound(
                    f"No storyboard file found in {tmp_storyboard_path}."
                    f"Please create a new project or try another path."
                )
            storyboard_path = tmp_storyboard_path
        else:
            storyboard_path = path
            path = get_directory_of_file(path)

        file_type = os.path.splitext(storyboard_path)[1]
        if file_type == ".json":
            file_string = load_file_as_string(storyboard_path)
            file_json = json.loads(file_string)
            if not Storyboard.is_valid_storyboard_dict(file_json):
                raise InvalidStoryboard(
                    f"The chosen storyboard is not valid, please check, that all required attributes are set!"
                )
        else:
            raise StoryboardFileNotFound(
                f"Storyboard file if from type {file_type}, "
                f"instead of .json. Please check that the file has the ending .json and is a valid storyboard file!"
            )

        storyboard: Storyboard = Storyboard.generate_from_file(storyboard_path)
        return Project(path=path, storyboard=storyboard)

    @staticmethod
    def generate_new_project(path: str):
        if not os.path.exists(path) or len(os.listdir(path)) is not 0:
            raise DirectoryIsNotEmpty(
                f"The directory {path} is not empty or does not exists! "
                f"Please create an empty directory for the project."
            )

        storyboard_path = os.path.join(path, "storyboard.json")
        image_path = os.path.join(path, "images")
        output_path = os.path.join(path, "output")
        if not os.path.exists(storyboard_path):
            copyfile(
                os.path.join(sample_data_path, "sample_storyboard.json"),
                storyboard_path,
            )

        os.mkdir(output_path)
        os.mkdir(image_path)

        storyboard: Storyboard = Storyboard.generate_from_file(storyboard_path)
        project = Project(path=path, storyboard=storyboard)
        for image in ["sample_image.jpg", "sample_image_2.png"]:
            print(os.path.join(sample_data_path, image))
            print(project.images_directory)
            copyfile(
                os.path.join(sample_data_path, image),
                os.path.join(
                    image_path, image
                ),  # add here the path to copy and image! Need for the default project.
            )
        return project
