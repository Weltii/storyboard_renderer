import os
from abc import ABC, abstractmethod

from utils.missing_data import MissingData, MissingDataInFrame


class AbstractLayout(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def generate_file(self, storyboard: dict):
		pass

	@abstractmethod
	def get_required_frame_data(self):
		pass

	def check_frames(self, frames: list):
		required_data = self.get_required_frame_data()
		missing_data = MissingData()
		for c in range(len(frames)):
			frame = frames[c]
			missing_data_frame = MissingDataInFrame(c)
			for data in required_data:
				if data not in frame:
					missing_data_frame.add_missing_data(data)
			if missing_data_frame.has_missing_data():
				missing_data.add_missing_data(missing_data_frame)
		return missing_data

	def save_file(self, path: str, name: str, string: str):
		file = open(os.path.join(path, name), "w")
		file.write(string)
		file.close()
