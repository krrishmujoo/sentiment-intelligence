import { FileSearch } from "lucide-react";
import type { InsightObservation } from "../../types";

interface ObservationCardProps {
  observation: InsightObservation;
}

export function ObservationCard({ observation }: ObservationCardProps) {
  return (
    <div className="rounded-md border border-line bg-surface-alt p-4 dark:border-line-dark dark:bg-surface-dark-alt">
      <div className="flex items-start gap-2">
        <FileSearch
          className="mt-0.5 h-4 w-4 flex-shrink-0 text-signal dark:text-signal-dark"
          aria-hidden="true"
        />
        <div className="flex-1">
          <h4 className="text-sm font-semibold text-ink dark:text-ink-dark">{observation.title}</h4>
          <p className="mt-1 text-sm text-ink-soft dark:text-ink-dark-soft">{observation.description}</p>

          {observation.evidence.length > 0 && (
            <ul className="mt-3 flex flex-col gap-1 border-l-2 border-signal/30 pl-3 dark:border-signal-dark/40">
              {observation.evidence.map((item, index) => (
                <li key={index} className="text-xs text-ink-faint dark:text-ink-dark-soft">
                  {item}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}