import pytest

from src.intelligence.prioritization import (
    calculate_priority_issues,
)
from src.intelligence.schemas import (
    ThemeStatistics,
)


def test_calculate_priority_issues():
    themes = [
        ThemeStatistics(
            theme="performance",
            total_mentions=20,
            positive_mentions=2,
            neutral_mentions=2,
            negative_mentions=16,
            positive_rate=0.10,
            neutral_rate=0.10,
            negative_rate=0.80,
        ),
        ThemeStatistics(
            theme="crashes",
            total_mentions=5,
            positive_mentions=0,
            neutral_mentions=0,
            negative_mentions=5,
            positive_rate=0.0,
            neutral_rate=0.0,
            negative_rate=1.0,
        ),
        ThemeStatistics(
            theme="ui_ux",
            total_mentions=50,
            positive_mentions=45,
            neutral_mentions=2,
            negative_mentions=3,
            positive_rate=0.90,
            neutral_rate=0.04,
            negative_rate=0.06,
        ),
    ]

    issues = calculate_priority_issues(
        theme_statistics=themes,
        total_reviews=100,
    )

    assert len(issues) == 3

    assert issues[0].theme == "performance"
    assert issues[1].theme == "crashes"
    assert issues[2].theme == "ui_ux"


def test_priority_score_calculation():
    themes = [
        ThemeStatistics(
            theme="performance",
            total_mentions=20,
            positive_mentions=2,
            neutral_mentions=2,
            negative_mentions=16,
            positive_rate=0.10,
            neutral_rate=0.10,
            negative_rate=0.80,
        )
    ]

    issues = calculate_priority_issues(
        theme_statistics=themes,
        total_reviews=100,
    )

    issue = issues[0]

    assert issue.frequency_share == pytest.approx(
        0.20
    )

    assert issue.negative_rate == pytest.approx(
        0.80
    )

    assert issue.priority_score == pytest.approx(
        0.16
    )


def test_more_negative_theme_can_rank_higher():
    themes = [
        ThemeStatistics(
            theme="theme_a",
            total_mentions=10,
            positive_mentions=0,
            neutral_mentions=0,
            negative_mentions=10,
            positive_rate=0.0,
            neutral_rate=0.0,
            negative_rate=1.0,
        ),
        ThemeStatistics(
            theme="theme_b",
            total_mentions=10,
            positive_mentions=5,
            neutral_mentions=0,
            negative_mentions=5,
            positive_rate=0.5,
            neutral_rate=0.0,
            negative_rate=0.5,
        ),
    ]

    issues = calculate_priority_issues(
        theme_statistics=themes,
        total_reviews=100,
    )

    assert issues[0].theme == "theme_a"
    assert issues[1].theme == "theme_b"


def test_higher_frequency_can_rank_higher():
    themes = [
        ThemeStatistics(
            theme="large_issue",
            total_mentions=40,
            positive_mentions=8,
            neutral_mentions=0,
            negative_mentions=32,
            positive_rate=0.20,
            neutral_rate=0.0,
            negative_rate=0.80,
        ),
        ThemeStatistics(
            theme="small_issue",
            total_mentions=5,
            positive_mentions=0,
            neutral_mentions=0,
            negative_mentions=5,
            positive_rate=0.0,
            neutral_rate=0.0,
            negative_rate=1.0,
        ),
    ]

    issues = calculate_priority_issues(
        theme_statistics=themes,
        total_reviews=100,
    )

    assert issues[0].theme == "large_issue"
    assert issues[1].theme == "small_issue"


def test_empty_theme_list_returns_empty_list():
    issues = calculate_priority_issues(
        theme_statistics=[],
        total_reviews=100,
    )

    assert issues == []


def test_invalid_total_reviews_rejected():
    with pytest.raises(ValueError):
        calculate_priority_issues(
            theme_statistics=[],
            total_reviews=0,
        )


def test_non_list_theme_statistics_rejected():
    with pytest.raises(TypeError):
        calculate_priority_issues(
            theme_statistics="invalid",
            total_reviews=100,
        )