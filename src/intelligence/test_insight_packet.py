import pytest

from src.intelligence.analytics import (
    calculate_batch_analytics,
)
from src.intelligence.insight_packet import (
    build_insight_packet,
)


def _make_summary():
    predictions = [
        {
            "review": "The app crashes and is very slow.",
            "sentiment": "negative",
            "confidence": 0.88,
            "prediction_margin": 0.62,
            "is_uncertain": False,
        },
        {
            "review": "Login is slow and frustrating.",
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

    return calculate_batch_analytics(
        predictions
    )


def test_build_insight_packet():
    summary = _make_summary()

    packet = build_insight_packet(
        summary
    )

    assert packet.dataset.total_reviews == 3

    assert packet.dataset.positive_rate == pytest.approx(
        1 / 3
    )

    assert packet.dataset.negative_rate == pytest.approx(
        2 / 3
    )

    assert len(packet.themes) >= 1

    assert len(
        packet.priority_issues
    ) >= 1


def test_insight_packet_excludes_raw_review_text():
    """
    This is a critical privacy regression test.

    Raw customer reviews must not appear anywhere
    inside the default LLM insight packet.
    """

    summary = _make_summary()

    packet = build_insight_packet(
        summary
    )

    serialized = (
        packet.model_dump_json()
    )

    raw_reviews = [
        "The app crashes and is very slow.",
        "Login is slow and frustrating.",
        "Performance is excellent.",
    ]

    for review in raw_reviews:
        assert review not in serialized


def test_insight_packet_contains_only_expected_top_level_fields():
    """
    Prevent accidental expansion of the LLM payload
    with unsafe fields later.
    """

    summary = _make_summary()

    packet = build_insight_packet(
        summary
    )

    data = packet.model_dump()

    assert set(
        data.keys()
    ) == {
        "dataset",
        "themes",
        "priority_issues",
    }


def test_insight_packet_does_not_include_review_field():
    """
    Recursively verify that no field named 'review'
    exists anywhere in the packet.
    """

    summary = _make_summary()

    packet = build_insight_packet(
        summary
    )

    data = packet.model_dump()

    def contains_review_key(value):
        if isinstance(value, dict):
            if "review" in value:
                return True

            return any(
                contains_review_key(
                    nested_value
                )
                for nested_value in value.values()
            )

        if isinstance(value, list):
            return any(
                contains_review_key(
                    item
                )
                for item in value
            )

        return False

    assert (
        contains_review_key(data)
        is False
    )


def test_theme_limit_is_respected():
    summary = _make_summary()

    packet = build_insight_packet(
        summary,
        top_theme_limit=1,
    )

    assert len(
        packet.themes
    ) == 1


def test_priority_limit_is_respected():
    summary = _make_summary()

    packet = build_insight_packet(
        summary,
        top_priority_limit=1,
    )

    assert len(
        packet.priority_issues
    ) == 1


def test_invalid_theme_limit_rejected():
    summary = _make_summary()

    with pytest.raises(ValueError):
        build_insight_packet(
            summary,
            top_theme_limit=0,
        )


def test_invalid_priority_limit_rejected():
    summary = _make_summary()

    with pytest.raises(ValueError):
        build_insight_packet(
            summary,
            top_priority_limit=0,
        )


def test_invalid_summary_rejected():
    with pytest.raises(TypeError):
        build_insight_packet(
            "not a summary"
        )