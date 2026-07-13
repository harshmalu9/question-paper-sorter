import type { ReactNode } from "react";

interface SectionProps {
  children: ReactNode;
  className?: string;
  title?: string;
}

export default function Section({
  children,
  className = "",
  title,
}: SectionProps) {
  return (
    <section className={`py-12 ${className}`}>
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        {title && (
          <h2 className="mb-6 text-2xl font-semibold text-surface-800">
            {title}
          </h2>
        )}
        {children}
      </div>
    </section>
  );
}
