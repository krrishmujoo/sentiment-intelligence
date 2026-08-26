import type { InsightPriority } from "../../types";

const PRIORITY_STYLES: Record<InsightPriority, string> = {
  high: "bg-negative-soft text-negative dark:bg-negative/10 dark:text-negative-dark",
  medium: "bg-neutral-soft text-neutral dark:bg-neutral/10 dark:text-neutral-dark",
  low: "bg-surface-alt text-ink-soft dark:bg-surface-dark-alt dark:text-ink-dark-soft",
};

const PRIORITY_LABELS: Record<InsightPriority, string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
};

interface PriorityBadgeProps {
  priority: InsightPriority;
}

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${PRIORITY_STYLES[priority]}`}
    >
      {PRIORITY_LABELS[priority]}
    </span>
  );
}