import os

from statics import output_directory


def save_tex_file(file_name: str, content: str):
	if not os.path.exists(output_directory):
		os.mkdir(output_directory)
	write_file(os.path.join(output_directory, file_name), content)


def write_file(path: str, content: str):
	file = open(path, "w")
	file.write(content)
	file.close()
