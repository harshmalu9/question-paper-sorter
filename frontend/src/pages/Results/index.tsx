import { FiDownload, FiCheckCircle } from "react-icons/fi";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import PaperCard from "@/components/results/PaperCard";
import EmptyResults from "@/components/results/EmptyResults";

const staticPapers = [
  { title: "Paper 1", pages: 4, confidence: 0.96 },
  { title: "Paper 2", pages: 6, confidence: 0.91 },
  { title: "Paper 3", pages: 3, confidence: 0.88 },
  { title: "Paper 4", pages: 5, confidence: 0.82 },
  { title: "Paper 5", pages: 8, confidence: 0.95 },
];

const showResults = true;

export default function Results() {
  if (!showResults) {
    return (
      <div className="px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl">
          <EmptyResults />
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 py-16 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-3xl">
        {/* Header */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2">
              <FiCheckCircle className="h-5 w-5 text-success" />
              <h1 className="text-2xl font-bold tracking-tight text-foreground">
                Processing Complete
              </h1>
            </div>
            <p className="text-sm text-muted-foreground">
              {staticPapers.length} papers detected &middot;{" "}
              {staticPapers.reduce((sum, p) => sum + p.pages, 0)} total pages
            </p>
          </div>
          <Button size="lg">
            <FiDownload className="h-4 w-4" />
            Download All
          </Button>
        </div>

        {/* Summary card */}
        <Card className="mb-8">
          <CardContent className="flex items-center gap-6 p-5">
            <div className="grid flex-1 grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-foreground">5</p>
                <p className="text-xs text-muted-foreground">Papers</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">26</p>
                <p className="text-xs text-muted-foreground">Pages</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">90%</p>
                <p className="text-xs text-muted-foreground">Avg. Confidence</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Paper list */}
        <div className="space-y-3">
          {staticPapers.map((paper) => (
            <PaperCard key={paper.title} {...paper} />
          ))}
        </div>
      </div>
    </div>
  );
}
