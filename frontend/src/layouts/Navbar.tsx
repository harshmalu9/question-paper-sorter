import { Link } from "react-router-dom";
import { FiGithub } from "react-icons/fi";

const navLinks = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
];

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-surface-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link
          to="/"
          className="text-lg font-semibold text-surface-800"
        >
          Question Paper Sorter
        </Link>

        <nav className="flex items-center gap-6">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              to={link.href}
              className="text-sm font-medium text-surface-500 transition-colors hover:text-surface-800"
            >
              {link.label}
            </Link>
          ))}
          <a
            href="https://github.com/harshmalu9/question-paper-sorter"
            target="_blank"
            rel="noopener noreferrer"
            className="text-surface-500 transition-colors hover:text-surface-800"
            aria-label="GitHub"
          >
            <FiGithub size={20} />
          </a>
        </nav>
      </div>
    </header>
  );
}
