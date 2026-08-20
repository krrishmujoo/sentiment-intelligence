import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiRequestError, getHealth, predictBatch, predictReview } from "../api";

function mockFetchOnce(body: unknown, status = 200) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      json: async () => body,
    })
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("getHealth", () => {
  it("calls GET /health", async () => {
    mockFetchOnce({ status: "healthy", model_loaded: true });

    await getHealth();

    expect(fetch).toHaveBeenCalledWith("/health");
  });
});

describe("predictReview", () => {
  it("calls POST /predict with the review body", async () => {
    mockFetchOnce({
      review: "Great app",
      normalized_review: "great app",
      sentiment: "positive",
      confidence: 0.9,
      confidence_level: "high",
      prediction_margin: 0.6,
      is_uncertain: false,
      probabilities: { negative: 0.02, neutral: 0.08, positive: 0.9 },
    });

    const result = await predictReview("Great app");

    expect(fetch).toHaveBeenCalledWith(
      "/predict",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ review: "Great app" }),
      })
    );
    expect(result.sentiment).toBe("positive");
  });

  it("throws ApiRequestError with the backend detail message on failure", async () => {
    mockFetchOnce({ detail: "Review cannot be empty." }, 400);

    await expect(predictReview("   ")).rejects.toThrow(ApiRequestError);
    await expect(predictReview("   ")).rejects.toThrow("Review cannot be empty.");
  });
});

describe("predictBatch", () => {
  it("calls POST /predict-batch with the reviews array", async () => {
    mockFetchOnce({ count: 1, predictions: [] });

    await predictBatch(["Great app"]);

    expect(fetch).toHaveBeenCalledWith(
      "/predict-batch",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ reviews: ["Great app"] }),
      })
    );
  });
});
