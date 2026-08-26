from typing import Any

from src.intelligence.analytics import (
    calculate_batch_analytics,
)
from src.intelligence.claude_insight import (
    generate_business_insights,
)
from src.intelligence.claude_planner import (
    generate_analysis_plan,
)
from src.intelligence.insight_packet import (
    build_insight_packet,
)
from src.intelligence.planner_executor import (
    execute_plan,
)


def analyze_business_question(
    user_question: str,
    predictions: list[dict],
    client: Any,
) -> dict:
    """
    Run the complete privacy-safe intelligence pipeline.

    Flow:
    predictions
        -> local analytics
        -> privacy-safe InsightPacket
        -> Claude planner
        -> local executor
        -> Claude business insights

    Raw review text is used only by the local analytics
    layer and is never sent to Claude.
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
        predictions,
        list,
    ):
        raise TypeError(
            "predictions must be a list"
        )

    if not predictions:
        raise ValueError(
            "predictions cannot be empty"
        )

    # 1. Local deterministic analytics.
    analytics_summary = (
        calculate_batch_analytics(
            predictions
        )
    )

    # 2. Remove raw review text and create
    #    privacy-safe aggregate representation.
    insight_packet = (
        build_insight_packet(
            analytics_summary
        )
    )

    # 3. Claude sees only the business question
    #    and allowed planner operations.
    plan = generate_analysis_plan(
        user_question,
        client=client,
    )

    # 4. Python executes the validated plan
    #    against the privacy-safe packet.
    execution_result = execute_plan(
        plan,
        insight_packet,
    )

    # 5. Claude receives only safe deterministic
    #    facts and produces business interpretation.
    insights = generate_business_insights(
        user_question,
        execution_result,
        client=client,
    )

    return {
        "question": user_question,
        "plan": plan.model_dump(),
        "analytics": (
            insight_packet.model_dump()
        ),
        "execution": execution_result,
        "insights": insights.model_dump(),
    }