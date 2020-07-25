import os

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json

from layouts.movie_layout import MovieLayout
from render_job import RenderJob
from render_job_worker import JobWorker
from storyboard import Storyboard

app = FastAPI()
render_job_worker = JobWorker()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return RedirectResponse("/web/dist/index.html")


@app.post("/storyboard/")
async def render_json(storyboard: Storyboard):
    # storyboard = json.loads(payload)
    render_job = RenderJob(MovieLayout, storyboard)
    render_job_worker.run_job(render_job)
    d = render_job.to_dict()
    return Response(content=json.dumps(d), media_type="application/json")


app.mount("/web", StaticFiles(directory="web"), name="web")

app.mount("/output", StaticFiles(directory="output"), name="pdf-output")

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "output")
    if not os.path.exists(path):
        os.makedirs(path)
    uvicorn.run(app, host="0.0.0.0", port=8000)
