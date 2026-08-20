from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_frontend_homepage_loads():
    """
    The root URL should successfully serve
    the Sentiment Analyzer frontend.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert "text/html" in response.headers[
        "content-type"
    ]


def test_frontend_contains_main_title():
    """
    The frontend should contain the main
    Sentiment Analyzer heading.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert "Sentiment Analyzer" in response.text


def test_frontend_connects_to_single_prediction_endpoint():
    """
    The frontend JavaScript should call
    the single-prediction API.
    """

    response = client.get(
        "/frontend/app.js"
    )

    assert response.status_code == 200

    assert '"/predict"' in response.text


def test_frontend_connects_to_batch_prediction_endpoint():
    """
    Manual batch and CSV workflows should
    call the batch prediction API.
    """

    response = client.get(
        "/frontend/app.js"
    )

    assert response.status_code == 200

    assert '"/predict-batch"' in response.text


def test_frontend_contains_csv_parser():
    """
    The JavaScript bundle should contain
    the custom CSV parser.
    """

    response = client.get(
        "/frontend/app.js"
    )

    assert response.status_code == 200

    javascript = response.text

    assert (
        "function parseCsv(text)"
        in javascript
    )

    assert (
        "parseCsv("
        in javascript
    )


def test_frontend_reads_uploaded_csv_file():
    """
    Regression test for the bug where
    parseCsv(text) was called before
    the uploaded file had been read.
    """

    response = client.get(
        "/frontend/app.js"
    )

    assert response.status_code == 200

    javascript = response.text

    assert (
        "await file.text()"
        in javascript
    )


def test_frontend_contains_csv_download_filename():
    """
    Prediction export should retain its
    expected CSV filename.
    """

    response = client.get(
        "/frontend/app.js"
    )

    assert response.status_code == 200

    assert (
        "sentiment_predictions.csv"
        in response.text
    )

def test_existing_api_is_available_through_main_app():
    """
    app.py imports and extends the same
    FastAPI application used by src.api.

    Therefore API routes must still work
    when the application is launched through
    app:app.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_single_prediction_works_through_main_app():
    """
    Verify the main production application
    exposes the working prediction backend.
    """

    response = client.post(
        "/predict",
        json={
            "review":
                "Amazing app, I absolutely love it."
        },
    )

    assert response.status_code == 200

    prediction = response.json()

    assert prediction["sentiment"] in {
        "negative",
        "neutral",
        "positive",
    }

    assert (
        0.0
        <= prediction["confidence"]
        <= 1.0
    )

    assert set(
        prediction["probabilities"].keys()
    ) == {
        "negative",
        "neutral",
        "positive",
    }


def test_batch_prediction_works_through_main_app():
    """
    Verify that the production application
    exposes batch inference as expected by
    both manual batch and CSV workflows.
    """

    reviews = [
        "Amazing app.",
        "The app crashes constantly.",
        "It works fine.",
    ]

    response = client.post(
        "/predict-batch",
        json={
            "reviews": reviews
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 3
    assert len(data["predictions"]) == 3

    for prediction in data["predictions"]:

        assert prediction["sentiment"] in {
            "negative",
            "neutral",
            "positive",
        }

        assert set(
            prediction[
                "probabilities"
            ].keys()
        ) == {
            "negative",
            "neutral",
            "positive",
        }

def test_frontend_javascript_file_is_served():
    """
    FastAPI should serve the frontend
    JavaScript file.
    """

    response = client.get(
        "/frontend/app.js"
    )

    assert response.status_code == 200

    assert (
        "javascript"
        in response.headers[
            "content-type"
        ]
    )


def test_frontend_stylesheet_is_served():
    """
    FastAPI should serve the frontend
    stylesheet.
    """

    response = client.get(
        "/frontend/style.css"
    )

    assert response.status_code == 200

    assert (
        "text/css"
        in response.headers[
            "content-type"
        ]
    )

def test_frontend_contains_single_review_controls():
    """
    Single-review UI elements must exist.
    """

    response = client.get("/")

    html = response.text

    assert 'id="review"' in html
    assert 'id="analyze-button"' in html
    assert 'id="result"' in html

    assert 'id="sentiment"' in html
    assert 'id="confidence"' in html
    assert 'id="confidence-level"' in html

    assert 'id="negative"' in html
    assert 'id="neutral"' in html
    assert 'id="positive"' in html

    assert 'id="uncertain"' in html


def test_frontend_contains_batch_controls():
    """
    Batch-analysis UI elements must exist.
    """

    response = client.get("/")

    html = response.text

    assert 'id="batch-reviews"' in html
    assert 'id="batch-button"' in html
    assert 'id="batch-results"' in html
    assert 'id="batch-table-body"' in html
    assert 'id="batch-summary"' in html


def test_frontend_contains_csv_controls():
    """
    CSV upload and download controls
    must exist.
    """

    response = client.get("/")

    html = response.text

    assert 'id="csv-file"' in html
    assert 'id="csv-button"' in html
    assert 'id="csv-results"' in html
    assert 'id="csv-table-body"' in html
    assert 'id="csv-summary"' in html
    assert 'id="download-button"' in html