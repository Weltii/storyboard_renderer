import os
import unittest

from backend.classes.render_job import Job
from backend.classes.steps.generate_tex_file_step import GenerateTexFileStep
from backend.classes.storyboard import Storyboard
from backend.config import output_path, sample_data_path
from backend.sample_data.sample_generator import (
    generate_sample_project,
    remove_sample_project,
)
from backend.utils.enums import LayoutName, Status
from backend.utils.utils import write_file, load_file_as_string

sample_image_path = os.path.join(sample_data_path, "sample_image.jpg")
storyboard = Storyboard(
    title="test title", author="Bernhard Brueckenpfeiler", frames=[]
)
expected_file_content = """\\documentclass[10pt]{scrreprt}
\\usepackage[
	a4paper,
	margin=2cm
]{geometry}
\\usepackage{graphicx}
\\usepackage[german]{babel}
\\usepackage[utf8]{inputenc}
\\usepackage{fancyhdr}
\\usepackage{csquotes}
%\\usepackage{fontspec}

\\graphicspath{%*imagepath*}

% \\setmainfont{Courier}

% Define here your author and title!
\\renewcommand{\\title}{
	ExampleTitle
}
\\renewcommand{\\author}{
	Bernhard Brückenpfeiler
}

% Defines a frame of the storyboard
% #1 \\storyboardFrameHeader
% #2 \\storyboardContent
% #3 \\storyboardFooter
\\newcommand{\\storyboardFrame}[2]{
	\\vspace{1cm}
	\\begin{tabular}{p{.4\\textwidth} p{.6\\textwidth}}
		\\begin{minipage}[t]{.4\\textwidth}
			\\vspace{-\\ht\\strutbox}\\includegraphics[width=\\textwidth]{#1}
		\\end{minipage} &
		\\begin{minipage}[t]{.5\\textwidth}
			#2
		\\end{minipage}
	\\end{tabular}

}

% Defines a page of two storyboards
% #1 \\storyboardFrame
% #2 \\storyboardFrame2
\\newcommand{\\storyboardPage}[5]{
	#1
	#2
	#3
	#4
	#5
	\\vspace{\\fill}
	\\pagebreak
}

\\pagestyle{fancy}
\\fancyhf{}
\\lhead{Filmprojekt \\enquote{\\title}}
\\lfoot{\\author - Stand \\today}
\\rfoot{Seite \\thepage}

\\begin{document}
% example
%\\storyboardPage
%	{
%		\\storyboardFrame{example_image.png}{Text}
%	}
%	{
%		\\storyboardFrame{example_image.png}{Text 2}
%	}
%	{
%		\\storyboardFrame{example_image.png}{Text}
%	}
%	{
%		\\storyboardFrame{example_image.png}{Text 2}
%	}
%	{
%		\\storyboardFrame{example_image.png}{Text 2}
%	}

% the next line will be replaced
\\storyboardPage
	{\storyboardFrame{./sample_image.jpg}{Beschreibung des Bildes}}
	{\storyboardFrame{./sample_image.jpg}{Beschreibung des Bildes}}
	{}
	{}
	{}

\\end{document}"""


def get_tex_file_name(title: str):
    return f"{title}.tex".replace(" ", "_")


def clear_output_directory(job: Job):
    remove_sample_project(job.project.path)


class TestGenerateTexFileStep(unittest.TestCase):
    def test_run_valid(self):
        GenerateTexFileStep.get_file_name = get_tex_file_name
        job = Job(
            layout=LayoutName.EASY_LAYOUT.value, project=generate_sample_project()
        )
        GenerateTexFileStep.run(job)
        expected_tex_file_path = os.path.join(
            job.project.output_directory,
            get_tex_file_name(job.project.storyboard.title),
        )

        self.assertEqual(job.status, Status.VALID)
        self.assertTrue(os.path.exists(job.tex_file_path))

        file_content = load_file_as_string(job.tex_file_path)
        self.assertEqual(job.tex_file_path, expected_tex_file_path)
        self.assertEqual(
            file_content,
            expected_file_content.replace("%*imagepath*", job.project.images_directory),
        )
        clear_output_directory(job)

    def test_run_file_already_exists(self):
        GenerateTexFileStep.get_file_name = get_tex_file_name
        job = Job(
            layout=LayoutName.EASY_LAYOUT.value, project=generate_sample_project()
        )
        for x in range(2):
            job.project.storyboard.frames.append(
                dict(image=sample_image_path, image_description="image_description")
            )
        tex_file_path = os.path.join(
            job.project.output_directory,
            get_tex_file_name(job.project.storyboard.title),
        )
        write_file(tex_file_path, "nothing special")
        GenerateTexFileStep.run(job)
        self.assertEqual(job.status, Status.GENERATE_TEX_ERROR)
        self.assertEqual(
            job.status_data["message"],
            f"Cannot save the .tex file, path {tex_file_path} already exists",
        )
        clear_output_directory(job)


if __name__ == "__main__":
    unittest.main()
