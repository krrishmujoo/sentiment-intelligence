import type {
  AnalyzeResponse,
  BatchPredictionResponse,
  HealthResponse,
  Prediction,
} from "../types";

export class ApiRequestError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
  }
}

async function parseJsonOrThrow<T>(response: Response, fallbackMessage: string): Promise<T> {
  let body: unknown;

  try {
    body = await response.json();
  } catch {
    body = null;
  }

  if (!response.ok) {
    const detail =
      body && typeof body === "object" && "detail" in body
        ? String((body as { detail: unknown }).detail)
        : fallbackMessage;

    throw new ApiRequestError(detail, response.status);
  }

  return body as T;
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch("/health");
  return parseJsonOrThrow<HealthResponse>(response, "Unable to reach the API.");
}

export async function predictReview(review: string): Promise<Prediction> {
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ review }),
  });

  return parseJsonOrThrow<Prediction>(response, "Prediction failed.");
}

export async function predictBatch(reviews: string[]): Promise<BatchPredictionResponse> {
  const response = await fetch("/predict-batch", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reviews }),
  });

  return parseJsonOrThrow<BatchPredictionResponse>(response, "Batch prediction failed.");
}

export async function analyzeBusinessQuestion(
  question: string,
  predictions: Prediction[],
): Promise<AnalyzeResponse> {
  const response = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, predictions }),
  });

  return parseJsonOrThrow<AnalyzeResponse>(response, "Business insight generation failed.");
}