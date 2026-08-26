import { Lightbulb } from "lucide-react";
import type { InsightRecommendation } from "../../types";
import { PriorityBadge } from "./PriorityBadge";

interface RecommendationCardProps {
  recommendation: InsightRecommendation;
}

export function RecommendationCard({ recommendation }: RecommendationCardProps) {
  return (
    <div className="rounded-md border border-signal/30 bg-signal-soft p-4 dark:border-signal-dark/30 dark:bg-signal-dark/10">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-start gap-2">
          <Lightbulb
            className="mt-0.5 h-4 w-4 flex-shrink-0 text-signal dark:text-signal-dark"
            aria-hidden="true"
          />
          <h4 className="text-sm font-semibold text-ink dark:text-ink-dark">{recommendation.title}</h4>
        </div>
        <PriorityBadge priority={recommendation.priority} />
      </div>

      <p className="mt-2 text-sm text-ink dark:text-ink-dark">{recommendation.action}</p>
      <p className="mt-1.5 text-xs text-ink-soft dark:text-ink-dark-soft">{recommendation.rationale}</p>
    </div>
  );
}