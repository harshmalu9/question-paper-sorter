import Section from "@/components/common/Section";
import Card from "@/components/common/Card";

export default function Home() {
  return (
    <>
      <Section className="pt-16 text-center">
        <h1 className="mb-4 text-4xl font-bold text-surface-800 sm:text-5xl">
          Question Paper Sorter
        </h1>
        <p className="mx-auto mb-8 max-w-2xl text-lg text-surface-500">
          Automatically sort scanned question papers into individual grouped
          PDFs using OCR and document boundary detection.
        </p>
      </Section>

      <Section title="How it works">
        <div className="grid gap-6 sm:grid-cols-3">
          {[
            {
              step: "1",
              title: "Upload",
              desc: "Upload a PDF or ZIP containing scanned question paper pages.",
            },
            {
              step: "2",
              title: "Process",
              desc: "The engine runs OCR, detects boundaries, and groups pages into papers.",
            },
            {
              step: "3",
              title: "Download",
              desc: "Download individually grouped PDFs with metadata.",
            },
          ].map((item) => (
            <Card key={item.step}>
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-600 font-semibold">
                {item.step}
              </div>
              <h3 className="mb-2 text-lg font-semibold text-surface-800">
                {item.title}
              </h3>
              <p className="text-sm text-surface-500">{item.desc}</p>
            </Card>
          ))}
        </div>
      </Section>
    </>
  );
}
