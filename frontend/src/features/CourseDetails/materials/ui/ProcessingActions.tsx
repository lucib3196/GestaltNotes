import { FiRefreshCw } from "react-icons/fi";

export function ProcessingActions({
  processed,
  busy,
  canProcess,
  failed,
  requestError,
  taskError,
  onProcess,
  onCheck,
}: {
  processed: boolean;
  busy: boolean;
  canProcess: boolean;
  failed: boolean;
  requestError: string | null;
  taskError: string | null;
  onProcess: () => void;
  onCheck: () => void;
}) {
  const buttonClass =
    "inline-flex min-h-9 items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-xs font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-not-allowed disabled:opacity-50";
  return (
    <>
      {!processed &&
        (requestError ? (
          <button
            type="button"
            onClick={onCheck}
            disabled={busy}
            className={`${buttonClass} text-accent hover:bg-accent/10`}
          >
            <FiRefreshCw aria-hidden="true" /> Check again
          </button>
        ) : (
          <button
            type="button"
            onClick={onProcess}
            disabled={busy || !canProcess}
            className={`${buttonClass} bg-accent/10 text-accent enabled:hover:bg-accent/20`}
          >
            {failed ? "Retry processing" : "Process"}
          </button>
        ))}
      {(requestError || taskError) && (
        <p
          role="alert"
          className="basis-full text-xs leading-5 text-red-600 dark:text-red-400"
        >
          {requestError || taskError}
        </p>
      )}
    </>
  );
}

