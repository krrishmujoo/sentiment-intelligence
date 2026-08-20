import { describe, expect, it } from "vitest";
import {
  calculateAverageConfidence,
  calculateSentimentDistribution,
  calculateUncertaintyRate,
  getHighestConfidenceReviews,
  getMostAmbiguousReviews,
} from "../analytics";
import type { Prediction } from "../../types";

function makePrediction(overrides: Partial<Prediction>): Prediction {
  return {
    review: "sample review",
    normalized_review: "sample review",
    sentiment: "neutral",
    confidence: 0.5,
    confidence_level: "low",
    prediction_margin: 0.05,
    is_uncertain: true,
    probabilities: { negative: 0.3, neutral: 0.4, positive: 0.3 },
    ...overrides,
  };
}

const dataset: Prediction[] = [
  makePrediction({
    review: "Amazing app",
    sentiment: "positive",
    confidence: 0.95,
    is_uncertain: false,
    prediction_margin: 0.8,
  }),
  makePrediction({
    review: "Terrible app",
    sentiment: "negative",
    confidence: 0.88,
    is_uncertain: false,
    prediction_margin: 0.7,
  }),
  makePrediction({
    review: "It's okay I guess",
    sentiment: "neutral",
    confidence: 0.52,
    is_uncertain: true,
    prediction_margin: 0.04,
  }),
];

describe("calculateSentimentDistribution", () => {
  it("counts and percentages match the dataset", () => {
    const summary = calculateSentimentDistribution(dataset);

    expect(summary.total).toBe(3);
    expect(summary.positive).toBe(1);
    expect(summary.negative).toBe(1);
    expect(summary.neutral).toBe(1);
    expect(summary.uncertain).toBe(1);
    expect(summary.positivePct).toBeCloseTo((1 / 3) * 100);
    expect(summary.uncertainPct).toBeCloseTo((1 / 3) * 100);
  });

  it("returns zeroed summary for an empty list", () => {
    const summary = calculateSentimentDistribution([]);
    expect(summary.total).toBe(0);
    expect(summary.averageConfidence).toBe(0);
  });
});

describe("calculateAverageConfidence", () => {
  it("computes the mean confidence", () => {
    const average = calculateAverageConfidence(dataset);
    const expected = (0.95 + 0.88 + 0.52) / 3;
    expect(average).toBeCloseTo(expected);
  });
});

describe("calculateUncertaintyRate", () => {
  it("computes the percentage of uncertain predictions", () => {
    expect(calculateUncertaintyRate(dataset)).toBeCloseTo((1 / 3) * 100);
  });
});

describe("getHighestConfidenceReviews", () => {
  it("filters by sentiment and sorts by confidence descending", () => {
    const result = getHighestConfidenceReviews(dataset, "positive", 3);
    expect(result).toHaveLength(1);
    expect(result[0].review).toBe("Amazing app");
  });
});

describe("getMostAmbiguousReviews", () => {
  it("ranks uncertain, low-margin predictions first", () => {
    const result = getMostAmbiguousReviews(dataset, 1);
    expect(result[0].review).toBe("It's okay I guess");
  });
});
