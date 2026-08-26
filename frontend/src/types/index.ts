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

/**
 * Below: types for the POST /analyze business intelligence pipeline.
 * These mirror the backend pydantic schemas exactly
 * (src/intelligence/insight_schema.py, planner_schema.py,
 * and the InsightPacket schemas referenced by insight_packet.py).
 */

// ---- Privacy-safe aggregate analytics (InsightPacket) ----

export interface InsightDatasetSummary {
  total_reviews: number;
  positive_rate: number;
  neutral_rate: number;
  negative_rate: number;
  uncertainty_rate: number;
  average_confidence: number;
}

export interface InsightThemeSummary {
  theme: string;
  total_mentions: number;
  positive_rate: number;
  neutral_rate: number;
  negative_rate: number;
}

export interface InsightPrioritySummary {
  theme: string;
  total_mentions: number;
  negative_rate: number;
  frequency_share: number;
  priority_score: number;
}

export interface InsightPacket {
  dataset: InsightDatasetSummary;
  themes: InsightThemeSummary[];
  priority_issues: InsightPrioritySummary[];
}

// ---- Planner (AnalysisPlan) ----

export type PlannerOperationName =
  | "summarize_sentiment"
  | "rank_priority_issues"
  | "summarize_themes"
  | "filter_negative_themes"
  | "filter_positive_themes"
  | "summarize_uncertainty";

export interface PlannerOperation {
  operation: PlannerOperationName;
  limit: number | null;
}

export interface AnalysisPlan {
  intent: string;
  operations: PlannerOperation[];
}

/**
 * The shape of `execution` is produced by the backend's plan
 * executor (src/intelligence/planner_executor.py), which was not
 * part of this frontend integration and is not rendered directly.
 * The "Analysis Details" UI is built from `plan`, not `execution`.
 * Typed loosely and intentionally, rather than guessed.
 */
export type AnalysisExecutionResult = Record<string, unknown>;

// ---- Business insights (BusinessInsightResponse) ----

export type InsightPriority = "high" | "medium" | "low";

export interface InsightObservation {
  title: string;
  description: string;
  evidence: string[];
}

export interface InsightRecommendation {
  title: string;
  action: string;
  rationale: string;
  priority: InsightPriority;
}

export interface BusinessInsightResponse {
  summary: string;
  observations: InsightObservation[];
  recommendations: InsightRecommendation[];
}

// ---- /analyze request/response ----

export interface AnalyzeRequest {
  question: string;
  predictions: Prediction[];
}

export interface AnalyzeResponse {
  question: string;
  plan: AnalysisPlan;
  analytics: InsightPacket;
  execution: AnalysisExecutionResult;
  insights: BusinessInsightResponse;
}