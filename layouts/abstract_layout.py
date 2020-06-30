import os
from abc import ABC, abstractmethod


class AbstractLayout(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def generate_file(self, storyboard: dict):
		pass

	def save_file(self, path: str, name: str, string: str):
		file = open(os.path.join(path, name), "w")
		file.write(string)
		file.close()
