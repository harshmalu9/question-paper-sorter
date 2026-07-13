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
    <Card className="group transition-all duration-200 hover:shadow-md hover:-translate-y-0.5">
      <CardContent className="p-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 transition-colors duration-200 group-hover:bg-primary/15">
              <FiFileText className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-semibold text-foreground">{title}</h3>
              <p className="text-sm text-muted-foreground">
                {pages} {pages === 1 ? "page" : "pages"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 pl-13 sm:pl-0">
            <Badge variant={confidencePercent >= 80 ? "success" : "warning"}>
              {confidencePercent}%
            </Badge>
            <Button variant="outline" size="sm">
              <FiDownload className="h-3.5 w-3.5" />
              Download
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
