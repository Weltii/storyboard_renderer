import os

# paths

base_path = os.path.dirname(__file__)
output_path = os.path.join(base_path, "output")
sample_data_path = os.path.join(base_path, "sample_data")

# latex settings

# latex path or terminal command
# I recommend lualatex or pdftex
# If you wanna use lua code inside the templates, you need lualatex!
latex_compiler = "lualatex"

supported_image_types = [".png", ".jpg", ".jpeg"]
