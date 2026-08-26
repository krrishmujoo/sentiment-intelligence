import pytest
from src.intelligence.themes import (
    calculate_theme_counts,
    calculate_theme_statistics,
    extract_themes,
)
from src.intelligence.schemas import ReviewSignal
from src.intelligence.themes import (
    calculate_theme_counts,
    extract_themes,
)


def test_extract_single_theme():
    themes = extract_themes(
        "The app crashes constantly."
    )

    assert themes == [
        "crashes"
    ]


def test_extract_multiple_themes():
    themes = extract_themes(
        (
            "The interface looks great but "
            "checkout crashes constantly."
        )
    )

    assert "crashes" in themes
    assert "payments" in themes
    assert "ui_ux" in themes


def test_extract_themes_is_case_insensitive():
    themes = extract_themes(
        "LOGIN is very slow."
    )

    assert "login_authentication" in themes
    assert "performance" in themes


def test_review_can_have_no_known_theme():
    themes = extract_themes(
        "I really enjoyed using this app."
    )

    assert themes == []


def test_empty_review_is_rejected():
    with pytest.raises(ValueError):
        extract_themes("   ")


def test_non_string_review_is_rejected():
    with pytest.raises(TypeError):
        extract_themes(123)


def test_calculate_theme_counts():
    signals = [
        ReviewSignal(
            review=(
                "The app crashes and is slow."
            ),
            sentiment="negative",
            confidence=0.80,
            prediction_margin=0.50,
            is_uncertain=False,
        ),
        ReviewSignal(
            review=(
                "Login is slow."
            ),
            sentiment="negative",
            confidence=0.70,
            prediction_margin=0.30,
            is_uncertain=False,
        ),
        ReviewSignal(
            review=(
                "The interface is easy to use."
            ),
            sentiment="positive",
            confidence=0.90,
            prediction_margin=0.70,
            is_uncertain=False,
        ),
    ]

    counts = calculate_theme_counts(
        signals
    )

    assert counts["performance"] == 2
    assert counts["crashes"] == 1
    assert (
        counts["login_authentication"]
        == 1
    )
    assert counts["ui_ux"] == 1


def test_theme_counts_reject_empty_list():
    with pytest.raises(ValueError):
        calculate_theme_counts([])


def test_theme_counts_reject_non_list():
    with pytest.raises(TypeError):
        calculate_theme_counts(
            "not a list"
        )

def test_calculate_theme_statistics():
    signals = [
        ReviewSignal(
            review="The app is slow and crashes.",
            sentiment="negative",
            confidence=0.88,
            prediction_margin=0.60,
            is_uncertain=False,
        ),
        ReviewSignal(
            review="Performance is excellent.",
            sentiment="positive",
            confidence=0.90,
            prediction_margin=0.70,
            is_uncertain=False,
        ),
        ReviewSignal(
            review="Login is slow.",
            sentiment="negative",
            confidence=0.78,
            prediction_margin=0.40,
            is_uncertain=False,
        ),
    ]

    statistics = calculate_theme_statistics(
        signals
    )

    by_theme = {
        item.theme: item
        for item in statistics
    }

    performance = by_theme[
        "performance"
    ]

    assert performance.total_mentions == 3
    assert performance.positive_mentions == 1
    assert performance.neutral_mentions == 0
    assert performance.negative_mentions == 2

    assert performance.positive_rate == pytest.approx(
        1 / 3
    )

    assert performance.negative_rate == pytest.approx(
        2 / 3
    )

    crashes = by_theme[
        "crashes"
    ]

    assert crashes.total_mentions == 1
    assert crashes.negative_mentions == 1
    assert crashes.negative_rate == pytest.approx(
        1.0
    )

    login = by_theme[
        "login_authentication"
    ]

    assert login.total_mentions == 1
    assert login.negative_mentions == 1
    assert login.negative_rate == pytest.approx(
        1.0
    )


def test_theme_statistics_are_ranked_by_volume():
    signals = [
        ReviewSignal(
            review="The app is slow.",
            sentiment="negative",
            confidence=0.80,
            prediction_margin=0.50,
            is_uncertain=False,
        ),
        ReviewSignal(
            review="Loading is slow.",
            sentiment="negative",
            confidence=0.81,
            prediction_margin=0.51,
            is_uncertain=False,
        ),
        ReviewSignal(
            review="The app crashes.",
            sentiment="negative",
            confidence=0.90,
            prediction_margin=0.70,
            is_uncertain=False,
        ),
    ]

    statistics = calculate_theme_statistics(
        signals
    )

    assert statistics[0].theme == "performance"
    assert statistics[0].total_mentions == 2


def test_theme_statistics_reject_empty_list():
    with pytest.raises(ValueError):
        calculate_theme_statistics([])


def test_theme_statistics_reject_non_list():
    with pytest.raises(TypeError):
        calculate_theme_statistics(
            "not a list"
        )