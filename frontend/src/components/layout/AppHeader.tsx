import { Activity, Moon, Sun } from "lucide-react";
import { HealthIndicator } from "./HealthIndicator";

interface AppHeaderProps {
  isDark: boolean;
  onToggleTheme: () => void;
}

export function AppHeader({ isDark, onToggleTheme }: AppHeaderProps) {
  return (
    <header className="border-b border-line dark:border-line-dark">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-signal text-white">
            <Activity className="h-4 w-4" aria-hidden="true" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="font-mono text-[15px] font-semibold tracking-tight">
              Sentiment Intelligence
            </span>
            <span className="hidden text-xs text-ink-faint sm:inline">
              ML-powered review analysis
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <HealthIndicator />
          <button
            onClick={onToggleTheme}
            aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
            className="flex h-7 w-7 items-center justify-center rounded-md text-ink-soft transition-colors hover:bg-surface-alt dark:text-ink-dark-soft dark:hover:bg-surface-dark-alt"
          >
            {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </button>
        </div>
      </div>
    </header>
  );
}
