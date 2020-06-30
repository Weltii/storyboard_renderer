from typing import List


class MissingDataInFrame:
	def __init__(self, frame_number: int):
		self.frame_number = frame_number
		self.missing_data = []

	def add_missing_data(self, data_name: str):
		self.missing_data.append(data_name)

	def has_missing_data(self):
		return len(self.missing_data) > 0


class MissingData:
	def __init__(self):
		self.missing_data = []

	def has_missing_data(self):
		return len(self.missing_data) > 0

	def add_missing_data(self, missing_data: MissingDataInFrame):
		self.missing_data.append(missing_data)
