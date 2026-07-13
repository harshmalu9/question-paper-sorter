import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import ProgressTimeline from "@/components/progress/ProgressTimeline";

const steps = [
  { label: "Uploading", status: "completed" as const },
  { label: "OCR Processing", status: "active" as const },
  { label: "Grouping Pages", status: "pending" as const },
  { label: "Exporting PDFs", status: "pending" as const },
  { label: "Completed", status: "pending" as const },
];

export default function Processing() {
  return (
    <div className="px-4 py-16 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
            <div className="h-4 w-4 rounded-full bg-primary animate-pulse" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">
            Processing your files
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            This usually takes 1–3 minutes depending on file size.
          </p>
        </div>

        {/* Main card */}
        <Card>
          <CardContent className="p-6 sm:p-8">
            {/* Progress bar */}
            <div className="mb-8">
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium text-foreground">
                  Overall Progress
                </span>
                <span className="text-muted-foreground">35%</span>
              </div>
              <Progress value={35} />
            </div>

            {/* Two-column layout */}
            <div className="grid gap-8 sm:grid-cols-2">
              {/* Timeline */}
              <div>
                <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Pipeline
                </h3>
                <ProgressTimeline steps={steps} />
              </div>

              {/* Stats */}
              <div className="space-y-5">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Details
                </h3>

                <div>
                  <p className="text-xs text-muted-foreground">Current file</p>
                  <p className="mt-0.5 text-sm font-medium text-foreground">
                    exam_2024.pdf
                  </p>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground">Current page</p>
                  <p className="mt-0.5 text-sm font-medium text-foreground">
                    24 / 69
                  </p>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground">
                    Estimated remaining
                  </p>
                  <p className="mt-0.5 text-sm font-medium text-foreground">
                    ~1 min 42 sec
                  </p>
                </div>

                <div>
                  <p className="text-xs text-muted-foreground">
                    Pages processed
                  </p>
                  <p className="mt-0.5 text-sm font-medium text-foreground">
                    24 of 69
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
