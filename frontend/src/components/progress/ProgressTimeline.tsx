import { FiCheck } from "react-icons/fi";
import { cn } from "@/lib/utils";

interface Step {
  label: string;
  status: "completed" | "active" | "pending";
}

interface ProgressTimelineProps {
  steps: Step[];
  orientation?: "vertical" | "horizontal";
}

export default function ProgressTimeline({
  steps,
  orientation = "vertical",
}: ProgressTimelineProps) {
  if (orientation === "horizontal") {
    return (
      <div className="flex items-center">
        {steps.map((step, i) => {
          const isLast = i === steps.length - 1;
          return (
            <div key={step.label} className="flex items-center">
              {/* Dot */}
              <div className="flex flex-col items-center">
                <div
                  className={cn(
                    "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-xs font-semibold transition-all duration-300",
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
                    <span>{i + 1}</span>
                  )}
                </div>
                <span
                  className={cn(
                    "mt-2 whitespace-nowrap text-xs font-medium",
                    step.status === "completed" && "text-foreground",
                    step.status === "active" && "text-primary",
                    step.status === "pending" && "text-muted-foreground",
                  )}
                >
                  {step.label}
                </span>
              </div>

              {/* Connector line */}
              {!isLast && (
                <div
                  className={cn(
                    "mx-1.5 h-0.5 w-8 sm:w-12 transition-colors duration-300",
                    step.status === "completed" ? "bg-primary" : "bg-border",
                  )}
                />
              )}
            </div>
          );
        })}
      </div>
    );
  }

  // Vertical layout
  return (
    <div className="space-y-0">
      {steps.map((step, i) => {
        const isLast = i === steps.length - 1;
        return (
          <div key={step.label} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 transition-all duration-300",
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
                  <span className="text-xs">{i + 1}</span>
                )}
              </div>
              {!isLast && (
                <div
                  className={cn(
                    "w-0.5 flex-1 min-h-6 transition-colors duration-300",
                    step.status === "completed" ? "bg-primary" : "bg-border",
                  )}
                />
              )}
            </div>

            <div className="pb-6 pt-1">
              <p
                className={cn(
                  "text-sm font-medium",
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
