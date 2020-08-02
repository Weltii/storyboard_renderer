import os
import re

from backend.config import output_path
from PIL import Image
import imagehash


class CustomFileExistsError(FileExistsError):
    path: str


class StoryboardFileNotFound(Exception):
    message: str

    def __init__(self, message):
        self.message = message


class InvalidStoryboard(Exception):
    message: str

    def __init__(self, message):
        self.message = message


class DirectoryIsNotEmpty(Exception):
    message: str

    def __init__(self, message):
        self.message = message


def load_file_as_string(path: str) -> str:
    """
    Returns the specified file as a string
    :param path:
    :return: str
    """
    if not os.path.exists(path):
        raise FileNotFoundError
    f = open(path)
    string = f.read().strip()
    f.close()
    return string


def save_tex_file(file_name: str, content: str):
    """
    Save a .tex file with the specified file_name and the specified content.
    Returns the path of saved file
    :param file_name:
    :param content:
    :return: str
    """
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    path = os.path.join(output_path, file_name)
    if os.path.exists(path):
        exception = CustomFileExistsError()
        exception.path = path
        raise exception
    write_file(path, content)
    return path


def write_file(path: str, content: str):
    """
    Saves a file to the specified path, with the specified content
    :param path:
    :param content:
    :return: void
    """
    file = open(path, "w")
    file.write(content)
    file.close()


def base64_image_add_type(base64_string: str, image_type: str):
    """
    Add the image type information to the base64 encoded string
    :param base64_string:
    :param image_type:
    :return:
    """
    image_type = image_type.replace(".", "")
    return f"data:image/{image_type};base64,{base64_string}"


def remove_base64_info(base64_string: str):
    """
    Removes the base64 type information.
    :param base64_string:
    :return:
    """
    return re.split("data:\w+\/\w+;base64,", base64_string)[1]


def generate_file_hash(file_path: str) -> dict:
    """
    Generates a file hash
    :param file_path:
    :return: dict(file_type=.txt, hash=123456789, filename="file"
    """
    img = Image.open(file_path)
    file_name, file_type = os.path.splitext(file_path)
    split = file_name.split("/")
    file_name = split[len(split) - 1]
    info = dict(
        file_type=file_type, hash=str(imagehash.whash(img)), file_name=file_name
    )
    return info


def get_directory_of_file(file_path: str):
    index = file_path.rfind("/")
    return file_path[:index]
