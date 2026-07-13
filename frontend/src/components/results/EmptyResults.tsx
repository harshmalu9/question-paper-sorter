import { FiInbox } from "react-icons/fi";

export default function EmptyResults() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-2xl bg-muted">
        <FiInbox className="h-9 w-9 text-muted-foreground/60" />
      </div>
      <h3 className="mb-2 text-lg font-semibold text-foreground">
        No results yet
      </h3>
      <p className="max-w-xs text-sm leading-relaxed text-muted-foreground">
        Upload a PDF or ZIP to get started. Your grouped papers will appear
        here once processing is complete.
      </p>
    </div>
  );
}
