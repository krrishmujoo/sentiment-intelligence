import { Card } from "../common/Card";
import { ErrorState, LoadingState } from "../common/StateViews";
import { useBatchPrediction } from "../../hooks/useBatchPrediction";
import { BatchInput } from "./BatchInput";
import { ResultsWorkspace } from "../results/ResultsWorkspace";

export function BatchTab() {
  const { predictions, isLoading, error, analyze } = useBatchPrediction();

  return (
    <div className="flex flex-col gap-5">
      <Card className="p-6">
        <BatchInput onAnalyze={analyze} isLoading={isLoading} />

        <div className="mt-4" id="batch-error">
          {isLoading && <LoadingState label="Analyzing batch" />}
          {error && !isLoading && <ErrorState message={error} />}
        </div>
      </Card>

      {predictions.length > 0 && !isLoading && (
        <ResultsWorkspace predictions={predictions} />
      )}
    </div>
  );
}
