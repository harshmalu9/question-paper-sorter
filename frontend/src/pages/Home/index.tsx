import { FiCpu, FiLayers, FiFileText } from "react-icons/fi";
import UploadCard from "@/components/upload/UploadCard";
import FeatureCard from "@/components/common/FeatureCard";

const features = [
  {
    icon: <FiCpu className="h-6 w-6" />,
    title: "OCR Powered",
    description:
      "Advanced text recognition extracts content from scanned pages with automatic rotation correction and caching.",
  },
  {
    icon: <FiLayers className="h-6 w-6" />,
    title: "Strong Page Grouping",
    description:
      "TF-IDF similarity analysis and keyword boundary detection identify where one paper ends and another begins.",
  },
  {
    icon: <FiFileText className="h-6 w-6" />,
    title: "Multiple PDF Export",
    description:
      "Each detected paper is exported as a separate high-quality PDF with full metadata and confidence scores.",
  },
];

export default function Home() {
  return (
    <>
      {/* Hero */}
      <section className="px-4 pt-20 pb-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Separate Mixed Question Papers{" "}
            <span className="text-primary">Automatically</span>
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground">
            Upload a PDF, ZIP, or Images and receive perfectly grouped PDFs in
            minutes.
          </p>
        </div>
      </section>

      {/* Upload */}
      <section className="px-4 pb-20 sm:px-6 lg:px-8">
        <UploadCard />
      </section>

      {/* Features */}
      <section className="border-t border-border bg-muted/30 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-12 text-center">
            <h2 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
              Built for accuracy
            </h2>
            <p className="mt-3 text-muted-foreground">
              Every layer is designed to produce clean, correctly grouped output.
            </p>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((f) => (
              <FeatureCard key={f.title} {...f} />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
