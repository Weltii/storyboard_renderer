import os

from fastapi import FastAPI, Response
import json

from starlette.staticfiles import StaticFiles

from backend.classes.render_job import Job
from backend.classes.storyboard import Storyboard
from backend.config import output_path
from backend.job_worker import JobWorker
from backend.layouts.Layouts import Layouts
from backend.utils.enums import LayoutName


def init():
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def add_endpoints(app: FastAPI):
    init()
    render_job_worker = JobWorker()

    @app.post("/storyboard/")
    async def render_json(storyboard: Storyboard):
        # storyboard = json.loads(payload)
        render_job = Job(layout=LayoutName.EASY_LAYOUT.value, storyboard=storyboard)
        render_job_worker.run_job(render_job)
        d = render_job.to_dict()
        return Response(content=json.dumps(d), media_type="application/json")

    @app.get("/layouts/")
    async def layouts():
        keys = []
        for key in LayoutName.get_all().keys():
            keys.append(key)
        return Response(content=json.dumps(keys), media_type="application/json")

    @app.get("/layouts/{layout_name}")
    async def layout(layout_name: str):
        if hasattr(LayoutName, layout_name):
            l = getattr(Layouts, getattr(LayoutName, layout_name).value).value
            required_data = l.get_required_frame_data()
            for key in required_data:
                required_data[key] = required_data[key].__name__
            dump = json.dumps(dict(required_frame_data=required_data))
            return Response(content=dump, media_type="application/json",)

    app.mount("/output", StaticFiles(directory=output_path), name="pdf-output")
