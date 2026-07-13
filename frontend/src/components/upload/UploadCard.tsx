import { FiUploadCloud, FiFile, FiArchive, FiImage } from "react-icons/fi";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function UploadCard() {
  return (
    <Card className="mx-auto w-full max-w-2xl overflow-hidden">
      {/* Drop zone */}
      <div className="border-b border-border p-8 sm:p-12">
        <div className="flex flex-col items-center gap-4 rounded-2xl border-2 border-dashed border-border bg-muted/30 px-6 py-12 transition-colors hover:border-primary/40 hover:bg-primary/5">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
            <FiUploadCloud className="h-7 w-7 text-primary" />
          </div>
          <div className="text-center">
            <p className="text-base font-medium text-foreground">
              Drop your files here
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              or{" "}
              <button className="font-medium text-primary hover:underline">
                Choose Files
              </button>
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span className="rounded-md bg-muted px-2 py-0.5 font-medium">PDF</span>
            <span className="rounded-md bg-muted px-2 py-0.5 font-medium">ZIP</span>
            <span className="rounded-md bg-muted px-2 py-0.5 font-medium">Images</span>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex flex-col gap-3 p-6 sm:flex-row">
        <Button className="flex-1" size="lg">
          <FiFile className="h-4 w-4" />
          Upload PDF
        </Button>
        <Button className="flex-1" variant="secondary" size="lg">
          <FiArchive className="h-4 w-4" />
          Upload ZIP
        </Button>
        <Button className="flex-1" variant="secondary" size="lg">
          <FiImage className="h-4 w-4" />
          Upload Images
        </Button>
      </div>
    </Card>
  );
}
