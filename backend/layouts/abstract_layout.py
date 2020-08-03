from abc import ABC, abstractmethod

from backend.classes.project import Project


class AbstractLayout(ABC):
    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @staticmethod
    @abstractmethod
    def get_description():
        pass

    @staticmethod
    @abstractmethod
    def generate_file_string(project: Project):
        pass

    @staticmethod
    @abstractmethod
    def get_required_frame_data() -> dict:
        """
        Returns a dict with data_name = type of the data
        Example: dict(
                image=str
                image_description=str
                focal_length=int
            )
        :return:
        """
        pass
