import { Minus, ThumbsDown, ThumbsUp } from "lucide-react";
import type { Sentiment } from "../../types";
import { sentimentBgClass, sentimentLabel, sentimentTextClass } from "../../utils/sentimentDisplay";

const sentimentIcon: Record<Sentiment, typeof ThumbsUp> = {
  positive: ThumbsUp,
  neutral: Minus,
  negative: ThumbsDown,
};

interface SentimentBadgeProps {
  sentiment: Sentiment;
  size?: "sm" | "lg";
}

export function SentimentBadge({ sentiment, size = "lg" }: SentimentBadgeProps) {
  const Icon = sentimentIcon[sentiment];

  return (
    <span
      data-testid="sentiment-badge"
      data-sentiment={sentiment}
      className={`inline-flex items-center gap-1.5 rounded-md font-medium ${sentimentBgClass[sentiment]} ${sentimentTextClass[sentiment]} ${
        size === "lg" ? "px-3 py-1.5 text-sm" : "px-2 py-0.5 text-xs"
      }`}
    >
      <Icon className={size === "lg" ? "h-3.5 w-3.5" : "h-3 w-3"} aria-hidden="true" />
      {sentimentLabel[sentiment]}
    </span>
  );
}
