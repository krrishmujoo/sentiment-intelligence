import type { Prediction } from "../../types";
import { formatPercent } from "../../utils/sentimentDisplay";
import { SentimentBadge } from "./SentimentBadge";
import { ProbabilityBars } from "./ProbabilityBars";
import { ModelSignals } from "./ModelSignals";
import { UncertaintyNotice } from "./UncertaintyNotice";

interface PredictionResultProps {
  prediction: Prediction;
}

export function PredictionResult({ prediction }: PredictionResultProps) {
  return (
    <div
      id="result"
      className="animate-slide-up flex flex-col gap-5 border-t border-line pt-5 dark:border-line-dark"
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <SentimentBadge sentiment={prediction.sentiment} />
          <span
            data-testid="confidence-value"
            className="tabular-nums font-mono text-sm text-ink-soft dark:text-ink-dark-soft"
          >
            {formatPercent(prediction.confidence)} confidence
          </span>
        </div>
      </div>

      <div>
        <p className="mb-2.5 text-xs font-medium uppercase tracking-wide text-ink-faint">
          Class probabilities
        </p>
        <ProbabilityBars probabilities={prediction.probabilities} predicted={prediction.sentiment} />
      </div>

      <div>
        <p className="mb-2.5 text-xs font-medium uppercase tracking-wide text-ink-faint">
          Model signals
        </p>
        <ModelSignals prediction={prediction} />
      </div>

      <UncertaintyNotice prediction={prediction} />
    </div>
  );
}
