import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from layout_bridge import compile_layout
import json


app = FastAPI()


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/")
def read_root():
    return generate_html_response()


@app.get("/storyboard/")
def render_json(payload: str):
    j = json.loads(payload)
    path = compile_layout("movie", j)
    return {"pdf_path": path}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
