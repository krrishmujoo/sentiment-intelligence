from collections import Counter, defaultdict

from src.intelligence.schemas import (
    ReviewSignal,
    ThemeStatistics,
)


THEME_KEYWORDS = {
    "crashes": {
        "crash",
        "crashes",
        "crashed",
        "crashing",
        "freeze",
        "freezes",
        "frozen",
    },

    "performance": {
        "slow",
        "lag",
        "laggy",
        "performance",
        "loading",
        "load time",
    },

    "login_authentication": {
        "login",
        "log in",
        "sign in",
        "signin",
        "password",
        "authentication",
        "otp",
    },

    "payments": {
        "payment",
        "payments",
        "checkout",
        "billing",
        "charged",
        "refund",
        "subscription",
    },

    "customer_support": {
        "support",
        "customer service",
        "help desk",
        "response",
        "respond",
        "ticket",
    },

    "ui_ux": {
        "interface",
        "design",
        "ui",
        "ux",
        "layout",
        "navigation",
        "easy to use",
        "user friendly",
    },

    "features": {
        "feature",
        "features",
        "functionality",
        "option",
        "missing",
    },

    "ads": {
        "ad",
        "ads",
        "advertisement",
        "advertisements",
    },

    "notifications": {
        "notification",
        "notifications",
        "alert",
        "alerts",
    },
}


def extract_themes(
    review_text: str,
) -> list[str]:
    """
    Detect known business themes in one review.

    Matching is deterministic and local.
    No LLM or external API is used.
    """

    if not isinstance(
        review_text,
        str,
    ):
        raise TypeError(
            "review_text must be a string"
        )

    normalized_text = (
        review_text
        .lower()
        .strip()
    )

    if not normalized_text:
        raise ValueError(
            "review_text must not be empty"
        )

    detected_themes = []

    for theme, keywords in (
        THEME_KEYWORDS.items()
    ):

        if any(
            keyword in normalized_text
            for keyword in keywords
        ):
            detected_themes.append(
                theme
            )

    return detected_themes


def calculate_theme_counts(
    signals: list[ReviewSignal],
) -> dict[str, int]:
    """
    Count how often each theme appears.

    One review may contribute to multiple themes.
    """

    if not isinstance(
        signals,
        list,
    ):
        raise TypeError(
            "signals must be a list"
        )

    if not signals:
        raise ValueError(
            "signals must not be empty"
        )

    theme_counter = Counter()

    for signal in signals:

        themes = extract_themes(
            signal.review
        )

        theme_counter.update(
            themes
        )

    return dict(
        theme_counter.most_common()
    )


def calculate_theme_statistics(
    signals: list[ReviewSignal],
) -> list[ThemeStatistics]:
    """
    Calculate sentiment breakdown for each detected theme.

    Example:

    performance:
        total_mentions = 10
        negative_mentions = 8
        neutral_mentions = 1
        positive_mentions = 1
        negative_rate = 0.80
    """

    if not isinstance(
        signals,
        list,
    ):
        raise TypeError(
            "signals must be a list"
        )

    if not signals:
        raise ValueError(
            "signals must not be empty"
        )

    theme_sentiments = defaultdict(
        lambda: Counter()
    )

    for signal in signals:

        themes = extract_themes(
            signal.review
        )

        for theme in themes:

            theme_sentiments[
                theme
            ][
                signal.sentiment
            ] += 1

    statistics = []

    for theme, sentiment_counts in (
        theme_sentiments.items()
    ):

        positive_mentions = (
            sentiment_counts["positive"]
        )

        neutral_mentions = (
            sentiment_counts["neutral"]
        )

        negative_mentions = (
            sentiment_counts["negative"]
        )

        total_mentions = (
            positive_mentions
            + neutral_mentions
            + negative_mentions
        )

        statistics.append(
            ThemeStatistics(
                theme=theme,

                total_mentions=(
                    total_mentions
                ),

                positive_mentions=(
                    positive_mentions
                ),

                neutral_mentions=(
                    neutral_mentions
                ),

                negative_mentions=(
                    negative_mentions
                ),

                positive_rate=(
                    positive_mentions
                    / total_mentions
                ),

                neutral_rate=(
                    neutral_mentions
                    / total_mentions
                ),

                negative_rate=(
                    negative_mentions
                    / total_mentions
                ),
            )
        )

    statistics.sort(
        key=lambda item: (
            -item.total_mentions,
            -item.negative_rate,
            item.theme,
        )
    )

    return statistics