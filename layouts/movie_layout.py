import os
from layouts.abstract_layout import AbstractLayout


class MovieLayout(AbstractLayout):
	def __init__(self):
		dirname = os.path.dirname(__file__)
		self.template_file_path = os.path.join(dirname, "templates/movie_layout.tex")
		self.frame_layout = \
			"\n\t{\storyboardFrame" \
			"\n\t\t{\storyboardFrameHead" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t}" \
			"\n\t\t{\storyboardFrameContent" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t}" \
			"\n\t\t{\storyboardFrameFooter" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t\t{%s}" \
			"\n\t\t}" \
			"\n\t}"
		self.required_frame_data = [
			"scene",
			"setting",
			"section",
			"timecode",
			"image",
			"image_description",
			"audio_description",
			"setting_size",
			"perspective",
			"focal_length",
			"camera_movement",
			"camera_support",
			"fx"
		]

	def get_required_frame_data(self):
		return self.required_frame_data

	def generate_frame(self, frame: dict):
		if frame:
			return \
				self.frame_layout % (frame["scene"],
														 frame["setting"],
														 frame["section"],
														 frame["timecode"],
														 frame["image"],
														 frame["image_description"],
														 frame["audio_description"],
														 frame["setting_size"],
														 frame["perspective"],
														 frame["focal_length"],
														 frame["camera_movement"],
														 frame["camera_support"],
														 frame["fx"])
		else:
			return "\n\t{}"

	def generate_frames(self, storyboard: dict):
		frames = storyboard["frames"]
		frames_string = ""
		counter = 0
		if frames:
			for frame in frames:
				if counter % 2 == 0:
					frames_string += "\storyboardPage"
				frames_string += self.generate_frame(frame)
				counter += 1
			if len(frames) % 2 == 1:
				frames_string += self.generate_frame(None)
		return frames_string

	def generate_file(self, storyboard: dict):
		f = open(self.template_file_path)
		template = f.read().strip()
		template = template.replace("%*title*", storyboard["title"])
		template = template.replace("%*author*", storyboard["author"])
		template = template.replace("%*frames*", self.generate_frames(storyboard))
		return template

