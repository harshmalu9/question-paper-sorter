import { FiDownload, FiFileText } from "react-icons/fi";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface PaperCardProps {
  title: string;
  pages: number;
  confidence: number;
}

export default function PaperCard({
  title,
  pages,
  confidence,
}: PaperCardProps) {
  const confidencePercent = Math.round(confidence * 100);

  return (
    <Card className="group transition-shadow hover:shadow-md">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <FiFileText className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-semibold text-foreground">{title}</h3>
              <p className="text-sm text-muted-foreground">
                {pages} {pages === 1 ? "page" : "pages"}
              </p>
            </div>
          </div>
          <Badge variant={confidencePercent >= 80 ? "success" : "warning"}>
            {confidencePercent}% confidence
          </Badge>
        </div>

        <div className="mt-4 flex justify-end">
          <Button variant="outline" size="sm">
            <FiDownload className="h-3.5 w-3.5" />
            Download PDF
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
