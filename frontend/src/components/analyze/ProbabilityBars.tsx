import type { ClassProbabilities, Sentiment } from "../../types";
import { formatPercent, sentimentBarClass, sentimentLabel } from "../../utils/sentimentDisplay";

const ORDER: Sentiment[] = ["negative", "neutral", "positive"];

interface ProbabilityBarsProps {
  probabilities: ClassProbabilities;
  predicted?: Sentiment;
  compact?: boolean;
}

export function ProbabilityBars({ probabilities, predicted, compact = false }: ProbabilityBarsProps) {
  return (
    <div className="flex flex-col gap-1.5" role="group" aria-label="Class probabilities">
      {ORDER.map((sentiment) => {
        const value = probabilities[sentiment];
        const isPredicted = predicted === sentiment;

        return (
          <div key={sentiment} className="flex items-center gap-2.5">
            <span
              className={`w-16 flex-shrink-0 text-xs ${
                isPredicted ? "font-semibold text-ink dark:text-ink-dark" : "text-ink-soft dark:text-ink-dark-soft"
              }`}
            >
              {sentimentLabel[sentiment]}
            </span>

            <div
              className={`relative flex-1 overflow-hidden rounded-full bg-surface-alt dark:bg-surface-dark-alt ${
                compact ? "h-1.5" : "h-2"
              }`}
            >
              <div
                className={`h-full rounded-full transition-all duration-300 ease-out ${sentimentBarClass[sentiment]}`}
                style={{ width: `${Math.max(value * 100, 1.5)}%` }}
              />
            </div>

            <span className="tabular-nums font-mono w-12 flex-shrink-0 text-right text-xs text-ink-soft dark:text-ink-dark-soft">
              {formatPercent(value)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
