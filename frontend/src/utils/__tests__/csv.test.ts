import { describe, expect, it } from "vitest";
import { buildPredictionsCsv, extractReviewsFromCsvRows, parseCsv } from "../csv";
import type { Prediction } from "../../types";

describe("parseCsv", () => {
  it("parses a simple single-column CSV", () => {
    const text = "review\nAmazing app\nTerrible experience\n";
    const rows = parseCsv(text);

    expect(rows).toEqual([
      ["review"],
      ["Amazing app"],
      ["Terrible experience"],
    ]);
  });

  it("preserves commas inside quoted fields", () => {
    const text = 'review,rating\n"Amazing app, I absolutely love it.",5\n';
    const rows = parseCsv(text);

    expect(rows[1][0]).toBe("Amazing app, I absolutely love it.");
    expect(rows[1][1]).toBe("5");
  });

  it("handles doubled-quote escaping inside a quoted field", () => {
    const text = 'review\n"He said ""great app"" but I disagree."\n';
    const rows = parseCsv(text);

    expect(rows[1][0]).toBe('He said "great app" but I disagree.');
  });

  it("ignores carriage returns and skips fully blank rows", () => {
    const text = "review\r\nAmazing app\r\n\r\nTerrible experience\r\n";
    const rows = parseCsv(text);

    expect(rows).toEqual([
      ["review"],
      ["Amazing app"],
      ["Terrible experience"],
    ]);
  });

  it("supports additional columns beyond review", () => {
    const text = 'review,rating\n"Amazing app, I love it.",5\n"It works fine, nothing special.",3\n';
    const rows = parseCsv(text);

    expect(rows[0]).toEqual(["review", "rating"]);
    expect(rows).toHaveLength(3);
  });

  it("throws on an unclosed quoted field", () => {
    const text = 'review\n"Unterminated quote';

    expect(() => parseCsv(text)).toThrow("CSV contains an unclosed quoted field.");
  });
});

describe("extractReviewsFromCsvRows", () => {
  it("extracts the review column by case-insensitive header match", () => {
    const rows = [
      ["Rating", "Review"],
      ["5", "Amazing app"],
      ["1", "Terrible experience"],
    ];

    expect(extractReviewsFromCsvRows(rows)).toEqual(["Amazing app", "Terrible experience"]);
  });

  it("throws when no review column exists", () => {
    const rows = [["rating"], ["5"]];

    expect(() => extractReviewsFromCsvRows(rows)).toThrow(
      'CSV must contain a column named "review".'
    );
  });

  it("throws when the CSV has no data rows", () => {
    expect(() => extractReviewsFromCsvRows([["review"]])).toThrow(
      "CSV must contain a header and at least one review."
    );
  });

  it("throws when all review cells are empty", () => {
    const rows = [["review"], [""], ["   "]];

    expect(() => extractReviewsFromCsvRows(rows)).toThrow(
      "No valid reviews were found in the CSV."
    );
  });
});

describe("buildPredictionsCsv", () => {
  const prediction: Prediction = {
    review: 'Great app, "highly" recommend',
    normalized_review: 'great app, "highly" recommend',
    sentiment: "positive",
    confidence: 0.91,
    confidence_level: "high",
    prediction_margin: 0.7,
    is_uncertain: false,
    probabilities: { negative: 0.03, neutral: 0.06, positive: 0.91 },
  };

  it("includes the header row with the expected export fields", () => {
    const csv = buildPredictionsCsv([prediction]);
    const [header] = csv.split("\n");

    expect(header).toBe(
      '"review","sentiment","confidence","confidence_level","negative_probability","neutral_probability","positive_probability","prediction_margin","is_uncertain"'
    );
  });

  it("escapes embedded quotes in review text", () => {
    const csv = buildPredictionsCsv([prediction]);

    expect(csv).toContain('"Great app, ""highly"" recommend"');
  });
});
