import json
from typing import Any

from src.intelligence.claude_client import (
    DEFAULT_CLAUDE_MODEL,
)
from src.intelligence.insight_prompt import (
    INSIGHT_SYSTEM_PROMPT,
)
from src.intelligence.insight_schema import (
    BusinessInsightResponse,
)


def _clean_json_response(
    response_text: str,
) -> str:
    cleaned = response_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):]

    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```"):]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def generate_business_insights(
    user_question: str,
    execution_result: dict,
    client: Any,
    model: str = DEFAULT_CLAUDE_MODEL,
) -> BusinessInsightResponse:
    """
    Convert privacy-safe deterministic analytics
    results into validated business insights.

    Raw customer reviews must never be passed here.
    """

    if not isinstance(
        user_question,
        str,
    ):
        raise TypeError(
            "user_question must be a string"
        )

    if not user_question.strip():
        raise ValueError(
            "user_question cannot be empty"
        )

    if not isinstance(
        execution_result,
        dict,
    ):
        raise TypeError(
            "execution_result must be a dictionary"
        )

    payload = {
        "user_question": user_question,
        "analytics_result": execution_result,
    }

    user_payload = json.dumps(
        payload,
        indent=2,
    )

    response = client.messages.create(
        model=model,
        max_tokens=1800,
        system=INSIGHT_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    "Using only the following "
                    "privacy-safe analytics facts, "
                    "produce business insights and "
                    "recommendations.\n\n"
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
            "Insight token usage:",
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

    response_text = None

    for block in response.content:
        text = getattr(
            block,
            "text",
            None,
        )

        if text:
            response_text = text
            break

    if response_text is None:
        raise RuntimeError(
            "Claude returned no text response"
        )
    print("\nCLAUDE STOP REASON:")
    print(getattr(response, "stop_reason", None))

    print("\nRAW INSIGHT RESPONSE:")
    print(repr(response_text))

    response_text = _clean_json_response(
            response_text
        )
    if getattr(response, "stop_reason", None) == "max_tokens":
        raise RuntimeError(
            "Claude insight response was truncated "
            "because the output token limit was reached"
        )
    
    try:
        response_data = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Claude returned invalid JSON"
        ) from error

    return BusinessInsightResponse.model_validate(
        response_data
    )


