from src.intelligence.planner_schema import (
    AnalysisPlan,
)


ALLOWED_OPERATIONS = {
    "summarize_sentiment":
        "Return high-level sentiment distribution.",

    "rank_priority_issues":
        "Return business issues ranked by deterministic priority score.",

    "summarize_themes":
        "Return the most frequently detected customer themes.",

    "filter_negative_themes":
        "Return themes with the strongest negative sentiment.",

    "filter_positive_themes":
        "Return themes with the strongest positive sentiment.",

    "summarize_uncertainty":
        "Return uncertainty rate and average model confidence.",
}


PLANNER_SYSTEM_PROMPT = """
You are a constrained analytics planner for a
customer-review intelligence system.

Your ONLY job is to translate the user's business
question into an AnalysisPlan.

You do NOT analyze customer data.
You do NOT calculate statistics.
You do NOT provide explanations or recommendations.

You may only use these operation names:

- summarize_sentiment
- rank_priority_issues
- summarize_themes
- filter_negative_themes
- filter_positive_themes
- summarize_uncertainty

Your response MUST match exactly this JSON structure:

{
  "intent": "short_machine_readable_intent",
  "operations": [
    {
      "operation": "one_allowed_operation_name",
      "limit": 5
    }
  ]
}

Rules:

- Return one JSON object only.
- Do not wrap the JSON in another object.
- Do not use "analysis_plan".
- Do not use "steps".
- Do not include "purpose".
- Do not include "notes".
- Do not include "excluded_operations".
- Do not include explanations.
- Do not include Markdown.
- Do not include ```json code fences.
- "limit" may be an integer or null.
- Every operation must come from the allowed list.
- Never request raw reviews.
- Never request customer records.
- Never request personal information.
- Never request file access.
- Never request arbitrary code execution.
- Never request shell commands.

The local Python analytics engine performs all
calculations after your plan is validated.
""".strip()


def build_planner_context(
    user_question: str,
) -> dict:
    """
    Build the privacy-safe context that will later
    be sent to the LLM planner.

    No review data or InsightPacket is included.
    """

    if not isinstance(
        user_question,
        str,
    ):
        raise TypeError(
            "user_question must be a string"
        )

    question = user_question.strip()

    if not question:
        raise ValueError(
            "user_question must not be empty"
        )

    return {
        "user_question": question,

        "allowed_operations": (
            ALLOWED_OPERATIONS
        ),
    }


def parse_planner_response(
    response_data: dict,
) -> AnalysisPlan:
    """
    Validate a planner response against the strict
    AnalysisPlan schema.

    Unsupported operation names are rejected by
    Pydantic.
    """

    if not isinstance(
        response_data,
        dict,
    ):
        raise TypeError(
            "response_data must be a dictionary"
        )

    return AnalysisPlan.model_validate(
        response_data
    )