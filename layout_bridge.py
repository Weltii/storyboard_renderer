import os

from bridge import compile_latex
from layouts.movie_layout import MovieLayout

layouts = dict(
	movie=MovieLayout()
)


def compile_layout(layout_name: str, storyboard: dict):
	layout: MovieLayout = layouts[layout_name]
	if layout:
		path = os.path.join(os.path.dirname(__file__), "output")
		file_name = "output_1.tex"
		layout.save_file(path, file_name, layout.generate_file(storyboard))
		compile_latex(path, file_name)


if __name__ == '__main__':
	compile_layout("movie", dict(
		title="Storyboard",
		author="Benjamin Krause",
		frames=[
			dict(
				scene="001",
				setting="002",
				section="001",
				timecode="0:00:00:01",
				image="./example_image.png",
				image_description="asdnasjkdlf h",
				audio_description="asdfa fdhajkdf hajdfkl",
				setting_size="Halb Nah",
				perspective="Vogel",
				focal_length="85",
				camera_movement="Statisch",
				camera_support="Stativ",
				fx="-"
			)
		]
	))
