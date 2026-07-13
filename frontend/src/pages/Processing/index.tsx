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

const stats = [
  { label: "Current File", value: "exam_2024.pdf" },
  { label: "Pages Processed", value: "24 / 69" },
  { label: "OCR Confidence", value: "94%" },
  { label: "Groups Found", value: "3" },
  { label: "Estimated Time", value: "~1 min 42 sec" },
];

export default function Processing() {
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
                <span className="font-semibold text-primary">35%</span>
              </div>
              <Progress value={35} />
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

              {/* Stats */}
              <div className="space-y-4">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Details
                </h3>
                <div className="space-y-3">
                  {stats.map((stat) => (
                    <div
                      key={stat.label}
                      className="flex items-center justify-between rounded-lg bg-muted/50 px-4 py-3"
                    >
                      <span className="text-sm text-muted-foreground">
                        {stat.label}
                      </span>
                      <span className="text-sm font-medium text-foreground">
                        {stat.value}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
