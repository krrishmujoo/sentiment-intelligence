from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api import app


PROJECT_ROOT = Path(__file__).resolve().parent

FRONTEND_DIST = (
    PROJECT_ROOT
    / "frontend"
    / "dist"
)

ASSETS_DIR = (
    FRONTEND_DIST
    / "assets"
)

INDEX_FILE = (
    FRONTEND_DIST
    / "index.html"
)


if ASSETS_DIR.exists():
    app.mount(
        "/assets",
        StaticFiles(
            directory=ASSETS_DIR
        ),
        name="assets",
    )


@app.get(
    "/",
    include_in_schema=False,
)
def frontend_root():
    """
    Serve the production React frontend.
    """

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Frontend build was not found: {INDEX_FILE}"
        )

    return FileResponse(
        INDEX_FILE
    )


@app.get(
    "/{full_path:path}",
    include_in_schema=False,
)
def frontend_spa_fallback(
    full_path: str,
):
    """
    Serve index.html for React client-side routes.

    Existing FastAPI routes such as /health,
    /predict, /predict-batch, and /analyze
    are matched before this fallback route.
    """

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Frontend build was not found: {INDEX_FILE}"
        )

    return FileResponse(
        INDEX_FILE
    )