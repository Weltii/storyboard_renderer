from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/storyboard/")
def render_json(payload: str):
    j = json.loads(payload)
    print(j["t"])
    return {"message": "Auftrag angenommen"}
