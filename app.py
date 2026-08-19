from pathlib import Path

from fastapi.responses import FileResponse

from src.api import app


PROJECT_ROOT = Path(__file__).resolve().parent

FRONTEND_PATH = (
    PROJECT_ROOT
    / "frontend"
    / "index.html"
)


@app.get("/", include_in_schema=False)
def frontend():
    """
    Serve the sentiment analyzer web interface.
    """

    if not FRONTEND_PATH.exists():
        raise FileNotFoundError(
            f"Frontend file was not found: {FRONTEND_PATH}"
        )

    return FileResponse(FRONTEND_PATH)