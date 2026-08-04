from pathlib import Path

import joblib
import pandas as pd


# ---------------------------------------------------------
# Project and model paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "balanced_logreg_bigram.joblib"
)

VECTORIZER_PATH = (
    PROJECT_ROOT
    / "models"
    / "tfidf_unigram_bigram.joblib"
)


# ---------------------------------------------------------
# Validate that saved artifacts exist
# ---------------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file was not found: {MODEL_PATH}"
    )

if not VECTORIZER_PATH.exists():
    raise FileNotFoundError(
        f"Vectorizer file was not found: {VECTORIZER_PATH}"
    )


# ---------------------------------------------------------
# Load fitted model and vectorizer
# ---------------------------------------------------------

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# ---------------------------------------------------------
# Text preprocessing
# ---------------------------------------------------------

def normalize_review(text: str) -> str:
    """
    Normalize one review using the same logic used during training.

    Steps:
    - Validate that the input is a string.
    - Convert text to lowercase.
    - Remove leading and trailing whitespace.
    - Replace repeated whitespace with a single space.
    - Reject empty reviews.
    """

    if not isinstance(text, str):
        raise TypeError(
            "Review must be provided as text."
        )

    normalized_text = " ".join(
        text.lower().strip().split()
    )

    if not normalized_text:
        raise ValueError(
            "Review cannot be empty."
        )

    return normalized_text


# ---------------------------------------------------------
# Confidence helpers
# ---------------------------------------------------------

def get_confidence_level(confidence: float) -> str:
    """
    Convert a numerical confidence value into a display label.
    """

    if confidence >= 0.80:
        return "high"

    if confidence >= 0.60:
        return "medium"

    return "low"


def calculate_uncertainty(
    probability_values
) -> tuple[float, bool]:
    """
    Calculate the gap between the two highest class probabilities.

    A prediction is marked uncertain when:
    - the highest probability is below 0.50, or
    - the gap between the highest two probabilities is below 0.10
    """

    sorted_probabilities = sorted(
        [
            float(probability)
            for probability in probability_values
        ],
        reverse=True
    )

    confidence = sorted_probabilities[0]

    prediction_margin = (
        sorted_probabilities[0]
        - sorted_probabilities[1]
    )

    is_uncertain = (
        confidence < 0.60
        or prediction_margin < 0.10
    )

    return float(prediction_margin), bool(is_uncertain)

# ---------------------------------------------------------
# Shared prediction engine
# ---------------------------------------------------------

def _predict_reviews(
    review_texts: list[str]
) -> list[dict]:
    """
    Run sentiment prediction for one or more reviews.

    This internal function contains the shared prediction
    logic used by both single and batch prediction.
    """

    normalized_reviews = [
        normalize_review(review)
        for review in review_texts
    ]

    review_features = vectorizer.transform(
        normalized_reviews
    )

    predictions = model.predict(
        review_features
    )

    probability_matrix = model.predict_proba(
        review_features
    )

    prediction_results = []

    for row_index, predicted_sentiment in enumerate(
        predictions
    ):
        probability_values = probability_matrix[
            row_index
        ]

        class_probabilities = {
            class_name: float(probability)
            for class_name, probability in zip(
                model.classes_,
                probability_values
            )
        }

        confidence = class_probabilities[
            predicted_sentiment
        ]

        prediction_margin, is_uncertain = (
            calculate_uncertainty(
                probability_values
            )
        )

        prediction_results.append({
            "review": review_texts[row_index],
            "normalized_review": normalized_reviews[
                row_index
            ],
            "sentiment": predicted_sentiment,
            "confidence": float(confidence),
            "confidence_level": get_confidence_level(
                confidence
            ),
            "prediction_margin": prediction_margin,
            "is_uncertain": is_uncertain,
            "probabilities": class_probabilities,
        })

    return prediction_results


# ---------------------------------------------------------
# Single-review prediction
# ---------------------------------------------------------

def predict_sentiment(
    review_text: str
) -> dict:
    """
    Predict sentiment for one review.
    """

    return _predict_reviews(
        [review_text]
    )[0]


# ---------------------------------------------------------
# Batch prediction
# ---------------------------------------------------------

def predict_sentiment_batch(
    review_texts: list[str]
) -> pd.DataFrame:
    """
    Predict sentiment for multiple reviews in one batch.
    """

    if not isinstance(review_texts, list):
        raise TypeError(
            "review_texts must be provided as a list."
        )

    if len(review_texts) == 0:
        raise ValueError(
            "At least one review is required."
        )

    prediction_results = _predict_reviews(
        review_texts
    )

    flattened_results = []

    for result in prediction_results:
        flattened_result = {
            "review": result["review"],
            "normalized_review": result[
                "normalized_review"
            ],
            "sentiment": result["sentiment"],
        }

        for class_name, probability in result[
            "probabilities"
        ].items():
            flattened_result[
                f"{class_name}_probability"
            ] = probability

        flattened_result.update({
            "confidence": result["confidence"],
            "confidence_level": result[
                "confidence_level"
            ],
            "prediction_margin": result[
                "prediction_margin"
            ],
            "is_uncertain": result[
                "is_uncertain"
            ],
        })

        flattened_results.append(
            flattened_result
        )

    return pd.DataFrame(
        flattened_results
    )

