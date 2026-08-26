import { useCallback, useState } from "react";
import { analyzeBusinessQuestion } from "../utils/api";
import type { AnalyzeResponse, Prediction } from "../types";

const DEFAULT_QUESTION = "What should the product team focus on first?";

export function useBusinessInsights() {
  const [question, setQuestion] = useState(DEFAULT_QUESTION);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = useCallback(
    async (predictions: Prediction[]) => {
      const trimmedQuestion = question.trim();

      if (!trimmedQuestion) {
        setError("Enter a business question before generating insights.");
        return;
      }

      if (predictions.length === 0) {
        setError("Run a batch analysis first — insights need existing predictions.");
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const response = await analyzeBusinessQuestion(trimmedQuestion, predictions);
        setResult(response);
      } catch (err) {
        setResult(null);
        setError(err instanceof Error ? err.message : "Business insight generation failed.");
      } finally {
        setIsLoading(false);
      }
    },
    [question],
  );

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { question, setQuestion, result, isLoading, error, generate, reset };
}