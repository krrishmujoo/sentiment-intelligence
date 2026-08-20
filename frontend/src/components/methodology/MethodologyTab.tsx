import { Card } from "../common/Card";

const steps = [
  { title: "Normalization", detail: "Lowercase, trim, and collapse repeated whitespace." },
  { title: "Vectorization", detail: "TF-IDF representation using unigrams and bigrams." },
  { title: "Classification", detail: "Balanced logistic regression across three classes." },
  { title: "Uncertainty check", detail: "Flags predictions with low confidence or a narrow margin between the top two classes." },
];

export function MethodologyTab() {
  return (
    <Card className="p-6">
      <h2 className="text-sm font-semibold">Model methodology</h2>
      <p className="mt-1.5 max-w-2xl text-sm text-ink-soft dark:text-ink-dark-soft">
        Every review passes through the same fixed pipeline. Nothing shown elsewhere in this
        product is inferred beyond what this pipeline returns.
      </p>

      <ol className="mt-6 flex flex-col gap-4">
        {steps.map((step, index) => (
          <li key={step.title} className="flex gap-3.5">
            <span className="tabular-nums font-mono flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-surface-alt text-xs font-medium text-ink-soft dark:bg-surface-dark-alt dark:text-ink-dark-soft">
              {index + 1}
            </span>
            <div>
              <p className="text-sm font-medium">{step.title}</p>
              <p className="text-sm text-ink-soft dark:text-ink-dark-soft">{step.detail}</p>
            </div>
          </li>
        ))}
      </ol>

      <div className="mt-6 rounded-md border border-line bg-surface-alt px-3.5 py-3 text-xs text-ink-soft dark:border-line-dark dark:bg-surface-dark-alt dark:text-ink-dark-soft">
        This product does not expose feature-level or word-level explanations for individual
        predictions. Confidence, prediction margin, and class probabilities are the only signals
        the underlying model provides, and they are shown as returned&mdash;nothing here is
        inferred from the text content itself beyond the model's own output.
      </div>
    </Card>
  );
}
