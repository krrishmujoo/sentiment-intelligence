from src.intelligence.schemas import (
    PriorityIssue,
    ThemeStatistics,
)


def calculate_priority_issues(
    theme_statistics: list[ThemeStatistics],
    total_reviews: int,
) -> list[PriorityIssue]:
    """
    Rank business issues using a transparent,
    deterministic formula.

    priority_score =
        frequency_share * negative_rate

    where:

    frequency_share =
        theme total mentions / total reviews

    No LLM is used.
    """

    if not isinstance(
        theme_statistics,
        list,
    ):
        raise TypeError(
            "theme_statistics must be a list"
        )

    if total_reviews < 1:
        raise ValueError(
            "total_reviews must be at least 1"
        )

    priority_issues = []

    for theme in theme_statistics:

        frequency_share = (
            theme.total_mentions
            / total_reviews
        )

        priority_score = (
            frequency_share
            * theme.negative_rate
        )

        priority_issues.append(
            PriorityIssue(
                theme=theme.theme,
                total_mentions=(
                    theme.total_mentions
                ),
                negative_rate=(
                    theme.negative_rate
                ),
                frequency_share=(
                    frequency_share
                ),
                priority_score=(
                    priority_score
                ),
            )
        )

    priority_issues.sort(
        key=lambda issue: (
            -issue.priority_score,
            -issue.total_mentions,
            issue.theme,
        )
    )

    return priority_issues