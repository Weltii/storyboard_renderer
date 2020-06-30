import uvicorn
from fastapi import FastAPI
from layout_bridge import compile_layout
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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


@app.get("/storyboard/")
def render_json(payload: str):
    j = json.loads(payload)
    path = compile_layout("movie", j)
    return {"path": path}


app.mount("/web", StaticFiles(directory="web"), name="web")

app.mount("/output", StaticFiles(directory="output"), name="pdf-output")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
