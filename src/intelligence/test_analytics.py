import pytest

from src.intelligence.analytics import calculate_batch_analytics


def test_calculate_batch_analytics_basic_summary():
    predictions = [
        {
            "review": "Amazing app",
            "sentiment": "positive",
            "confidence": 0.90,
            "prediction_margin": 0.70,
            "is_uncertain": False,
        },
        {
            "review": "Terrible crashes",
            "sentiment": "negative",
            "confidence": 0.82,
            "prediction_margin": 0.63,
            "is_uncertain": False,
        },
        {
            "review": "It is okay",
            "sentiment": "neutral",
            "confidence": 0.47,
            "prediction_margin": 0.04,
            "is_uncertain": True,
        },
        {
            "review": "Useful but buggy",
            "sentiment": "positive",
            "confidence": 0.55,
            "prediction_margin": 0.07,
            "is_uncertain": True,
        },
    ]

    summary = calculate_batch_analytics(predictions)

    assert summary.total_reviews == 4

    assert summary.sentiment_counts.positive == 2
    assert summary.sentiment_counts.neutral == 1
    assert summary.sentiment_counts.negative == 1

    assert summary.sentiment_rates.positive == pytest.approx(0.50)
    assert summary.sentiment_rates.neutral == pytest.approx(0.25)
    assert summary.sentiment_rates.negative == pytest.approx(0.25)

    assert summary.uncertain_count == 2
    assert summary.uncertainty_rate == pytest.approx(0.50)

    assert summary.average_confidence == pytest.approx(0.685)

    theme_statistics = {
        item.theme: item
        for item in summary.theme_statistics
         }
    assert (
        theme_statistics["crashes"].total_mentions
        == 1
    )

def test_most_confident_positive():
    predictions = [
        {
            "review": "Good",
            "sentiment": "positive",
            "confidence": 0.70,
            "prediction_margin": 0.40,
            "is_uncertain": False,
        },
        {
            "review": "Excellent",
            "sentiment": "positive",
            "confidence": 0.95,
            "prediction_margin": 0.80,
            "is_uncertain": False,
        },
    ]

    summary = calculate_batch_analytics(predictions)

    assert summary.most_confident_positive is not None
    assert summary.most_confident_positive.review == "Excellent"
    assert summary.most_confident_positive.confidence == pytest.approx(0.95)


def test_most_confident_negative():
    predictions = [
        {
            "review": "Bad",
            "sentiment": "negative",
            "confidence": 0.65,
            "prediction_margin": 0.30,
            "is_uncertain": False,
        },
        {
            "review": "Completely unusable",
            "sentiment": "negative",
            "confidence": 0.91,
            "prediction_margin": 0.74,
            "is_uncertain": False,
        },
    ]

    summary = calculate_batch_analytics(predictions)

    assert summary.most_confident_negative is not None
    assert summary.most_confident_negative.review == "Completely unusable"


def test_missing_positive_returns_none():
    predictions = [
        {
            "review": "Bad",
            "sentiment": "negative",
            "confidence": 0.80,
            "prediction_margin": 0.60,
            "is_uncertain": False,
        }
    ]

    summary = calculate_batch_analytics(predictions)

    assert summary.most_confident_positive is None


def test_ambiguous_reviews_prioritize_uncertain_and_low_margin():
    predictions = [
        {
            "review": "Strong negative",
            "sentiment": "negative",
            "confidence": 0.90,
            "prediction_margin": 0.75,
            "is_uncertain": False,
        },
        {
            "review": "Very ambiguous",
            "sentiment": "neutral",
            "confidence": 0.45,
            "prediction_margin": 0.02,
            "is_uncertain": True,
        },
        {
            "review": "Somewhat ambiguous",
            "sentiment": "positive",
            "confidence": 0.55,
            "prediction_margin": 0.08,
            "is_uncertain": True,
        },
    ]

    summary = calculate_batch_analytics(
        predictions,
        ambiguous_limit=2,
    )

    assert len(summary.most_ambiguous) == 2
    assert summary.most_ambiguous[0].review == "Very ambiguous"
    assert summary.most_ambiguous[1].review == "Somewhat ambiguous"


def test_empty_predictions_rejected():
    with pytest.raises(ValueError):
        calculate_batch_analytics([])


def test_invalid_ambiguous_limit_rejected():
    predictions = [
        {
            "review": "Fine",
            "sentiment": "neutral",
            "confidence": 0.60,
            "prediction_margin": 0.20,
            "is_uncertain": False,
        }
    ]

    with pytest.raises(ValueError):
        calculate_batch_analytics(
            predictions,
            ambiguous_limit=0,
        )

def test_batch_analytics_includes_theme_statistics():
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

    by_theme = {
        item.theme: item
        for item in summary.theme_statistics
    }

    performance = by_theme[
        "performance"
    ]

    assert performance.total_mentions == 3
    assert performance.positive_mentions == 1
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

def test_batch_analytics_includes_priority_issues():
    predictions = [
        {
            "review": "The app is slow.",
            "sentiment": "negative",
            "confidence": 0.82,
            "prediction_margin": 0.50,
            "is_uncertain": False,
        },
        {
            "review": "Loading is slow.",
            "sentiment": "negative",
            "confidence": 0.80,
            "prediction_margin": 0.48,
            "is_uncertain": False,
        },
        {
            "review": "Performance is excellent.",
            "sentiment": "positive",
            "confidence": 0.90,
            "prediction_margin": 0.70,
            "is_uncertain": False,
        },
        {
            "review": "The app crashes.",
            "sentiment": "negative",
            "confidence": 0.91,
            "prediction_margin": 0.74,
            "is_uncertain": False,
        },
    ]

    summary = calculate_batch_analytics(
        predictions
    )

    assert len(
        summary.priority_issues
    ) >= 2

    assert (
        summary.priority_issues[0].theme
        == "performance"
    )

    performance = (
        summary.priority_issues[0]
    )

    assert (
        performance.total_mentions
        == 3
    )

    assert (
        performance.negative_rate
        == pytest.approx(2 / 3)
    )

    assert (
        performance.frequency_share
        == pytest.approx(3 / 4)
    )

    assert (
        performance.priority_score
        == pytest.approx(0.50)
    )