export type Sentiment = "negative" | "neutral" | "positive";

export type ConfidenceLevel = "low" | "medium" | "high";

export interface ClassProbabilities {
  negative: number;
  neutral: number;
  positive: number;
}

/**
 * Matches the exact response schema returned by both
 * POST /predict and each item of POST /predict-batch.
 * Do not add fields here that the backend does not return —
 * the UI must only ever display real API output or values
 * mathematically derived from it.
 */
export interface Prediction {
  review: string;
  normalized_review: string;
  sentiment: Sentiment;
  confidence: number;
  confidence_level: ConfidenceLevel;
  prediction_margin: number;
  is_uncertain: boolean;
  probabilities: ClassProbabilities;
}

export interface BatchPredictionResponse {
  count: number;
  predictions: Prediction[];
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
}

export interface ApiError {
  detail: string;
}

/** Frontend-only derived summary — every field here is computed from Prediction[]. */
export interface SentimentDistributionSummary {
  total: number;
  positive: number;
  neutral: number;
  negative: number;
  uncertain: number;
  positivePct: number;
  neutralPct: number;
  negativePct: number;
  uncertainPct: number;
  averageConfidence: number;
}

export type SentimentFilter = "all" | Sentiment;

export type SortField = "confidence" | "prediction_margin" | "review";
export type SortDirection = "asc" | "desc";
