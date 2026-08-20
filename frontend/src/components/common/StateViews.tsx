import { AlertCircle, Inbox, Loader2 } from "lucide-react";

export function LoadingState({ label = "Analyzing" }: { label?: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="flex items-center gap-2 py-6 text-sm text-ink-soft dark:text-ink-dark-soft"
    >
      <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
      <span>{label}&hellip;</span>
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div
      role="alert"
      className="flex items-start gap-2 rounded-md border border-negative/30 bg-negative-soft px-3 py-2.5 text-sm text-negative dark:border-negative-dark/40 dark:bg-negative/10 dark:text-negative-dark"
    >
      <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" aria-hidden="true" />
      <span>{message}</span>
    </div>
  );
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="flex flex-col items-center gap-2 px-6 py-14 text-center">
      <Inbox className="h-5 w-5 text-ink-faint" aria-hidden="true" />
      <p className="text-sm font-medium text-ink dark:text-ink-dark">{title}</p>
      <p className="max-w-sm text-sm text-ink-soft dark:text-ink-dark-soft">{description}</p>
    </div>
  );
}
