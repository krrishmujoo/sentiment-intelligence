import { Fragment, useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import type { Prediction } from "../../types";
import { formatPercent } from "../../utils/sentimentDisplay";
import { SentimentBadge } from "../analyze/SentimentBadge";
import { ProbabilityBars } from "../analyze/ProbabilityBars";

interface ReviewTableProps {
  predictions: Prediction[];
}

export function ReviewTable({ predictions }: ReviewTableProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (predictions.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-ink-faint">
        No reviews match the current filters.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-faint dark:border-line-dark">
            <th className="py-2 pr-3 font-medium">Review</th>
            <th className="py-2 pr-3 font-medium">Sentiment</th>
            <th className="py-2 pr-3 font-medium">Confidence</th>
            <th className="py-2 pr-3 font-medium">Margin</th>
            <th className="py-2 pr-3 font-medium">Uncertain</th>
            <th className="w-8 py-2" />
          </tr>
        </thead>
        <tbody data-testid="review-table-body">
          {predictions.map((prediction, index) => {
            const isExpanded = expandedIndex === index;

            return (
              <Fragment key={index}>
                <tr
                  data-testid="review-row"
                  className="cursor-pointer border-b border-line last:border-b-0 hover:bg-surface-alt dark:border-line-dark dark:hover:bg-surface-dark-alt"
                  onClick={() => setExpandedIndex(isExpanded ? null : index)}
                >
                  <td className="max-w-xs py-2.5 pr-3 align-top">
                    <p className="line-clamp-2 text-ink dark:text-ink-dark">{prediction.review}</p>
                  </td>
                  <td className="py-2.5 pr-3 align-top">
                    <SentimentBadge sentiment={prediction.sentiment} size="sm" />
                  </td>
                  <td className="tabular-nums font-mono py-2.5 pr-3 align-top">
                    {formatPercent(prediction.confidence)}
                  </td>
                  <td className="tabular-nums font-mono py-2.5 pr-3 align-top">
                    {formatPercent(prediction.prediction_margin)}
                  </td>
                  <td className="py-2.5 pr-3 align-top">
                    {prediction.is_uncertain ? (
                      <span className="text-neutral dark:text-neutral-dark">Yes</span>
                    ) : (
                      <span className="text-ink-faint">No</span>
                    )}
                  </td>
                  <td className="py-2.5 align-top text-ink-faint">
                    {isExpanded ? (
                      <ChevronUp className="h-4 w-4" aria-hidden="true" />
                    ) : (
                      <ChevronDown className="h-4 w-4" aria-hidden="true" />
                    )}
                  </td>
                </tr>
                {isExpanded && (
                  <tr className="border-b border-line bg-surface-alt dark:border-line-dark dark:bg-surface-dark-alt">
                    <td colSpan={6} className="px-3 py-4">
                      <div className="max-w-md">
                        <ProbabilityBars
                          probabilities={prediction.probabilities}
                          predicted={prediction.sentiment}
                          compact
                        />
                      </div>
                    </td>
                  </tr>
                )}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
