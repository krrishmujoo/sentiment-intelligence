from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api import app


PROJECT_ROOT = Path(__file__).resolve().parent

FRONTEND_DIR = (
    PROJECT_ROOT
    / "frontend"
)

FRONTEND_PATH = (
    FRONTEND_DIR
    / "index.html"
)


app.mount(
    "/frontend",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="frontend",
)


@app.get(
    "/",
    include_in_schema=False,
)
def frontend():
    """
    Serve the sentiment analyzer web interface.
    """

    if not FRONTEND_PATH.exists():

        raise FileNotFoundError(
            f"Frontend file was not found: {FRONTEND_PATH}"
        )

    return FileResponse(
        FRONTEND_PATH
    )