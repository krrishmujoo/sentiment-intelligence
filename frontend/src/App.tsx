import { useEffect, useState, type ComponentType } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { AppHeader } from "./components/layout/AppHeader";
import { TabNav, type TabId } from "./components/layout/TabNav";
import { AnalyzeTab } from "./components/analyze/AnalyzeTab";
import { BatchTab } from "./components/batch/BatchTab";
import { CsvTab } from "./components/csv/CsvTab";
import { MethodologyTab } from "./components/methodology/MethodologyTab";

const tabComponents: Record<TabId, ComponentType> = {
  analyze: AnalyzeTab,
  batch: BatchTab,
  csv: CsvTab,
  methodology: MethodologyTab,
};

function getInitialTheme(): boolean {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<TabId>("analyze");
  const [isDark, setIsDark] = useState(getInitialTheme);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
  }, [isDark]);

  const ActiveComponent = tabComponents[activeTab];

  return (
    <div className="min-h-screen bg-canvas dark:bg-canvas-dark">
      <AppHeader isDark={isDark} onToggleTheme={() => setIsDark((prev) => !prev)} />
      <TabNav active={activeTab} onChange={setActiveTab} />

      <main className="mx-auto max-w-5xl px-6 py-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
          >
            <ActiveComponent />
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}
