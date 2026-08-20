import { useState, type KeyboardEvent } from "react";
import { Sparkles } from "lucide-react";
import { Button } from "../common/Button";

const EXAMPLES = [
  "The app looks good but crashes frequently.",
  "Absolutely love the redesign, everything feels faster now.",
  "It's fine. Does what it says, nothing more.",
];

const MAX_LENGTH = 2000;

interface ReviewInputProps {
  onAnalyze: (review: string) => void;
  isLoading: boolean;
}

export function ReviewInput({ onAnalyze, isLoading }: ReviewInputProps) {
  const [value, setValue] = useState("");
  const [validationError, setValidationError] = useState<string | null>(null);

  const trimmedLength = value.trim().length;

  const handleSubmit = () => {
    if (trimmedLength === 0) {
      setValidationError("Enter a review before analyzing.");
      return;
    }
    setValidationError(null);
    onAnalyze(value.trim());
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div>
      <label htmlFor="review-input" className="mb-2 block text-sm font-medium">
        Review text
      </label>

      <textarea
        id="review-input"
        value={value}
        onChange={(event) => {
          setValue(event.target.value.slice(0, MAX_LENGTH));
          if (validationError) setValidationError(null);
        }}
        onKeyDown={handleKeyDown}
        placeholder="Paste a single app review to analyze its sentiment&hellip;"
        maxLength={MAX_LENGTH}
        aria-invalid={Boolean(validationError)}
        aria-describedby="review-char-count"
        className="min-h-[140px] w-full resize-y rounded-md border border-line bg-surface px-3.5 py-3 text-sm leading-relaxed text-ink placeholder:text-ink-faint focus:border-signal dark:border-line-dark dark:bg-surface-dark dark:text-ink-dark"
      />

      <div className="mt-2 flex items-center justify-between">
        <div className="flex flex-wrap gap-1.5">
          {EXAMPLES.map((example) => (
            <button
              key={example}
              onClick={() => setValue(example)}
              className="inline-flex items-center gap-1 rounded-full border border-line px-2.5 py-1 text-xs text-ink-soft transition-colors hover:border-signal hover:text-signal dark:border-line-dark dark:text-ink-dark-soft"
            >
              <Sparkles className="h-3 w-3" aria-hidden="true" />
              Example
            </button>
          ))}
        </div>

        <span
          id="review-char-count"
          className="tabular-nums font-mono text-xs text-ink-faint"
        >
          {value.length}/{MAX_LENGTH}
        </span>
      </div>

      {validationError && (
        <p role="alert" className="mt-2 text-xs text-negative dark:text-negative-dark">
          {validationError}
        </p>
      )}

      <div className="mt-4 flex items-center gap-3">
        <Button
          id="analyze-button"
          data-testid="analyze-button"
          onClick={handleSubmit}
          isLoading={isLoading}
        >
          Analyze sentiment
        </Button>
        <span className="text-xs text-ink-faint">&#8984;/Ctrl + Enter</span>
      </div>
    </div>
  );
}
