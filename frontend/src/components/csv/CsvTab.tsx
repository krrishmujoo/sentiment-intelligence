import { Card } from "../common/Card";
import { ErrorState, LoadingState } from "../common/StateViews";
import { useBatchPrediction } from "../../hooks/useBatchPrediction";
import { CsvUploader } from "./CsvUploader";
import { ResultsWorkspace } from "../results/ResultsWorkspace";
import { downloadPredictionsCsv } from "../../utils/csv";

export function CsvTab() {
  const { predictions, isLoading, error, analyze } = useBatchPrediction();

  return (
    <div className="flex flex-col gap-5">
      <Card className="p-6">
        <CsvUploader onAnalyze={analyze} isLoading={isLoading} />

        <div className="mt-4" id="csv-error">
          {isLoading && <LoadingState label="Analyzing CSV" />}
          {error && !isLoading && <ErrorState message={error} />}
        </div>
      </Card>

      {predictions.length > 0 && !isLoading && (
        <ResultsWorkspace
          predictions={predictions}
          onExport={() => downloadPredictionsCsv(predictions)}
        />
      )}
    </div>
  );
}
