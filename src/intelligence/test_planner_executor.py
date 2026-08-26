import pytest

from src.intelligence.analytics import (
    calculate_batch_analytics,
)
from src.intelligence.insight_packet import (
    build_insight_packet,
)
from src.intelligence.planner_executor import (
    execute_operation,
    execute_plan,
)
from src.intelligence.planner_schema import (
    AnalysisPlan,
    PlannerOperation,
)


def _make_packet():
    predictions = [
        {
            "review": "The app crashes and is slow.",
            "sentiment": "negative",
            "confidence": 0.88,
            "prediction_margin": 0.62,
            "is_uncertain": False,
        },
        {
            "review": "Login is slow.",
            "sentiment": "negative",
            "confidence": 0.77,
            "prediction_margin": 0.40,
            "is_uncertain": False,
        },
        {
            "review": "Performance is excellent.",
            "sentiment": "positive",
            "confidence": 0.91,
            "prediction_margin": 0.72,
            "is_uncertain": False,
        },
    ]

    summary = calculate_batch_analytics(
        predictions
    )

    return build_insight_packet(
        summary
    )


def test_execute_sentiment_summary():
    packet = _make_packet()

    operation = PlannerOperation(
        operation="summarize_sentiment"
    )

    result = execute_operation(
        operation,
        packet,
    )

    assert (
        result["operation"]
        == "summarize_sentiment"
    )

    assert (
        result["result"]["total_reviews"]
        == 3
    )

    assert (
        result["result"]["negative_rate"]
        == pytest.approx(2 / 3)
    )


def test_execute_priority_ranking():
    packet = _make_packet()

    operation = PlannerOperation(
        operation="rank_priority_issues",
        limit=2,
    )

    result = execute_operation(
        operation,
        packet,
    )

    issues = result["result"]

    assert len(issues) == 2
    assert issues[0]["theme"] == "performance"
    assert issues[1]["theme"] == "crashes"


def test_execute_negative_theme_filter():
    packet = _make_packet()

    operation = PlannerOperation(
        operation="filter_negative_themes",
        limit=2,
    )

    result = execute_operation(
        operation,
        packet,
    )

    themes = result["result"]

    assert len(themes) == 2

    assert (
        themes[0]["negative_rate"]
        >= themes[1]["negative_rate"]
    )


def test_execute_positive_theme_filter():
    packet = _make_packet()

    operation = PlannerOperation(
        operation="filter_positive_themes",
        limit=2,
    )

    result = execute_operation(
        operation,
        packet,
    )

    themes = result["result"]

    assert len(themes) == 2

    assert (
        themes[0]["positive_rate"]
        >= themes[1]["positive_rate"]
    )


def test_execute_uncertainty_summary():
    packet = _make_packet()

    operation = PlannerOperation(
        operation="summarize_uncertainty"
    )

    result = execute_operation(
        operation,
        packet,
    )

    assert (
        result["result"]["uncertainty_rate"]
        == pytest.approx(0.0)
    )

    assert (
        result["result"]["average_confidence"]
        == pytest.approx(
            0.8533333333333334
        )
    )


def test_execute_complete_plan():
    packet = _make_packet()

    plan = AnalysisPlan(
        intent="identify_customer_problems",
        operations=[
            PlannerOperation(
                operation="rank_priority_issues",
                limit=3,
            ),
            PlannerOperation(
                operation="summarize_uncertainty",
            ),
        ],
    )

    result = execute_plan(
        plan,
        packet,
    )

    assert (
        result["intent"]
        == "identify_customer_problems"
    )

    assert len(
        result["results"]
    ) == 2

    assert (
        result["results"][0]["operation"]
        == "rank_priority_issues"
    )

    assert (
        result["results"][1]["operation"]
        == "summarize_uncertainty"
    )


def test_execute_plan_rejects_invalid_plan():
    packet = _make_packet()

    with pytest.raises(TypeError):
        execute_plan(
            "not a plan",
            packet,
        )


def test_execute_plan_rejects_invalid_packet():
    plan = AnalysisPlan(
        intent="test",
        operations=[
            PlannerOperation(
                operation="summarize_sentiment"
            )
        ],
    )

    with pytest.raises(TypeError):
        execute_plan(
            plan,
            "not a packet",
        )