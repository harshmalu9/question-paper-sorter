import { Link } from "react-router-dom";
import { FiGithub, FiLayers } from "react-icons/fi";

const navLinks = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
];

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <FiLayers className="h-4 w-4" />
          </div>
          <span className="text-base font-semibold text-foreground">
            Question Paper Sorter
          </span>
        </Link>

        <nav className="flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              to={link.href}
              className="rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              {link.label}
            </Link>
          ))}
          <a
            href="https://github.com/harshmalu9/question-paper-sorter"
            target="_blank"
            rel="noopener noreferrer"
            className="ml-2 flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
          >
            <FiGithub className="h-4 w-4" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </nav>
      </div>
    </header>
  );
}
