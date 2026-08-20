from collections.abc import Sequence

from src.intelligence.schemas import (
    BatchAnalyticsSummary,
    ReviewSignal,
    SentimentCounts,
    SentimentRates,
)


def _to_review_signal(
    prediction: dict,
) -> ReviewSignal:
    """
    Convert a full predictor result into the smaller
    ReviewSignal structure used by the analytics layer.
    """

    return ReviewSignal(
        review=prediction["review"],
        sentiment=prediction["sentiment"],
        confidence=prediction["confidence"],
        prediction_margin=prediction[
            "prediction_margin"
        ],
        is_uncertain=prediction[
            "is_uncertain"
        ],
    )


def calculate_batch_analytics(
    predictions: Sequence[dict],
    ambiguous_limit: int = 3,
) -> BatchAnalyticsSummary:
    """
    Calculate deterministic batch analytics from
    sentiment prediction results.

    No LLM is used here.
    """

    if not isinstance(
        predictions,
        Sequence,
    ):

        raise TypeError(
            "predictions must be a sequence"
        )


    if len(predictions) == 0:

        raise ValueError(
            "predictions must not be empty"
        )


    if ambiguous_limit < 1:

        raise ValueError(
            "ambiguous_limit must be at least 1"
        )


    signals = [
        _to_review_signal(
            prediction
        )
        for prediction in predictions
    ]


    positive_signals = [
        signal
        for signal in signals
        if signal.sentiment == "positive"
    ]


    neutral_signals = [
        signal
        for signal in signals
        if signal.sentiment == "neutral"
    ]


    negative_signals = [
        signal
        for signal in signals
        if signal.sentiment == "negative"
    ]


    total_reviews = len(
        signals
    )


    sentiment_counts = (
        SentimentCounts(
            positive=len(
                positive_signals
            ),
            neutral=len(
                neutral_signals
            ),
            negative=len(
                negative_signals
            ),
        )
    )


    sentiment_rates = (
        SentimentRates(
            positive=(
                sentiment_counts.positive
                / total_reviews
            ),
            neutral=(
                sentiment_counts.neutral
                / total_reviews
            ),
            negative=(
                sentiment_counts.negative
                / total_reviews
            ),
        )
    )


    uncertain_signals = [
        signal
        for signal in signals
        if signal.is_uncertain
    ]


    uncertain_count = len(
        uncertain_signals
    )


    uncertainty_rate = (
        uncertain_count
        / total_reviews
    )


    average_confidence = (
        sum(
            signal.confidence
            for signal in signals
        )
        / total_reviews
    )


    most_confident_positive = None

    if positive_signals:

        most_confident_positive = max(
            positive_signals,
            key=lambda signal:
                signal.confidence,
        )


    most_confident_negative = None

    if negative_signals:

        most_confident_negative = max(
            negative_signals,
            key=lambda signal:
                signal.confidence,
        )


    ambiguous_signals = sorted(
        signals,
        key=lambda signal: (
            not signal.is_uncertain,
            signal.prediction_margin,
            signal.confidence,
        ),
    )


    most_ambiguous = (
        ambiguous_signals[
            :ambiguous_limit
        ]
    )


    return BatchAnalyticsSummary(
        total_reviews=total_reviews,

        sentiment_counts=(
            sentiment_counts
        ),

        sentiment_rates=(
            sentiment_rates
        ),

        uncertain_count=(
            uncertain_count
        ),

        uncertainty_rate=(
            uncertainty_rate
        ),

        average_confidence=(
            average_confidence
        ),

        most_confident_positive=(
            most_confident_positive
        ),

        most_confident_negative=(
            most_confident_negative
        ),

        most_ambiguous=(
            most_ambiguous
        ),
    )