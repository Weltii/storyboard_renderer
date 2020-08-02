import os
from layouts.abstract_layout import AbstractLayout, TemplateNotFound
from storyboard import Storyboard


class MovieLayout(AbstractLayout):
	template_file_path = ""

	def __init__(self):
		super().__init__()
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

	@staticmethod
	def get_required_frame_data() -> dict:
		return dict(
			scene=str,
			setting=str,
			section=str,
			timecode=str,
			image=str,
			image_description=str,
			audio_description=str,
			setting_size=str,
			perspective=str,
			focal_length=int,
			camera_movement=str,
			camera_support=str,
			fx=str
		)

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

	def generate_frames(self, storyboard: Storyboard):
		frames = storyboard.frames
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

	def generate_file(self, storyboard: Storyboard):
		try:
			f = open(self.template_file_path)
		except FileNotFoundError:
			raise TemplateNotFound

		template = f.read().strip()
		template = template.replace("%*title*", storyboard["title"])
		template = template.replace("%*author*", storyboard["author"])
		template = template.replace("%*frames*", self.generate_frames(storyboard))

		# maybe add a i18n translation feature?
		return template
