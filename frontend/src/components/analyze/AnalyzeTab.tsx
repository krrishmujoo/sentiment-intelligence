import { Card } from "../common/Card";
import { ErrorState, LoadingState } from "../common/StateViews";
import { usePrediction } from "../../hooks/usePrediction";
import { ReviewInput } from "./ReviewInput";
import { PredictionResult } from "./PredictionResult";

export function AnalyzeTab() {
  const { prediction, isLoading, error, analyze } = usePrediction();

  return (
    <Card className="p-6">
      <ReviewInput onAnalyze={analyze} isLoading={isLoading} />

      <div className="mt-5" id="error">
        {isLoading && <LoadingState />}
        {error && !isLoading && <ErrorState message={error} />}
      </div>

      {prediction && !isLoading && !error && <PredictionResult prediction={prediction} />}
    </Card>
  );
}
