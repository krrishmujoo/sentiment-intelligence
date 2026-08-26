import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)


DEFAULT_CLAUDE_MODEL = "claude-sonnet-5"


def get_anthropic_client() -> Anthropic:
    """
    Create an Anthropic client using the API key
    stored in the project's .env file.

    The API key is never hard-coded into source code.
    """

    api_key = os.getenv(
        "ANTHROPIC_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not configured"
        )

    return Anthropic(
        api_key=api_key
    )