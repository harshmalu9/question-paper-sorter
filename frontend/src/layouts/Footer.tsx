import { FiGithub, FiLayers } from "react-icons/fi";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-4 px-4 py-8 sm:flex-row sm:justify-between sm:px-6 sm:py-10 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary/10 text-primary">
            <FiLayers className="h-3 w-3" />
          </div>
          <span className="text-sm font-medium text-foreground">
            Question Paper Sorter
          </span>
        </div>

        {/* <p className="text-xs text-muted-foreground">
          &copy; {new Date().getFullYear()} Question Paper Sorter
        </p> */}

        <a
          href="https://github.com/harshmalu9/question-paper-sorter"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-xs text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm"
        >
          <FiGithub className="h-3.5 w-3.5" />
          GitHub
        </a>
      </div>
    </footer>
  );
}
