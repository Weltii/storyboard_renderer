import subprocess


def compile_latex(path: str, input_file: str):
	cmd = [f"lualatex", f"-output-directory={path}", "-interaction=nonstopmode", f"{path}{input_file}"]
	result = subprocess.run(cmd, stdout=subprocess.PIPE)

if __name__ == '__main__':
	compile_latex("./layouts/test/", "test.tex")
