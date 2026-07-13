import { useRef, useState, useCallback, type DragEvent } from "react";
import { FiUploadCloud, FiLoader, FiAlertCircle } from "react-icons/fi";
import { Card } from "@/components/ui/card";
import { useUpload } from "@/hooks/useUpload";

const ACCEPT = ".pdf,.zip,.jpg,.jpeg,.png";

export default function UploadCard() {
  const { status, error, upload, reset } = useUpload();
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const isBusy = status === "preparing" || status === "uploading";

  // --- Event handlers ---

  const handleFiles = useCallback(
    (files: FileList | null) => {
      if (!files || files.length === 0) return;
      upload(files);
    },
    [upload],
  );

  const handleDrop = useCallback(
    (e: DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      if (!isBusy) handleFiles(e.dataTransfer.files);
    },
    [isBusy, handleFiles],
  );

  const handleDragOver = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleClick = useCallback(() => {
    if (!isBusy) inputRef.current?.click();
  }, [isBusy]);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      handleFiles(e.target.files);
      // Reset input so re-selecting the same file triggers onChange.
      e.target.value = "";
    },
    [handleFiles],
  );

  // --- Render ---

  return (
    <Card className="mx-auto w-full max-w-2xl overflow-hidden animate-scale-in">
      {/* Hidden file input */}
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPT}
        multiple
        className="hidden"
        onChange={handleChange}
      />

      {/* Drop zone — entire card area is clickable */}
      <div
        role="button"
        tabIndex={isBusy ? -1 : 0}
        aria-label="Upload files"
        onClick={handleClick}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            handleClick();
          }
        }}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`flex flex-col items-center gap-5 border-b border-border px-6 py-14 transition-all duration-200 sm:px-12 sm:py-20 ${
          isBusy
            ? "cursor-wait opacity-60"
            : "cursor-pointer hover:bg-primary/[0.02]"
        } ${isDragging ? "bg-primary/[0.04]" : ""}`}
      >
        {/* Icon */}
        <div
          className={`flex h-16 w-16 items-center justify-center rounded-2xl transition-all duration-200 ${
            isDragging
              ? "bg-primary/20 scale-110"
              : "bg-primary/10"
          }`}
        >
          {status === "uploading" || status === "preparing" ? (
            <FiLoader className="h-8 w-8 text-primary animate-spin" />
          ) : (
            <FiUploadCloud className="h-8 w-8 text-primary" />
          )}
        </div>

        {/* Text */}
        <div className="text-center">
          {status === "preparing" ? (
            <p className="text-lg font-semibold text-foreground">
              Preparing files...
            </p>
          ) : status === "uploading" ? (
            <p className="text-lg font-semibold text-foreground">
              Uploading...
            </p>
          ) : (
            <>
              <p className="text-lg font-semibold text-foreground">
                Drop your files here
              </p>
              <p className="mt-1.5 text-sm text-muted-foreground">
                or{" "}
                <span className="font-medium text-primary hover:underline">
                  choose files
                </span>{" "}
                from your computer
              </p>
            </>
          )}
        </div>

        {/* Supported formats */}
        {!isBusy && (
          <div className="flex items-center gap-2">
            {["PDF", "ZIP", "JPG", "PNG"].map((fmt) => (
              <span
                key={fmt}
                className="rounded-full border border-border bg-background px-3 py-1 text-xs font-medium text-muted-foreground"
              >
                {fmt}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Error message */}
      {status === "error" && error && (
        <div className="flex items-start gap-3 border-t border-destructive/20 bg-destructive/5 px-6 py-4">
          <FiAlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-destructive" />
          <div className="flex-1">
            <p className="text-sm font-medium text-destructive">{error}</p>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation();
              reset();
            }}
            className="text-xs font-medium text-destructive/70 hover:text-destructive transition-colors"
          >
            Dismiss
          </button>
        </div>
      )}
    </Card>
  );
}
