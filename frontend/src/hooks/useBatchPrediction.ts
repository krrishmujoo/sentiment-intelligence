import { useCallback, useState } from "react";
import { predictBatch } from "../utils/api";
import type { Prediction } from "../types";

export function useBatchPrediction() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (reviews: string[]) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await predictBatch(reviews);
      setPredictions(result.predictions);
    } catch (err) {
      setPredictions([]);
      setError(err instanceof Error ? err.message : "Batch prediction failed.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setPredictions([]);
    setError(null);
  }, []);

  return { predictions, isLoading, error, analyze, reset };
}
