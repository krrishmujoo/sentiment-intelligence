import { useState } from "react";
import { Button } from "../common/Button";

interface BatchInputProps {
  onAnalyze: (reviews: string[]) => void;
  isLoading: boolean;
}

export function BatchInput({ onAnalyze, isLoading }: BatchInputProps) {
  const [value, setValue] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  const reviewCount = value
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0).length;

  const handleSubmit = () => {
    const reviews = value
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

    if (reviews.length === 0) {
      setValidationError("Enter at least one review, one per line.");
      return;
    }

    setValidationError(null);
    onAnalyze(reviews);
  };

  return (
    <div>
      <label htmlFor="batch-input" className="mb-2 block text-sm font-medium">
        Reviews
        <span className="ml-1.5 font-normal text-ink-faint">(one per line)</span>
      </label>

      <textarea
        id="batch-input"
        value={value}
        onChange={(event) => {
          setValue(event.target.value);
          if (validationError) setValidationError(null);
        }}
        placeholder={"Amazing app\nTerrible experience\nIt works fine"}
        className="min-h-[180px] w-full resize-y rounded-md border border-line bg-surface px-3.5 py-3 text-sm leading-relaxed text-ink placeholder:text-ink-faint focus:border-signal dark:border-line-dark dark:bg-surface-dark dark:text-ink-dark"
      />

      <div className="mt-2 flex items-center justify-between">
        <span className="tabular-nums font-mono text-xs text-ink-faint">
          {reviewCount} review{reviewCount === 1 ? "" : "s"} detected
        </span>
      </div>

      {validationError && (
        <p role="alert" className="mt-2 text-xs text-negative dark:text-negative-dark">
          {validationError}
        </p>
      )}

      <div className="mt-4">
        <Button
          id="batch-button"
          data-testid="batch-button"
          onClick={handleSubmit}
          isLoading={isLoading}
        >
          Analyze batch
        </Button>
      </div>
    </div>
  );
}
