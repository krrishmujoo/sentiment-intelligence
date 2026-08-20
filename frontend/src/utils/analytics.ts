import type { Prediction, SentimentDistributionSummary } from "../types";

function toPct(count: number, total: number): number {
  if (total === 0) return 0;
  return (count / total) * 100;
}

export function calculateSentimentDistribution(
  predictions: Prediction[]
): SentimentDistributionSummary {
  const total = predictions.length;

  let positive = 0;
  let neutral = 0;
  let negative = 0;
  let uncertain = 0;
  let confidenceSum = 0;

  for (const prediction of predictions) {
    if (prediction.sentiment === "positive") positive++;
    else if (prediction.sentiment === "neutral") neutral++;
    else if (prediction.sentiment === "negative") negative++;

    if (prediction.is_uncertain) uncertain++;

    confidenceSum += prediction.confidence;
  }

  return {
    total,
    positive,
    neutral,
    negative,
    uncertain,
    positivePct: toPct(positive, total),
    neutralPct: toPct(neutral, total),
    negativePct: toPct(negative, total),
    uncertainPct: toPct(uncertain, total),
    averageConfidence: total === 0 ? 0 : confidenceSum / total,
  };
}

export function calculateAverageConfidence(predictions: Prediction[]): number {
  if (predictions.length === 0) return 0;
  const sum = predictions.reduce((acc, p) => acc + p.confidence, 0);
  return sum / predictions.length;
}

export function calculateUncertaintyRate(predictions: Prediction[]): number {
  if (predictions.length === 0) return 0;
  const uncertainCount = predictions.filter((p) => p.is_uncertain).length;
  return (uncertainCount / predictions.length) * 100;
}

/** Highest-confidence predictions for a given sentiment class. */
export function getHighestConfidenceReviews(
  predictions: Prediction[],
  sentiment: Prediction["sentiment"],
  limit = 3
): Prediction[] {
  return predictions
    .filter((p) => p.sentiment === sentiment)
    .sort((a, b) => b.confidence - a.confidence)
    .slice(0, limit);
}

/**
 * Most ambiguous reviews: uncertain first, then ranked by the smallest
 * prediction_margin (closest race between classes), tie-broken by
 * lowest confidence. Purely a re-sort of returned API values.
 */
export function getMostAmbiguousReviews(predictions: Prediction[], limit = 3): Prediction[] {
  return [...predictions]
    .sort((a, b) => {
      if (a.is_uncertain !== b.is_uncertain) {
        return a.is_uncertain ? -1 : 1;
      }
      if (a.prediction_margin !== b.prediction_margin) {
        return a.prediction_margin - b.prediction_margin;
      }
      return a.confidence - b.confidence;
    })
    .slice(0, limit);
}

export function getLowestConfidenceReviews(predictions: Prediction[], limit = 3): Prediction[] {
  return [...predictions].sort((a, b) => a.confidence - b.confidence).slice(0, limit);
}
