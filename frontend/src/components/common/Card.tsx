import type { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ children, className = "", ...rest }: CardProps) {
  return (
    <div
      className={`rounded-lg border border-line dark:border-line-dark bg-surface dark:bg-surface-dark shadow-panel ${className}`}
      {...rest}
    >
      {children}
    </div>
  );
}
