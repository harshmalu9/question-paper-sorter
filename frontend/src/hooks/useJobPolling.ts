import { useState, useEffect, useRef, useCallback } from "react";
import api from "@/services/api";
import type { Job } from "@/types/api";

const POLL_INTERVAL_MS = 1000;

interface UseJobPollingReturn {
  job: Job | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useJobPolling(jobId: string): UseJobPollingReturn {
  const [job, setJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const mountedRef = useRef(true);

  const stopPolling = useCallback(() => {
    if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const fetchJob = useCallback(async () => {
    try {
      const { data } = await api.get<Job>(`/jobs/${jobId}`);
      if (!mountedRef.current) return;

      setJob(data);
      setError(null);
      setIsLoading(false);

      if (data.status === "completed" || data.status === "failed") {
        stopPolling();
      }
    } catch (err: unknown) {
      if (!mountedRef.current) return;

      let message = "Failed to fetch job status.";

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
          message = "Network error. Could not reach the server.";
        }
      } else if (err instanceof Error) {
        message = err.message;
      }

      setError(message);
      setIsLoading(false);
      stopPolling();
    }
  }, [jobId, stopPolling]);

  useEffect(() => {
    mountedRef.current = true;

    // Initial fetch.
    fetchJob();

    // Start polling.
    intervalRef.current = setInterval(fetchJob, POLL_INTERVAL_MS);

    return () => {
      mountedRef.current = false;
      stopPolling();
    };
  }, [fetchJob, stopPolling]);

  return { job, isLoading, error, refetch: fetchJob };
}
