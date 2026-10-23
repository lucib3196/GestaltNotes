import {
  FiAlertCircle,
  FiCheckCircle,
  FiCircle,
  FiClock,
  FiLoader,
  FiRefreshCw,
} from "react-icons/fi";
import type { DisplayStatus } from "../processingStatus";

const badgeStyles = {
  processed: {
    label: "Processed",
    Icon: FiCheckCircle,
    tone: "bg-accent/10 text-accent",
  },
  idle: {
    label: "Not processed",
    Icon: FiCircle,
    tone: "bg-surface-muted text-text-muted",
  },
  starting: {
    label: "Starting…",
    Icon: FiLoader,
    tone: "bg-accent/10 text-accent",
  },
  queued: {
    label: "Queued",
    Icon: FiClock,
    tone: "bg-surface-muted text-text-muted",
  },
  running: {
    label: "Processing…",
    Icon: FiLoader,
    tone: "bg-accent/10 text-accent",
  },
  retrying: {
    label: "Retrying…",
    Icon: FiRefreshCw,
    tone: "bg-accent/10 text-accent",
  },
  failed: {
    label: "Processing failed",
    Icon: FiAlertCircle,
    tone: "bg-red-500/10 text-red-600 dark:text-red-400",
  },
  revoked: {
    label: "Processing cancelled",
    Icon: FiCircle,
    tone: "bg-surface-muted text-text-muted",
  },
  checking: {
    label: "Checking result…",
    Icon: FiLoader,
    tone: "bg-accent/10 text-accent",
  },
};

export function ProcessingBadge({ status }: { status: DisplayStatus }) {
  const { label, Icon, tone } = badgeStyles[status];
  const spinning = ["starting", "running", "retrying", "checking"].includes(
    status,
  );
  return (
    <span
      role="status"
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${tone}`}
    >
      <Icon
        aria-hidden="true"
        className={spinning ? "motion-safe:animate-spin" : undefined}
      />
      {label}
    </span>
  );
}

