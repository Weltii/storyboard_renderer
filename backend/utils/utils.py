import os

from backend.config import output_path


class CustomFileExistsError(FileExistsError):
    path: str


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
