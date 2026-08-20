import type { SentimentDistributionSummary } from "../../types";
import { formatPercent } from "../../utils/sentimentDisplay";

interface AnalyticsSummaryProps {
  summary: SentimentDistributionSummary;
}

export function AnalyticsSummary({ summary }: AnalyticsSummaryProps) {
  const metrics = [
    { label: "Positive", value: `${summary.positivePct.toFixed(0)}%`, sub: `${summary.positive} reviews` },
    { label: "Neutral", value: `${summary.neutralPct.toFixed(0)}%`, sub: `${summary.neutral} reviews` },
    { label: "Negative", value: `${summary.negativePct.toFixed(0)}%`, sub: `${summary.negative} reviews` },
    { label: "Uncertain", value: `${summary.uncertainPct.toFixed(0)}%`, sub: `${summary.uncertain} reviews` },
  ];

  return (
    <div data-testid="analytics-summary">
      <div className="flex items-baseline justify-between">
        <p className="tabular-nums font-mono text-2xl font-semibold">
          {summary.total} <span className="text-base font-normal text-ink-faint">reviews analyzed</span>
        </p>
        <p className="text-sm text-ink-soft dark:text-ink-dark-soft">
          Avg. confidence{" "}
          <span className="tabular-nums font-mono font-semibold text-ink dark:text-ink-dark">
            {formatPercent(summary.averageConfidence, 0)}
          </span>
        </p>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-px overflow-hidden rounded-md border border-line bg-line dark:border-line-dark dark:bg-line-dark sm:grid-cols-4">
        {metrics.map((metric) => (
          <div key={metric.label} className="bg-surface px-3.5 py-3 dark:bg-surface-dark">
            <p className="text-[11px] uppercase tracking-wide text-ink-faint">{metric.label}</p>
            <p className="tabular-nums font-mono mt-1 text-lg font-semibold">{metric.value}</p>
            <p className="tabular-nums text-xs text-ink-faint">{metric.sub}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
