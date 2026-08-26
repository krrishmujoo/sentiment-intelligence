from src.intelligence.schemas import (
    BatchAnalyticsSummary,
    InsightDatasetSummary,
    InsightPacket,
    InsightPrioritySummary,
    InsightThemeSummary,
)


def build_insight_packet(
    summary: BatchAnalyticsSummary,
    top_theme_limit: int = 10,
    top_priority_limit: int = 5,
) -> InsightPacket:
    """
    Convert deterministic batch analytics into a
    privacy-controlled aggregate payload.

    Raw review text is intentionally excluded.

    This packet is designed to become the boundary
    between local analytics and the future LLM layer.
    """

    if not isinstance(
        summary,
        BatchAnalyticsSummary,
    ):
        raise TypeError(
            "summary must be a BatchAnalyticsSummary"
        )

    if top_theme_limit < 1:
        raise ValueError(
            "top_theme_limit must be at least 1"
        )

    if top_priority_limit < 1:
        raise ValueError(
            "top_priority_limit must be at least 1"
        )

    dataset = InsightDatasetSummary(
        total_reviews=(
            summary.total_reviews
        ),

        positive_rate=(
            summary.sentiment_rates.positive
        ),

        neutral_rate=(
            summary.sentiment_rates.neutral
        ),

        negative_rate=(
            summary.sentiment_rates.negative
        ),

        uncertainty_rate=(
            summary.uncertainty_rate
        ),

        average_confidence=(
            summary.average_confidence
        ),
    )

    themes = [
        InsightThemeSummary(
            theme=item.theme,

            total_mentions=(
                item.total_mentions
            ),

            positive_rate=(
                item.positive_rate
            ),

            neutral_rate=(
                item.neutral_rate
            ),

            negative_rate=(
                item.negative_rate
            ),
        )
        for item in summary.theme_statistics[
            :top_theme_limit
        ]
    ]

    priority_issues = [
        InsightPrioritySummary(
            theme=item.theme,

            total_mentions=(
                item.total_mentions
            ),

            negative_rate=(
                item.negative_rate
            ),

            frequency_share=(
                item.frequency_share
            ),

            priority_score=(
                item.priority_score
            ),
        )
        for item in summary.priority_issues[
            :top_priority_limit
        ]
    ]

    return InsightPacket(
        dataset=dataset,
        themes=themes,
        priority_issues=priority_issues,
    )