import { useState } from "react";
import { ChevronDown, ListTree } from "lucide-react";
import type { AnalysisPlan, PlannerOperationName } from "../../types";

const OPERATION_LABELS: Record<PlannerOperationName, string> = {
  summarize_sentiment: "Sentiment Summary",
  rank_priority_issues: "Priority Issue Ranking",
  summarize_themes: "Theme Summary",
  filter_negative_themes: "Negative Theme Analysis",
  filter_positive_themes: "Positive Theme Analysis",
  summarize_uncertainty: "Uncertainty Summary",
};

interface AnalysisDetailsProps {
  plan: AnalysisPlan;
}

export function AnalysisDetails({ plan }: AnalysisDetailsProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border-t border-line pt-3 dark:border-line-dark">
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        className="flex w-full items-center justify-between text-left text-xs font-medium text-ink-soft hover:text-ink dark:text-ink-dark-soft dark:hover:text-ink-dark"
      >
        <span className="flex items-center gap-1.5">
          <ListTree className="h-3.5 w-3.5" aria-hidden="true" />
          How this answer was generated
        </span>
        <ChevronDown
          className={`h-3.5 w-3.5 transition-transform ${isOpen ? "rotate-180" : ""}`}
          aria-hidden="true"
        />
      </button>

      {isOpen && (
        <div className="animate-fade-in mt-3 flex flex-col gap-2 text-xs text-ink-soft dark:text-ink-dark-soft">
          <div>
            <span className="font-medium text-ink dark:text-ink-dark">Intent: </span>
            <span className="font-mono">{plan.intent}</span>
          </div>

          {plan.operations.length > 0 && (
            <div>
              <span className="font-medium text-ink dark:text-ink-dark">Analysis used:</span>
              <ul className="mt-1 list-disc pl-4">
                {plan.operations.map((op, index) => (
                  <li key={`${op.operation}-${index}`}>{OPERATION_LABELS[op.operation]}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}