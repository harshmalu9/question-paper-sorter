import { FiCheck, FiCircle } from "react-icons/fi";
import { cn } from "@/lib/utils";

interface Step {
  label: string;
  status: "completed" | "active" | "pending";
}

interface ProgressTimelineProps {
  steps: Step[];
}

export default function ProgressTimeline({ steps }: ProgressTimelineProps) {
  return (
    <div className="space-y-0">
      {steps.map((step, i) => {
        const isLast = i === steps.length - 1;
        return (
          <div key={step.label} className="flex gap-4">
            {/* Icon + line */}
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 transition-colors",
                  step.status === "completed" &&
                    "border-primary bg-primary text-primary-foreground",
                  step.status === "active" &&
                    "border-primary bg-primary/10 text-primary",
                  step.status === "pending" &&
                    "border-border bg-muted text-muted-foreground",
                )}
              >
                {step.status === "completed" ? (
                  <FiCheck className="h-4 w-4" />
                ) : step.status === "active" ? (
                  <div className="h-2.5 w-2.5 rounded-full bg-primary animate-pulse" />
                ) : (
                  <FiCircle className="h-3 w-3" />
                )}
              </div>
              {!isLast && (
                <div
                  className={cn(
                    "w-0.5 flex-1 min-h-8",
                    step.status === "completed"
                      ? "bg-primary"
                      : "bg-border",
                  )}
                />
              )}
            </div>

            {/* Label */}
            <div className="pb-8">
              <p
                className={cn(
                  "text-sm font-medium leading-none",
                  step.status === "completed" && "text-foreground",
                  step.status === "active" && "text-primary",
                  step.status === "pending" && "text-muted-foreground",
                )}
              >
                {step.label}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
