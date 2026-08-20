import { useCallback, useState } from "react";
import { predictReview } from "../utils/api";
import type { Prediction } from "../types";

export function usePrediction() {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (review: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await predictReview(review);
      setPrediction(result);
    } catch (err) {
      setPrediction(null);
      setError(err instanceof Error ? err.message : "Prediction failed.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setPrediction(null);
    setError(null);
  }, []);

  return { prediction, isLoading, error, analyze, reset };
}
