import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { SentimentDistributionSummary } from "../../types";
import { sentimentLabel } from "../../utils/sentimentDisplay";

const COLORS = {
  positive: "#1F8A5F",
  neutral: "#8A6D1F",
  negative: "#B23B3B",
};

interface SentimentDistributionProps {
  summary: SentimentDistributionSummary;
}

export function SentimentDistribution({ summary }: SentimentDistributionProps) {
  const data = [
    { key: "positive" as const, value: summary.positive },
    { key: "neutral" as const, value: summary.neutral },
    { key: "negative" as const, value: summary.negative },
  ].filter((entry) => entry.value > 0);

  if (data.length === 0) return null;

  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row sm:gap-6">
      <div className="h-[180px] w-[180px] flex-shrink-0">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="key"
              innerRadius={52}
              outerRadius={80}
              paddingAngle={2}
              stroke="none"
            >
              {data.map((entry) => (
                <Cell key={entry.key} fill={COLORS[entry.key]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value, _name, item) => [
                `${value} reviews`,
                sentimentLabel[
                  (item.payload as { key: keyof typeof sentimentLabel }).key
                ],
              ]}
              contentStyle={{
                borderRadius: 6,
                border: "1px solid #E4E5E9",
                fontSize: 12,
                fontFamily: "Inter, sans-serif",
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <ul className="flex flex-col gap-2 text-sm">
        {data.map((entry) => (
          <li key={entry.key} className="flex items-center gap-2">
            <span
              className="h-2.5 w-2.5 flex-shrink-0 rounded-full"
              style={{ backgroundColor: COLORS[entry.key] }}
              aria-hidden="true"
            />
            <span className="text-ink-soft dark:text-ink-dark-soft">{sentimentLabel[entry.key]}</span>
            <span className="tabular-nums font-mono font-medium">{entry.value}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
