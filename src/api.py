from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.predictor import (
    predict_sentiment,
    predict_sentiment_batch
)


app = FastAPI(
    title="Sentiment Analyzer API",
    description=(
        "API for classifying app reviews as "
        "negative, neutral, or positive."
    ),
    version="1.0.0"
)


class SinglePredictionRequest(BaseModel):
    review: str = Field(
        ...,
        min_length=1,
        description="Review text to analyze."
    )


class BatchPredictionRequest(BaseModel):
    reviews: list[str] = Field(
        ...,
        min_length=1,
        description="Review texts to analyze."
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True
    }


@app.post("/predict")
def predict_single(
    request: SinglePredictionRequest
):
    try:
        result = predict_sentiment(
            request.review
        )

        return result

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error


@app.post("/predict-batch")
@app.post("/predict-batch")
def predict_batch(
    request: BatchPredictionRequest
):
    try:
        results = predict_sentiment_batch(
            request.reviews
        )

        return {
            "count": len(results),
            "predictions": results,
        }

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error