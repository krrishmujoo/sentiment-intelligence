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

class ThemeCount(BaseModel):
    """
    Aggregated count for one detected business theme.
    """

    theme: str
    count: int

class ThemeStatistics(BaseModel):
    """
    Business-oriented statistics for one detected theme.
    """

    theme: str

    total_mentions: int

    positive_mentions: int

    neutral_mentions: int

    negative_mentions: int

    positive_rate: float

    neutral_rate: float

    negative_rate: float

class PriorityIssue(BaseModel):
    """
    Deterministic business-priority signal for one theme.

    This is calculated locally from:
    - how often the theme appears
    - how negative the theme is

    No LLM is involved.
    """

    theme: str

    total_mentions: int

    negative_rate: float

    frequency_share: float

    priority_score: float

class InsightDatasetSummary(BaseModel):
    """
    High-level aggregate information about the dataset.

    This contains no raw review text.
    """

    total_reviews: int

    positive_rate: float

    neutral_rate: float

    negative_rate: float

    uncertainty_rate: float

    average_confidence: float


class InsightThemeSummary(BaseModel):
    """
    Privacy-safe aggregate information for one theme.

    No raw review text is included.
    """

    theme: str

    total_mentions: int

    positive_rate: float

    neutral_rate: float

    negative_rate: float


class InsightPrioritySummary(BaseModel):
    """
    Privacy-safe business-priority information
    for one issue.
    """

    theme: str

    total_mentions: int

    negative_rate: float

    frequency_share: float

    priority_score: float


class InsightPacket(BaseModel):
    """
    Privacy-controlled payload intended for the
    future LLM insight/recommendation layer.

    The default packet contains only aggregate,
    deterministic information.

    Raw review text is intentionally excluded.
    """

    dataset: InsightDatasetSummary

    themes: list[InsightThemeSummary]

    priority_issues: list[InsightPrioritySummary]
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

    theme_statistics: list[ThemeStatistics]

    priority_issues: list[PriorityIssue]