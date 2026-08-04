import math

from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


VALID_SENTIMENTS = {
    "negative",
    "neutral",
    "positive",
}


def test_health_endpoint():
    """
    The health endpoint should confirm that the API
    and model are available.
    """

    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body == {
        "status": "healthy",
        "model_loaded": True,
    }


def test_single_prediction_endpoint():
    """
    A valid review should return a complete prediction.
    """

    response = client.post(
        "/predict",
        json={
            "review": (
                "The app is useful but keeps crashing."
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

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

    assert set(body.keys()) == expected_fields
    assert body["sentiment"] in VALID_SENTIMENTS
    assert 0.0 <= body["confidence"] <= 1.0
    assert isinstance(body["is_uncertain"], bool)


def test_single_prediction_probabilities_sum_to_one():
    """
    The API should return a valid probability distribution.
    """

    response = client.post(
        "/predict",
        json={
            "review": "Amazing application."
        },
    )

    assert response.status_code == 200

    probabilities = response.json()[
        "probabilities"
    ]

    assert set(probabilities.keys()) == (
        VALID_SENTIMENTS
    )

    assert math.isclose(
        sum(probabilities.values()),
        1.0,
        rel_tol=1e-6,
        abs_tol=1e-6,
    )


def test_predict_rejects_whitespace_only_review():
    """
    A review containing only whitespace should be rejected.
    """

    response = client.post(
        "/predict",
        json={
            "review": "   "
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Review cannot be empty."
    }


def test_predict_rejects_missing_review():
    """
    The request must contain the required review field.
    """

    response = client.post(
        "/predict",
        json={},
    )

    assert response.status_code == 422


def test_predict_rejects_wrong_data_type():
    """
    The review field must contain text.
    """

    response = client.post(
        "/predict",
        json={
            "review": 123
        },
    )

    assert response.status_code == 422


def test_batch_prediction_endpoint():
    """
    A valid batch request should return one prediction
    for every submitted review.
    """

    reviews = [
        "Amazing app",
        "It is okay",
        "The app crashes every time",
    ]

    response = client.post(
        "/predict-batch",
        json={
            "reviews": reviews
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == len(reviews)
    assert len(body["predictions"]) == len(
        reviews
    )

    returned_reviews = [
        prediction["review"]
        for prediction in body["predictions"]
    ]

    assert returned_reviews == reviews


def test_batch_predictions_have_valid_fields():
    """
    Every batch result should contain the expected
    flattened probability fields.
    """

    response = client.post(
        "/predict-batch",
        json={
            "reviews": [
                "Excellent app",
                "Terrible experience",
            ]
        },
    )

    assert response.status_code == 200

    predictions = response.json()[
        "predictions"
    ]

    expected_fields = {
        "review",
        "normalized_review",
        "sentiment",
        "negative_probability",
        "neutral_probability",
        "positive_probability",
        "confidence",
        "confidence_level",
        "prediction_margin",
        "is_uncertain",
    }

    for prediction in predictions:
        assert set(prediction.keys()) == (
            expected_fields
        )

        assert (
            prediction["sentiment"]
            in VALID_SENTIMENTS
        )


def test_batch_probabilities_sum_to_one():
    """
    Each batch result should contain probabilities
    that total approximately one.
    """

    response = client.post(
        "/predict-batch",
        json={
            "reviews": [
                "Excellent app",
                "Average experience",
                "Completely unusable",
            ]
        },
    )

    assert response.status_code == 200

    for prediction in response.json()[
        "predictions"
    ]:
        total = (
            prediction[
                "negative_probability"
            ]
            + prediction[
                "neutral_probability"
            ]
            + prediction[
                "positive_probability"
            ]
        )

        assert math.isclose(
            total,
            1.0,
            rel_tol=1e-6,
            abs_tol=1e-6,
        )


def test_batch_rejects_empty_list():
    """
    A batch request must contain at least one review.
    """

    response = client.post(
        "/predict-batch",
        json={
            "reviews": []
        },
    )

    assert response.status_code == 422


def test_batch_rejects_whitespace_review():
    """
    A batch containing an invalid review should be rejected.
    """

    response = client.post(
        "/predict-batch",
        json={
            "reviews": [
                "Amazing app",
                "   ",
            ]
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Review cannot be empty."
    }


def test_unknown_endpoint_returns_404():
    """
    Requests to nonexistent routes should return 404.
    """

    response = client.get(
        "/does-not-exist"
    )

    assert response.status_code == 404
    