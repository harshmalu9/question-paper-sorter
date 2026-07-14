import { useEffect, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { FiAlertCircle, FiHome, FiRefreshCw } from "react-icons/fi";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import ProgressTimeline from "@/components/progress/ProgressTimeline";
import { useJobPolling } from "@/hooks/useJobPolling";
import type { Job } from "@/types/api";

const TIMELINE_STEPS = [
  "Upload complete",
  "Preparing files",
  "OCR running",
  "Grouping pages",
  "Exporting PDFs",
  "Completed",
] as const;

function getTimelineStatuses(
  job: Job,
): ("completed" | "active" | "pending")[] {
  if (job.status === "completed") {
    return TIMELINE_STEPS.map(() => "completed" as const);
  }

  if (job.status === "failed") {
    const activeIdx = TIMELINE_STEPS.indexOf(
      job.message as (typeof TIMELINE_STEPS)[number],
    );
    return TIMELINE_STEPS.map((_, i) =>
      i < activeIdx ? "completed" : i === activeIdx ? "active" : "pending",
    );
  }

  // For "queued" or "processing", determine which step is active.
  const activeIdx = TIMELINE_STEPS.indexOf(
    job.message as (typeof TIMELINE_STEPS)[number],
  );

  if (activeIdx === -1) {
    // Unknown message — treat everything pending.
    return TIMELINE_STEPS.map(() => "pending" as const);
  }

  return TIMELINE_STEPS.map((_, i) =>
    i < activeIdx ? "completed" : i === activeIdx ? "active" : "pending",
  );
}

function getStageLabel(job: Job): string {
  if (job.status === "completed") return "Completed";
  if (job.status === "failed") return "Failed";
  return job.message || "Queued";
}

export default function Processing() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const { job, isLoading, error, refetch } = useJobPolling(jobId!);

  const statuses = useMemo(
    () => (job ? getTimelineStatuses(job) : TIMELINE_STEPS.map(() => "pending" as const)),
    [job],
  );

  const steps = useMemo(
    () =>
      TIMELINE_STEPS.map((label, i) => ({
        label,
        status: statuses[i],
      })),
    [statuses],
  );

  // Auto-navigate to results on completion.
  useEffect(() => {
    if (job?.status === "completed") {
      navigate(`/results/${job.job_id}`, { replace: true });
    }
  }, [job?.status, job?.job_id, navigate]);

  // ---------- Error state (job not found / network) ----------
  if (error && !job) {
    return (
      <div className="px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-2xl animate-fade-in">
          <Card className="border-destructive/30">
            <CardContent className="flex flex-col items-center gap-6 p-8 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
                <FiAlertCircle className="h-8 w-8 text-destructive" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-foreground">
                  Something went wrong
                </h2>
                <p className="mt-2 text-sm text-muted-foreground">{error}</p>
              </div>
              <div className="flex gap-3">
                <Button variant="outline" onClick={() => navigate("/")}>
                  <FiHome className="h-4 w-4" />
                  Back to Home
                </Button>
                <Button onClick={refetch}>
                  <FiRefreshCw className="h-4 w-4" />
                  Try Again
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // ---------- Failed job state ----------
  if (job?.status === "failed") {
    return (
      <div className="px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-2xl animate-fade-in">
          <Card className="border-destructive/30">
            <CardContent className="flex flex-col items-center gap-6 p-8 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-destructive/10">
                <FiAlertCircle className="h-8 w-8 text-destructive" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-foreground">
                  Processing failed
                </h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  {job.error || "An unexpected error occurred."}
                </p>
              </div>
              <div className="flex gap-3">
                <Button variant="outline" onClick={() => navigate("/")}>
                  <FiHome className="h-4 w-4" />
                  Back to Home
                </Button>
                <Button onClick={() => navigate("/", { replace: true })}>
                  <FiRefreshCw className="h-4 w-4" />
                  Retry
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // ---------- Loading state (initial fetch) ----------
  if (isLoading || !job) {
    return (
      <div className="px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        <div className="mx-auto max-w-2xl animate-fade-in">
          <div className="mb-10 text-center">
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <div className="h-4 w-4 rounded-full bg-primary animate-pulse" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
              Loading job status...
            </h1>
          </div>
        </div>
      </div>
    );
  }

  // ---------- Active processing ----------
  return (
    <div className="px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-2xl animate-fade-in">
        {/* Header */}
        <div className="mb-10 text-center">
          <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
            <div className="h-4 w-4 rounded-full bg-primary animate-pulse" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            Processing your files
          </h1>
          <p className="mt-3 text-sm text-muted-foreground">
            This usually takes 1–3 minutes depending on file size.
          </p>
        </div>

        {/* Main card */}
        <Card className="overflow-hidden">
          <CardContent className="p-6 sm:p-8">
            {/* Progress bar */}
            <div className="mb-8">
              <div className="mb-2.5 flex items-center justify-between text-sm">
                <span className="font-medium text-foreground">
                  Overall Progress
                </span>
                <span className="font-semibold text-primary">
                  {job.progress}%
                </span>
              </div>
              <Progress value={job.progress} />
            </div>

            {/* Desktop: horizontal timeline */}
            <div className="mb-8 hidden sm:block">
              <ProgressTimeline steps={steps} orientation="horizontal" />
            </div>

            {/* Content grid */}
            <div className="grid gap-8 sm:grid-cols-2">
              {/* Mobile: vertical timeline */}
              <div className="sm:hidden">
                <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Pipeline
                </h3>
                <ProgressTimeline steps={steps} orientation="vertical" />
              </div>

              {/* Details */}
              <div className="space-y-4">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Details
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between rounded-lg bg-muted/50 px-4 py-3">
                    <span className="text-sm text-muted-foreground">
                      Current File
                    </span>
                    <span className="text-sm font-medium text-foreground truncate max-w-[180px]">
                      {job.input_filename}
                    </span>
                  </div>
                  <div className="flex items-center justify-between rounded-lg bg-muted/50 px-4 py-3">
                    <span className="text-sm text-muted-foreground">
                      Current Stage
                    </span>
                    <span className="text-sm font-medium text-foreground">
                      {getStageLabel(job)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between rounded-lg bg-muted/50 px-4 py-3">
                    <span className="text-sm text-muted-foreground">
                      Status
                    </span>
                    <span className="text-sm font-medium text-foreground capitalize">
                      {job.status}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
