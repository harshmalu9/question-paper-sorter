import { FiGithub, FiLayers } from "react-icons/fi";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-4 px-4 py-10 sm:flex-row sm:justify-between sm:px-6 lg:px-8">
        <div className="flex items-center gap-2.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary/10 text-primary">
            <FiLayers className="h-3.5 w-3.5" />
          </div>
          <span className="text-sm font-medium text-foreground">
            Question Paper Sorter
          </span>
        </div>

        <p className="text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} Question Paper Sorter
        </p>

        <a
          href="https://github.com/harshmalu9/question-paper-sorter"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
        >
          <FiGithub className="h-4 w-4" />
          GitHub
        </a>
      </div>
    </footer>
  );
}
