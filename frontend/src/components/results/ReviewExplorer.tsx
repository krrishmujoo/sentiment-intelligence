import { useMemo, useState } from "react";
import { ArrowDownUp, Search } from "lucide-react";
import type { Prediction, SentimentFilter, SortDirection, SortField } from "../../types";
import { ReviewTable } from "./ReviewTable";

interface ReviewExplorerProps {
  predictions: Prediction[];
}

const filterOptions: { id: SentimentFilter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "positive", label: "Positive" },
  { id: "neutral", label: "Neutral" },
  { id: "negative", label: "Negative" },
];

export function ReviewExplorer({ predictions }: ReviewExplorerProps) {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<SentimentFilter>("all");
  const [uncertainOnly, setUncertainOnly] = useState(false);
  const [sortField, setSortField] = useState<SortField>("confidence");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const filtered = useMemo(() => {
    let result = predictions;

    if (filter !== "all") {
      result = result.filter((p) => p.sentiment === filter);
    }

    if (uncertainOnly) {
      result = result.filter((p) => p.is_uncertain);
    }

    if (query.trim()) {
      const lowerQuery = query.trim().toLowerCase();
      result = result.filter((p) => p.review.toLowerCase().includes(lowerQuery));
    }

    const sorted = [...result].sort((a, b) => {
      let comparison = 0;

      if (sortField === "review") {
        comparison = a.review.localeCompare(b.review);
      } else {
        comparison = a[sortField] - b[sortField];
      }

      return sortDirection === "asc" ? comparison : -comparison;
    });

    return sorted;
  }, [predictions, filter, uncertainOnly, query, sortField, sortDirection]);

  const toggleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  return (
    <div>
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative flex-1 sm:max-w-xs">
          <Search
            className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-ink-faint"
            aria-hidden="true"
          />
          <input
            type="text"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search reviews&hellip;"
            aria-label="Search reviews"
            className="w-full rounded-md border border-line bg-surface py-1.5 pl-8 pr-3 text-sm focus:border-signal dark:border-line-dark dark:bg-surface-dark"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex rounded-md border border-line p-0.5 dark:border-line-dark" role="group" aria-label="Filter by sentiment">
            {filterOptions.map((option) => (
              <button
                key={option.id}
                onClick={() => setFilter(option.id)}
                aria-pressed={filter === option.id}
                className={`rounded px-2.5 py-1 text-xs font-medium transition-colors ${
                  filter === option.id
                    ? "bg-signal text-white"
                    : "text-ink-soft hover:bg-surface-alt dark:text-ink-dark-soft dark:hover:bg-surface-dark-alt"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>

          <label className="flex items-center gap-1.5 text-xs text-ink-soft dark:text-ink-dark-soft">
            <input
              type="checkbox"
              checked={uncertainOnly}
              onChange={(event) => setUncertainOnly(event.target.checked)}
              className="h-3.5 w-3.5 rounded border-line accent-signal dark:border-line-dark"
            />
            Uncertain only
          </label>

          <div className="flex items-center gap-1 text-xs text-ink-faint">
            <ArrowDownUp className="h-3 w-3" aria-hidden="true" />
            <button
              onClick={() => toggleSort("confidence")}
              className={`underline-offset-2 hover:underline ${sortField === "confidence" ? "font-medium text-ink dark:text-ink-dark" : ""}`}
            >
              Confidence
            </button>
            <span>&middot;</span>
            <button
              onClick={() => toggleSort("prediction_margin")}
              className={`underline-offset-2 hover:underline ${sortField === "prediction_margin" ? "font-medium text-ink dark:text-ink-dark" : ""}`}
            >
              Margin
            </button>
          </div>
        </div>
      </div>

      <ReviewTable predictions={filtered} />
    </div>
  );
}
