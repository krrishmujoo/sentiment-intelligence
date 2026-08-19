import math

import pandas as pd
import pytest

from src.predictor import (
    predict_sentiment,
    predict_sentiment_batch,
)


VALID_SENTIMENTS = {
    "negative",
    "neutral",
    "positive",
}


def test_single_prediction_returns_expected_fields():
    """
    A valid review should return a complete prediction dictionary.
    """

    result = predict_sentiment(
        "The app is useful but keeps crashing."
    )

    expected_fields = {
        "review",
        "normalized_review",
        "sentiment",
        "confidence",
        "confidence_level",
        "prediction_margin",
        "is_uncertain",
        "probabilities",
    }

    assert set(result.keys()) == expected_fields
    assert result["sentiment"] in VALID_SENTIMENTS
    assert result["confidence_level"] in {
        "low",
        "medium",
        "high",
    }
    assert isinstance(result["is_uncertain"], bool)


def test_single_prediction_probabilities_are_valid():
    """
    Class probabilities should be between 0 and 1 and sum to 1.
    """

    result = predict_sentiment(
        "Amazing app."
    )

    probabilities = result["probabilities"]

    assert set(probabilities.keys()) == VALID_SENTIMENTS

    for probability in probabilities.values():
        assert 0.0 <= probability <= 1.0

    assert math.isclose(
        sum(probabilities.values()),
        1.0,
        rel_tol=1e-6,
        abs_tol=1e-6,
    )


def test_single_prediction_confidence_matches_winning_class():
    """
    Confidence should equal the probability of the predicted class.
    """

    result = predict_sentiment(
        "This app crashes every time I open it."
    )

    predicted_class = result["sentiment"]

    assert result["confidence"] == pytest.approx(
        result["probabilities"][predicted_class]
    )


def test_review_is_normalized():
    """
    Normalization should lowercase and collapse extra whitespace.
    """

    result = predict_sentiment(
        "   AMAZING    APP   "
    )

    assert result["normalized_review"] == "amazing app"


def test_empty_review_is_rejected():
    """
    Empty or whitespace-only reviews should not be accepted.
    """

    with pytest.raises(
        ValueError,
        match="Review cannot be empty",
    ):
        predict_sentiment("   ")


def test_non_string_review_is_rejected():
    """
    The prediction function should only accept text.
    """

    with pytest.raises(
        TypeError,
        match="Review must be provided as text",
    ):
        predict_sentiment(123)


def test_batch_prediction_returns_list():
    """
    Batch prediction should return one dictionary
    per input review.
    """

    reviews = [
        "Amazing app",
        "It is okay",
        "The app crashes every time",
    ]

    results = predict_sentiment_batch(
        reviews
    )

    assert isinstance(results, list)
    assert len(results) == len(reviews)

    returned_reviews = [
        result["review"]
        for result in results
    ]

    assert returned_reviews == reviews

def test_batch_predictions_have_valid_sentiments():
    results = predict_sentiment_batch([
        "Excellent application",
        "It is average",
        "Completely unusable",
    ])

    for result in results:
        assert result["sentiment"] in (
            VALID_SENTIMENTS
        )


def test_batch_probabilities_sum_to_one():
    results = predict_sentiment_batch([
        "Excellent app",
        "The experience was average",
        "This app is terrible",
    ])

    for result in results:
        assert math.isclose(
            sum(
                result[
                    "probabilities"
                ].values()
            ),
            1.0,
            rel_tol=1e-6,
            abs_tol=1e-6,
        )

def test_batch_rejects_empty_list():
    """
    Batch prediction requires at least one review.
    """

    with pytest.raises(
        ValueError,
        match="At least one review is required",
    ):
        predict_sentiment_batch([])


def test_batch_rejects_non_list_input():
    """
    Batch input must be provided as a list.
    """

    with pytest.raises(
        TypeError,
        match="review_texts must be provided as a list",
    ):
        predict_sentiment_batch(
            "Amazing app"
        )


def test_single_and_batch_predictions_are_consistent():
    """
    The same review should receive the same result through both paths.
    """

    review = "The design is nice but the app is slow."

    single_result = predict_sentiment(review)
    batch_result = predict_sentiment_batch(
    [review]
)[0]

    assert (
        single_result["sentiment"]
        == batch_result["sentiment"]
    )

    assert single_result[
        "confidence"
    ] == pytest.approx(
        batch_result["confidence"]
    )

    assert (
        single_result["is_uncertain"]
        == bool(batch_result["is_uncertain"])
    )