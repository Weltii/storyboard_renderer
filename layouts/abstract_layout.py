from abc import ABC, abstractmethod

from storyboard import Storyboard


class TemplateNotFound(Exception):
	pass


class AbstractLayout(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def generate_file(self, storyboard: Storyboard):
		pass

	@staticmethod
	@abstractmethod
	def get_required_frame_data() -> dict:
		pass
