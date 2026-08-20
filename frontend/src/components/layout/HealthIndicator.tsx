import { useHealth } from "../../hooks/useHealth";

const stateConfig = {
  checking: { dot: "bg-ink-faint", label: "Checking API" },
  online: { dot: "bg-positive dark:bg-positive-dark", label: "Model online" },
  offline: { dot: "bg-negative dark:bg-negative-dark", label: "API unavailable" },
};

export function HealthIndicator() {
  const state = useHealth();
  const config = stateConfig[state];

  return (
    <div className="flex items-center gap-1.5 text-xs text-ink-soft dark:text-ink-dark-soft">
      <span
        className={`h-1.5 w-1.5 rounded-full ${config.dot} ${state === "checking" ? "animate-pulse" : ""}`}
        aria-hidden="true"
      />
      <span>{config.label}</span>
    </div>
  );
}
