import { AlertTriangle, CheckCircle2 } from "lucide-react";
import type { Prediction } from "../../types";

interface UncertaintyNoticeProps {
  prediction: Prediction;
}

export function UncertaintyNotice({ prediction }: UncertaintyNoticeProps) {
  if (prediction.is_uncertain) {
    return (
      <div className="flex items-start gap-2.5 rounded-md border border-neutral/30 bg-neutral-soft px-3.5 py-3 text-sm dark:border-neutral-dark/30 dark:bg-neutral/10">
        <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0 text-neutral dark:text-neutral-dark" aria-hidden="true" />
        <p className="text-ink dark:text-ink-dark">
          <span className="font-medium">Ambiguous prediction.</span> Multiple sentiment classes
          received similar scores &mdash; this does not necessarily mean the prediction is wrong,
          only that the model found less separation between classes than usual.
        </p>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-2.5 rounded-md border border-positive/30 bg-positive-soft px-3.5 py-3 text-sm dark:border-positive-dark/30 dark:bg-positive/10">
      <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-positive dark:text-positive-dark" aria-hidden="true" />
      <p className="text-ink dark:text-ink-dark">
        Prediction is sufficiently separated from competing classes.
      </p>
    </div>
  );
}
