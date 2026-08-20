import type { Sentiment } from "../types";

export const sentimentLabel: Record<Sentiment, string> = {
  positive: "Positive",
  neutral: "Neutral",
  negative: "Negative",
};

export const sentimentTextClass: Record<Sentiment, string> = {
  positive: "text-positive dark:text-positive-dark",
  neutral: "text-neutral dark:text-neutral-dark",
  negative: "text-negative dark:text-negative-dark",
};

export const sentimentBgClass: Record<Sentiment, string> = {
  positive: "bg-positive-soft dark:bg-positive/10",
  neutral: "bg-neutral-soft dark:bg-neutral/10",
  negative: "bg-negative-soft dark:bg-negative/10",
};

export const sentimentBarClass: Record<Sentiment, string> = {
  positive: "bg-positive dark:bg-positive-dark",
  neutral: "bg-neutral dark:bg-neutral-dark",
  negative: "bg-negative dark:bg-negative-dark",
};

export function formatPercent(value: number, decimals = 1): string {
  return `${(value * 100).toFixed(decimals)}%`;
}
