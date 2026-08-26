import json
from typing import Any

from src.intelligence.claude_client import (
    DEFAULT_CLAUDE_MODEL,
)
from src.intelligence.planner import (
    PLANNER_SYSTEM_PROMPT,
    build_planner_context,
    parse_planner_response,
)
from src.intelligence.planner_schema import (
    AnalysisPlan,
)

def _clean_json_response(
    response_text: str,
) -> str:
    """
    Remove common Markdown code fences from
    Claude JSON responses.

    This does not change the JSON structure.
    It only removes presentation formatting.
    """

    cleaned = response_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[
            len("```json"):
        ]

    elif cleaned.startswith("```"):
        cleaned = cleaned[
            len("```"):
        ]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()

def generate_analysis_plan(
    user_question: str,
    client: Any,
    model: str = DEFAULT_CLAUDE_MODEL,
) -> AnalysisPlan:
    """
    Ask Claude to translate a business question
    into a constrained, validated AnalysisPlan.

    The client is injected so tests can use a fake
    client without making real API requests.
    """

    context = build_planner_context(
        user_question
    )

    user_payload = json.dumps(
        context,
        indent=2,
    )

    response = client.messages.create(
        model=model,
        max_tokens=500,
        system=PLANNER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Create an analysis plan for "
                    "the following request.\n\n"
                    f"{user_payload}\n\n"
                    "Return JSON only."
                ),
            }
        ],
    )
    usage = getattr(
    response,
    "usage",
    None,
    )

    if usage is not None:
        print(
            "Planner token usage:",
            "input=",
            getattr(
                usage,
                "input_tokens",
                None,
            ),
            "output=",
            getattr(
                usage,
                "output_tokens",
                None,
            ),
        )

    if not response.content:
        raise RuntimeError(
            "Claude returned an empty response"
        )

    response_text = (
        response.content[0].text
    )

    response_text = _clean_json_response(
    response_text
    )


    try:
        response_data = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Claude returned invalid JSON"
        ) from error

    return parse_planner_response(
        response_data
    )


