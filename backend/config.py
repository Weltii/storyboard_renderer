import os

# paths

base_path = os.path.dirname(__file__)
output_path = os.path.join(base_path, "output")
sample_data_path = os.path.join(base_path, "sample_data")

# latex settings

# latex path or terminal command
# I recommend luatex or pdftex
# If you wanna use lua code inside the templates, you need luatex!
latex_compiler = "luatex"
