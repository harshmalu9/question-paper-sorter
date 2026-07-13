import { useState, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { prepareUpload, uploadFile, isAcceptedFile } from "@/services/upload";

type UploadStatus = "idle" | "preparing" | "uploading" | "error";

interface UseUploadReturn {
  status: UploadStatus;
  error: string | null;
  upload: (files: FileList | File[]) => Promise<void>;
  reset: () => void;
}

export function useUpload(): UseUploadReturn {
  const navigate = useNavigate();
  const [status, setStatus] = useState<UploadStatus>("idle");
  const [error, setError] = useState<string | null>(null);

  // Guard against double-invocations (e.g. drop + onChange).
  const inFlight = useRef(false);

  const reset = useCallback(() => {
    setStatus("idle");
    setError(null);
  }, []);

  const upload = useCallback(
    async (fileList: FileList | File[]) => {
      if (inFlight.current) return;
      inFlight.current = true;

      const files = Array.from(fileList);

      // Validate every file before doing anything.
      const rejected = files.find((f) => !isAcceptedFile(f));
      if (rejected) {
        const ext = rejected.name.split(".").pop()?.toLowerCase() ?? "unknown";
        setError(
          `Unsupported file type: .${ext}. Please upload PDF, ZIP, JPG, or PNG files.`,
        );
        setStatus("error");
        inFlight.current = false;
        return;
      }

      if (files.length === 0) {
        setError("No files selected.");
        setStatus("error");
        inFlight.current = false;
        return;
      }

      try {
        // Step 1: Prepare (ZIP images if needed).
        setStatus("preparing");
        setError(null);
        const prepared = await prepareUpload(files);

        // Step 2: Upload to backend.
        setStatus("uploading");
        const result = await uploadFile(prepared);

        // Step 3: Navigate to processing page.
        navigate(`/processing/${result.job_id}`);
      } catch (err: unknown) {
        let message = "Upload failed. Please try again.";

        if (err instanceof Error) {
          message = err.message;
        }

        // Axios errors have a response or request property.
        if (
          typeof err === "object" &&
          err !== null &&
          "isAxiosError" in err &&
          (err as { isAxiosError: boolean }).isAxiosError
        ) {
          const axiosErr = err as {
            response?: { data?: { detail?: string } };
            request?: unknown;
          };
          if (axiosErr.response?.data?.detail) {
            message = axiosErr.response.data.detail;
          } else if (axiosErr.request) {
            message =
              "Network error. Could not reach the server. Is the backend running?";
          }
        }

        setError(message);
        setStatus("error");
      } finally {
        inFlight.current = false;
      }
    },
    [navigate],
  );

  return { status, error, upload, reset };
}
