import { useParams } from "react-router-dom";
import Section from "@/components/common/Section";
import Card from "@/components/common/Card";

export default function Results() {
  const { jobId } = useParams<{ jobId: string }>();

  return (
    <Section className="pt-16">
      <h1 className="mb-4 text-3xl font-bold text-surface-800">
        Results
      </h1>
      <p className="mb-8 text-surface-500">
        Job <span className="font-mono text-primary-600">{jobId}</span> results
        will appear here.
      </p>
      <Card>
        <p className="text-sm text-surface-400">
          No results to display yet. This page will show generated PDFs and
          metadata once the backend integration is complete.
        </p>
      </Card>
    </Section>
  );
}
