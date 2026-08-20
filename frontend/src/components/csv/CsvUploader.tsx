import { useRef, useState } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { Button } from "../common/Button";
import { extractReviewsFromCsvRows, parseCsv } from "../../utils/csv";

interface CsvUploaderProps {
  onAnalyze: (reviews: string[]) => void;
  isLoading: boolean;
}

export function CsvUploader({ onAnalyze, isLoading }: CsvUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [reviews, setReviews] = useState<string[] | null>(null);
  const [parseError, setParseError] = useState<string | null>(null);

  const handleFileChange = async (file: File) => {
    setParseError(null);
    setReviews(null);
    setFileName(file.name);

    try {
      const text = await file.text();
      const rows = parseCsv(text);
      const parsedReviews = extractReviewsFromCsvRows(rows);
      setReviews(parsedReviews);
    } catch (err) {
      setReviews(null);
      setParseError(err instanceof Error ? err.message : "Unable to parse CSV file.");
    }
  };

  return (
    <div>
      <label className="mb-2 block text-sm font-medium">
        CSV file
        <span className="ml-1.5 font-normal text-ink-faint">
          (must contain a &ldquo;review&rdquo; column)
        </span>
      </label>

      <div
        className="flex flex-col items-center gap-2 rounded-md border border-dashed border-line px-6 py-8 text-center dark:border-line-dark"
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          const file = event.dataTransfer.files?.[0];
          if (file) handleFileChange(file);
        }}
      >
        <UploadCloud className="h-5 w-5 text-ink-faint" aria-hidden="true" />
        <p className="text-sm text-ink-soft dark:text-ink-dark-soft">
          Drop a CSV here, or{" "}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="font-medium text-signal underline underline-offset-2"
          >
            browse files
          </button>
        </p>
        <input
          ref={fileInputRef}
          id="csv-file"
          type="file"
          accept=".csv"
          className="sr-only"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) handleFileChange(file);
          }}
        />
      </div>

      {fileName && !parseError && (
        <div className="mt-3 flex items-center gap-2 rounded-md bg-surface-alt px-3 py-2 text-sm dark:bg-surface-dark-alt">
          <FileText className="h-4 w-4 flex-shrink-0 text-ink-faint" aria-hidden="true" />
          <span className="truncate font-medium">{fileName}</span>
          {reviews && (
            <span className="tabular-nums font-mono ml-auto flex-shrink-0 text-ink-faint">
              {reviews.length} review{reviews.length === 1 ? "" : "s"} parsed
            </span>
          )}
        </div>
      )}

      {parseError && (
        <p role="alert" className="mt-3 text-xs text-negative dark:text-negative-dark">
          {parseError}
        </p>
      )}

      <div className="mt-4">
        <Button
          id="csv-button"
          data-testid="csv-button"
          onClick={() => reviews && onAnalyze(reviews)}
          disabled={!reviews || reviews.length === 0}
          isLoading={isLoading}
        >
          Analyze CSV
        </Button>
      </div>
    </div>
  );
}
