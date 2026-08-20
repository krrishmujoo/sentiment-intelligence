import type { Prediction } from "../../types";
import { formatPercent } from "../../utils/sentimentDisplay";

const levelLabel: Record<Prediction["confidence_level"], string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
};

interface ModelSignalsProps {
  prediction: Prediction;
}

export function ModelSignals({ prediction }: ModelSignalsProps) {
  const signals = [
    { label: "Confidence", value: formatPercent(prediction.confidence) },
    { label: "Prediction margin", value: formatPercent(prediction.prediction_margin) },
    { label: "Reliability", value: levelLabel[prediction.confidence_level] },
    { label: "Uncertain", value: prediction.is_uncertain ? "Yes" : "No" },
  ];

  return (
    <div className="grid grid-cols-2 gap-px overflow-hidden rounded-md border border-line bg-line dark:border-line-dark dark:bg-line-dark sm:grid-cols-4">
      {signals.map((signal) => (
        <div key={signal.label} className="bg-surface px-3.5 py-3 dark:bg-surface-dark">
          <p className="text-[11px] uppercase tracking-wide text-ink-faint">{signal.label}</p>
          <p className="tabular-nums font-mono mt-1 text-base font-semibold">{signal.value}</p>
        </div>
      ))}
    </div>
  );
}
