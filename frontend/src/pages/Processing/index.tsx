import { useParams } from "react-router-dom";
import Section from "@/components/common/Section";

export default function Processing() {
  const { jobId } = useParams<{ jobId: string }>();

  return (
    <Section className="pt-16 text-center">
      <h1 className="mb-4 text-3xl font-bold text-surface-800">
        Processing
      </h1>
      <p className="text-surface-500">
        Job <span className="font-mono text-primary-600">{jobId}</span> is
        being processed.
      </p>
      <div className="mt-8 mx-auto max-w-md">
        <div className="h-2 rounded-full bg-surface-200">
          <div className="h-2 w-1/3 rounded-full bg-primary-500" />
        </div>
        <p className="mt-3 text-sm text-surface-400">Placeholder progress bar</p>
      </div>
    </Section>
  );
}
