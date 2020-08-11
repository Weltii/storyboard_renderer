import os
import base64

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import FileResponse
import json

from starlette.staticfiles import StaticFiles

from backend.classes.project import Project
from backend.classes.render_job import Job
from backend.classes.storyboard import Storyboard
from backend.config import output_path
from backend.job_worker import JobWorker
from backend.layouts.Layouts import Layouts
from backend.project_handler import ProjectHandler
from backend.utils.enums import LayoutName, Status
from backend.utils.utils import StoryboardFileNotFound, DirectoryIsNotEmpty


def init():
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def add_endpoints(app: FastAPI):
    init()
    render_job_worker = JobWorker()
    project_handler = ProjectHandler()

    @app.get("/project/current/", response_model=Project)
    def get_current_project():
        if project_handler.current_project:
            return project_handler.current_project
        raise HTTPException(
            status_code=404, detail="No project can be found, please load one!"
        )

    @app.get("/project/{path:path}/", response_model=Project)
    def load_project(path: str):
        try:
            project = project_handler.load_project(path)
            return project
        except StoryboardFileNotFound as e:
            raise HTTPException(detail=e.message, status_code=400)
        except FileNotFoundError:
            raise HTTPException(
                detail=f"Path: '{path}' cannot be found", status_code=404
            )

    @app.post("/project/{path:path}/", response_model=Project)
    def create_project(path: str):
        try:
            project = project_handler.create_new_project(path)
            return project
        except DirectoryIsNotEmpty as e:
            raise HTTPException(detail=e.message, status_code=400)
        except FileNotFoundError:
            raise HTTPException(
                detail=f"Path: '{path}' cannot be found", status_code=404
            )
        except:
            raise HTTPException(
                detail=f"Something went completly wrong!", status_code=500
            )

    @app.patch("/project/current/storyboard/", response_model=Job)
    def overwrite_storyboard(storyboard: Storyboard):
        project = project_handler.current_project
        if not project:
            raise HTTPException(
                status_code=404, detail="No project can be found, please load one!"
            )
        project.storyboard = storyboard
        job = Job(layout=LayoutName.EASY_LAYOUT.value, project=project)
        render_job_worker.run_job(job, JobWorker.validate_frames_step)
        if job.status is Status.VALID:
            project_handler.save_project(project)
        return job

    @app.patch("/project/close/current/")
    def close_project():
        project = project_handler.current_project
        if not project:
            raise HTTPException(
                status_code=404, detail="No project can be found, please load one!"
            )
        project.save_project()
        project_handler.close_project()
        return Response("Project successfully closed", status_code=200)

    @app.patch("/render_project/current/", response_model=Job)
    def render_project():
        if project_handler.current_project:
            job = Job(
                layout=LayoutName.EASY_LAYOUT.value,
                project=project_handler.current_project,
            )
            render_job_worker.run_job(job)
            return job
        else:
            raise HTTPException(
                detail=f"Before you can render a project, you must load a project!",
                status_code=404,
            )

    @app.get("/pdf/current/pdf/{path:path}/")
    def get_base64_pdf(path: str):
        if os.path.exists(path) and os.path.splitext(path)[1] == ".pdf":
            with open(path, "rb") as pdf:
                base64_string = str(base64.b64encode(pdf.read()))
                base64_string = base64_string[2:]
                base64_string = base64_string[:-1]
                result = f"data:application/pdf;base64,{base64_string}"
            return Response(json.dumps(dict(
                pdf=result
            )), status_code=200)

        return Response(json.dumps(dict(
            message=f"The path {path} is incorrect. Please check that it is a valid .pdf file!"
        )), status_code=404)


    @app.get("/layouts/")
    def layouts():
        keys = []
        for key in LayoutName.get_all().keys():
            keys.append(key)
        return Response(content=json.dumps(keys), media_type="application/json")

    @app.get("/layouts/{layout_name}")
    def layout(layout_name: str):
        if hasattr(LayoutName, layout_name):
            l = getattr(Layouts, getattr(LayoutName, layout_name).value).value
            required_data = l.get_required_frame_data()
            for key in required_data:
                required_data[key] = required_data[key].__name__
            dump = json.dumps(dict(required_frame_data=required_data))
            return Response(content=dump, media_type="application/json",)

    app.mount("/output", StaticFiles(directory=output_path), name="pdf-output")
