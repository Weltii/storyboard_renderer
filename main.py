import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from backend.fast_api import add_endpoints


def init() -> FastAPI:
    app = FastAPI()

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

    app.mount("/web", StaticFiles(directory="web"), name="web")

    add_endpoints(app)

    return app


fast_api = init()


if __name__ == "__main__":
    uvicorn.run("main:fast_api", host="0.0.0.0", port=8000, reload=True)
