def load_file_as_string(path: str) -> str:
    """
    Returns the specified file as a string
    :param path:
    :return: str
    """
    f = open(path)
    string = f.read().strip()
    f.close()
    return string
