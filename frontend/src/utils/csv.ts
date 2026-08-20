import type { Prediction } from "../types";

/**
 * RFC4180-style CSV parser, ported 1:1 from the original app.js state
 * machine. Behavior preserved intentionally:
 * - handles quoted fields, including commas inside quotes
 * - handles doubled-quote escaping ("" -> ")
 * - ignores carriage returns
 * - skips fully blank rows
 * - throws on an unclosed quoted field
 */
export function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let insideQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const character = text[i];

    if (insideQuotes) {
      if (character === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          insideQuotes = false;
        }
      } else {
        field += character;
      }
    } else {
      if (character === '"') {
        insideQuotes = true;
      } else if (character === ",") {
        row.push(field.trim());
        field = "";
      } else if (character === "\n") {
        row.push(field.trim());

        if (row.some((value) => value !== "")) {
          rows.push(row);
        }

        row = [];
        field = "";
      } else if (character === "\r") {
        // Ignore carriage return.
      } else {
        field += character;
      }
    }
  }

  if (insideQuotes) {
    throw new Error("CSV contains an unclosed quoted field.");
  }

  row.push(field.trim());

  if (row.some((value) => value !== "")) {
    rows.push(row);
  }

  return rows;
}

/**
 * Extracts review strings from parsed CSV rows by locating a
 * case-insensitive "review" column header. Additional columns
 * (e.g. "rating") are ignored, matching prior behavior.
 */
export function extractReviewsFromCsvRows(rows: string[][]): string[] {
  if (rows.length < 2) {
    throw new Error("CSV must contain a header and at least one review.");
  }

  const headers = rows[0].map((header) => header.trim().toLowerCase());
  const reviewIndex = headers.indexOf("review");

  if (reviewIndex === -1) {
    throw new Error('CSV must contain a column named "review".');
  }

  const reviews: string[] = [];

  for (let i = 1; i < rows.length; i++) {
    const review = rows[i][reviewIndex]?.trim();

    if (review) {
      reviews.push(review);
    }
  }

  if (reviews.length === 0) {
    throw new Error("No valid reviews were found in the CSV.");
  }

  return reviews;
}

function escapeCsvField(value: string | number | boolean): string {
  return `"${String(value).replace(/"/g, '""')}"`;
}

/**
 * Builds the exportable prediction CSV. Field set and quoting behavior
 * match the original app.js download implementation exactly.
 */
export function buildPredictionsCsv(predictions: Prediction[]): string {
  const header = [
    "review",
    "sentiment",
    "confidence",
    "confidence_level",
    "negative_probability",
    "neutral_probability",
    "positive_probability",
    "prediction_margin",
    "is_uncertain",
  ];

  const rows = [header, ...predictions.map((prediction) => [
    prediction.review,
    prediction.sentiment,
    prediction.confidence,
    prediction.confidence_level,
    prediction.probabilities.negative,
    prediction.probabilities.neutral,
    prediction.probabilities.positive,
    prediction.prediction_margin,
    prediction.is_uncertain,
  ])];

  return rows.map((row) => row.map(escapeCsvField).join(",")).join("\n");
}

export function downloadPredictionsCsv(predictions: Prediction[], filename = "sentiment_predictions.csv") {
  const csvContent = buildPredictionsCsv(predictions);
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = filename;

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  URL.revokeObjectURL(url);
}
