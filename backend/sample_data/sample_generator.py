import os
from datetime import datetime
from shutil import rmtree

from backend.classes.project import Project


def generate_sample_project(path: str = None):
    if not path:
        path = (
            f"/tmp/sample_project_{str(datetime.now().timestamp()).replace('.', '_')}"
        )
        os.mkdir(path)
    return Project.generate_new_project(path)


def remove_project(path: str):
    if os.path.exists(path):
        rmtree(path)
