import { AnimatePresence, motion } from "framer-motion";
import { Sparkles, ShieldCheck } from "lucide-react";
import type { Prediction } from "../../types";
import { useBusinessInsights } from "../../hooks/useBusinessInsights";
import { Card } from "../common/Card";
import { EmptyState, ErrorState, LoadingState } from "../common/StateViews";
import { ObservationCard } from "./ObservationCard";
import { RecommendationCard } from "./RecommendationCard";
import { AnalysisDetails } from "./AnalysisDetails";

interface BusinessInsightsPanelProps {
  predictions: Prediction[];
}

export function BusinessInsightsPanel({ predictions }: BusinessInsightsPanelProps) {
  const { question, setQuestion, result, isLoading, error, generate } = useBusinessInsights();

  const hasPredictions = predictions.length > 0;

  const handleGenerate = () => {
    void generate(predictions);
  };

  return (
    <Card className="p-6" data-testid="business-insights-panel">
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-signal dark:text-signal-dark" aria-hidden="true" />
          <h3 className="text-sm font-semibold text-ink dark:text-ink-dark">AI Business Insights</h3>
        </div>
        <p className="text-sm text-ink-soft dark:text-ink-dark-soft">
          Ask a business question about this batch and get a grounded summary, observations, and
          recommended actions.
        </p>
      </div>

      <div className="mt-4 flex flex-col gap-2 sm:flex-row">
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={!hasPredictions || isLoading}
          placeholder="What should the product team fix first?"
          aria-label="Business question"
          className="flex-1 rounded-md border border-line bg-canvas px-3 py-2 text-sm text-ink placeholder:text-ink-faint focus:outline-none focus:ring-2 focus:ring-signal disabled:cursor-not-allowed disabled:opacity-60 dark:border-line-dark dark:bg-canvas-dark dark:text-ink-dark"
        />
        <button
          type="button"
          onClick={handleGenerate}
          disabled={!hasPredictions || isLoading || question.trim().length === 0}
          className="inline-flex items-center justify-center gap-1.5 rounded-md bg-signal px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-signal/90 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-signal-dark dark:hover:bg-signal-dark/90"
        >
          <Sparkles className="h-3.5 w-3.5" aria-hidden="true" />
          Generate Insights
        </button>
      </div>

      <div
        className="mt-3 flex items-center gap-1.5 text-xs text-ink-faint dark:text-ink-dark-soft"
        title="Customer review text is analyzed locally. The AI reasoning layer receives privacy-safe aggregate analytics rather than the raw review dataset."
      >
        <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
        <span>Privacy-aware analysis</span>
      </div>

      <div className="mt-4">
        {!hasPredictions && (
          <EmptyState
            title="No predictions yet"
            description="Run a batch analysis above to unlock AI business insights."
          />
        )}

        {hasPredictions && isLoading && <LoadingState label="Generating insights" />}

        {hasPredictions && error && !isLoading && (
          <div className="flex flex-col gap-3">
            <ErrorState message={error} />
            <button
              type="button"
              onClick={handleGenerate}
              className="self-start text-sm font-medium text-signal hover:underline dark:text-signal-dark"
            >
              Try again
            </button>
          </div>
        )}

        <AnimatePresence>
          {hasPredictions && result && !isLoading && !error && (
            <motion.div
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.18 }}
              className="flex flex-col gap-6"
            >
              <div className="rounded-md bg-surface-alt p-4 dark:bg-surface-dark-alt">
                <h4 className="text-xs font-semibold uppercase tracking-wide text-ink-faint dark:text-ink-dark-soft">
                  Executive Summary
                </h4>
                <p className="mt-2 text-sm leading-relaxed text-ink dark:text-ink-dark">
                  {result.insights.summary}
                </p>
              </div>

              {result.insights.observations.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-faint dark:text-ink-dark-soft">
                    Data-Grounded Observations
                  </h4>
                  <div className="flex flex-col gap-2">
                    {result.insights.observations.map((observation, index) => (
                      <ObservationCard key={index} observation={observation} />
                    ))}
                  </div>
                </div>
              )}

              {result.insights.recommendations.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-faint dark:text-ink-dark-soft">
                    AI-Generated Recommendations
                  </h4>
                  <div className="flex flex-col gap-2">
                    {result.insights.recommendations.map((recommendation, index) => (
                      <RecommendationCard key={index} recommendation={recommendation} />
                    ))}
                  </div>
                </div>
              )}

              <AnalysisDetails plan={result.plan} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </Card>
  );
}