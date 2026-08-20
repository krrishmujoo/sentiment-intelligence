from typing import Literal

from pydantic import BaseModel


SentimentLabel = Literal[
    "positive",
    "neutral",
    "negative",
]


class ReviewSignal(BaseModel):
    """
    A compact representation of one analyzed review.

    This is intentionally smaller than the full predictor
    response so analytics code only carries the fields it
    actually needs.
    """

    review: str

    sentiment: SentimentLabel

    confidence: float

    prediction_margin: float

    is_uncertain: bool


class SentimentCounts(BaseModel):
    """
    Number of reviews predicted in each sentiment class.
    """

    positive: int

    neutral: int

    negative: int


class SentimentRates(BaseModel):
    """
    Fraction of the full batch belonging to each sentiment
    class.

    Example:

    positive = 0.50
    neutral = 0.25
    negative = 0.25
    """

    positive: float

    neutral: float

    negative: float


class BatchAnalyticsSummary(BaseModel):
    """
    Deterministic analytics calculated locally from a batch
    of sentiment predictions.

    No LLM is involved in creating this object.
    """

    total_reviews: int

    sentiment_counts: SentimentCounts

    sentiment_rates: SentimentRates

    uncertain_count: int

    uncertainty_rate: float

    average_confidence: float

    most_confident_positive: ReviewSignal | None

    most_confident_negative: ReviewSignal | None

    most_ambiguous: list[ReviewSignal]