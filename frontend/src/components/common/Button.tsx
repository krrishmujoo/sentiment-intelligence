import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Loader2 } from "lucide-react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  isLoading?: boolean;
}

const variantClasses: Record<string, string> = {
  primary:
    "bg-signal text-white hover:bg-signal/90 disabled:bg-signal/50",
  secondary:
    "bg-surface-alt dark:bg-surface-dark-alt text-ink dark:text-ink-dark hover:bg-line dark:hover:bg-line-dark",
  ghost:
    "bg-transparent text-ink-soft dark:text-ink-dark-soft hover:bg-surface-alt dark:hover:bg-surface-dark-alt",
};

export function Button({
  children,
  variant = "primary",
  isLoading = false,
  disabled,
  className = "",
  ...rest
}: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      className={`inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors duration-150 disabled:cursor-not-allowed ${variantClasses[variant]} ${className}`}
      {...rest}
    >
      {isLoading && <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />}
      {children}
    </button>
  );
}
