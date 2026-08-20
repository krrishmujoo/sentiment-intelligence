export type TabId = "analyze" | "batch" | "csv" | "methodology";

interface TabNavProps {
  active: TabId;
  onChange: (tab: TabId) => void;
}

const tabs: { id: TabId; label: string }[] = [
  { id: "analyze", label: "Analyze" },
  { id: "batch", label: "Batch Intelligence" },
  { id: "csv", label: "CSV Workspace" },
  { id: "methodology", label: "Methodology" },
];

export function TabNav({ active, onChange }: TabNavProps) {
  return (
    <nav
      aria-label="Primary"
      className="border-b border-line dark:border-line-dark"
    >
      <div className="mx-auto flex max-w-5xl gap-1 px-6">
        {tabs.map((tab) => {
          const isActive = tab.id === active;
          return (
            <button
              key={tab.id}
              onClick={() => onChange(tab.id)}
              aria-current={isActive ? "page" : undefined}
              className={`relative px-3 py-3 text-sm font-medium transition-colors ${
                isActive
                  ? "text-ink dark:text-ink-dark"
                  : "text-ink-faint hover:text-ink-soft dark:hover:text-ink-dark-soft"
              }`}
            >
              {tab.label}
              {isActive && (
                <span className="absolute inset-x-3 -bottom-px h-0.5 rounded-full bg-signal" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
