import type { Prediction } from "../../types";
import { calculateSentimentDistribution } from "../../utils/analytics";
import { Card } from "../common/Card";
import { AnalyticsSummary } from "./AnalyticsSummary";
import { SentimentDistribution } from "./SentimentDistribution";
import { ReviewInsights } from "./ReviewInsights";
import { ReviewExplorer } from "./ReviewExplorer";
import { ExportCsvButton } from "./ExportCsvButton";
import { BusinessInsightsPanel } from "../insights/BusinessInsightsPanel";

interface ResultsWorkspaceProps {
  predictions: Prediction[];
  onExport?: () => void;
}

export function ResultsWorkspace({ predictions, onExport }: ResultsWorkspaceProps) {
  const summary = calculateSentimentDistribution(predictions);

  return (
    <div
      id={onExport ? "csv-results" : "batch-results"}
      data-testid="results-workspace"
      className="animate-fade-in flex flex-col gap-5"
    >
      <Card className="p-6">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex-1">
            <AnalyticsSummary summary={summary} />
          </div>
          <SentimentDistribution summary={summary} />
        </div>
      </Card>

      <BusinessInsightsPanel predictions={predictions} />

      <Card className="p-6">
        <ReviewInsights predictions={predictions} />
      </Card>

      <Card className="p-6">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-sm font-semibold">Review explorer</h3>
          {onExport && <ExportCsvButton onExport={onExport} />}
        </div>
        <ReviewExplorer predictions={predictions} />
      </Card>
    </div>
  );
}