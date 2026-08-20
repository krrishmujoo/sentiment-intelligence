from pathlib import Path

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_SRC = FRONTEND_DIR / "src"


def test_frontend_homepage_loads():
    """
    The production application root should
    successfully return HTML.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert "text/html" in response.headers[
        "content-type"
    ]


def test_react_frontend_directory_exists():
    """
    The project should contain the React/Vite
    frontend at the root frontend directory.
    """

    assert FRONTEND_DIR.exists()

    assert FRONTEND_DIR.is_dir()


def test_react_package_json_exists():
    """
    The React project must contain its npm
    package configuration.
    """

    package_json = (
        FRONTEND_DIR / "package.json"
    )

    assert package_json.exists()


def test_react_entrypoint_exists():
    """
    React should have its main TypeScript
    entrypoint.
    """

    main_file = (
        FRONTEND_SRC / "main.tsx"
    )

    assert main_file.exists()


def test_react_app_component_exists():
    """
    The main React App component should exist.
    """

    app_file = (
        FRONTEND_SRC / "App.tsx"
    )

    assert app_file.exists()


def test_react_stylesheet_exists():
    """
    The React application should contain
    its stylesheet.
    """

    stylesheet = (
        FRONTEND_SRC / "index.css"
    )

    assert stylesheet.exists()


def test_vite_configuration_exists():
    """
    Vite should provide the development
    frontend configuration.
    """

    vite_config = (
        FRONTEND_DIR / "vite.config.ts"
    )

    assert vite_config.exists()


def test_vite_proxies_single_prediction_endpoint():
    """
    During development, Vite should proxy
    single-review requests to FastAPI.
    """

    vite_config = (
        FRONTEND_DIR / "vite.config.ts"
    ).read_text()

    assert "/predict" in vite_config


def test_vite_proxies_batch_prediction_endpoint():
    """
    During development, Vite should proxy
    batch-review requests to FastAPI.
    """

    vite_config = (
        FRONTEND_DIR / "vite.config.ts"
    ).read_text()

    assert "/predict-batch" in vite_config


def test_vite_proxies_health_endpoint():
    """
    React uses the health endpoint to
    determine whether the model is online.
    """

    vite_config = (
        FRONTEND_DIR / "vite.config.ts"
    ).read_text()

    assert "/health" in vite_config


def test_existing_api_is_available_through_main_app():
    """
    The main application must continue
    exposing the existing FastAPI backend.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert data["model_loaded"] is True


def test_single_prediction_works_through_main_app():
    """
    The main application should expose
    single-review sentiment inference.
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
        prediction[
            "probabilities"
        ].keys()
    ) == {
        "negative",
        "neutral",
        "positive",
    }


def test_batch_prediction_works_through_main_app():
    """
    The main application should expose
    batch sentiment inference.
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

    assert len(
        data["predictions"]
    ) == 3

    for prediction in data[
        "predictions"
    ]:

        assert prediction[
            "sentiment"
        ] in {
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