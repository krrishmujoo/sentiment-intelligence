import type { Prediction } from "../../types";
import { formatPercent } from "../../utils/sentimentDisplay";
import {
  getHighestConfidenceReviews,
  getMostAmbiguousReviews,
} from "../../utils/analytics";
import { SentimentBadge } from "../analyze/SentimentBadge";

function InsightList({ title, items }: { title: string; items: Prediction[] }) {
  if (items.length === 0) return null;

  return (
    <div>
      <p className="mb-2.5 text-xs font-medium uppercase tracking-wide text-ink-faint">{title}</p>
      <ul className="flex flex-col gap-2">
        {items.map((item, index) => (
          <li
            key={`${item.review}-${index}`}
            className="flex items-start justify-between gap-3 rounded-md border border-line px-3 py-2.5 dark:border-line-dark"
          >
            <p className="line-clamp-2 flex-1 text-sm text-ink dark:text-ink-dark">{item.review}</p>
            <div className="flex flex-shrink-0 flex-col items-end gap-1">
              <SentimentBadge sentiment={item.sentiment} size="sm" />
              <span className="tabular-nums font-mono text-xs text-ink-faint">
                {formatPercent(item.confidence)}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

interface ReviewInsightsProps {
  predictions: Prediction[];
}

export function ReviewInsights({ predictions }: ReviewInsightsProps) {
  const mostConfidentPositive = getHighestConfidenceReviews(predictions, "positive", 3);
  const mostConfidentNegative = getHighestConfidenceReviews(predictions, "negative", 3);
  const mostAmbiguous = getMostAmbiguousReviews(predictions, 3);

  if (
    mostConfidentPositive.length === 0 &&
    mostConfidentNegative.length === 0 &&
    mostAmbiguous.length === 0
  ) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <InsightList title="Most confident positive" items={mostConfidentPositive} />
      <InsightList title="Most confident negative" items={mostConfidentNegative} />
      <InsightList title="Most ambiguous" items={mostAmbiguous} />
    </div>
  );
}
