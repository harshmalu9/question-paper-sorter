import { FiGithub } from "react-icons/fi";

export default function Footer() {
  return (
    <footer className="border-t border-surface-200 bg-surface-50">
      <div className="mx-auto flex max-w-5xl flex-col items-center gap-3 px-4 py-8 sm:flex-row sm:justify-between sm:px-6 lg:px-8">
        <p className="text-sm text-surface-500">
          &copy; {new Date().getFullYear()} Question Paper Sorter
        </p>
        <a
          href="https://github.com/harshmalu9/question-paper-sorter"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-sm text-surface-500 transition-colors hover:text-surface-800"
        >
          <FiGithub size={16} />
          GitHub
        </a>
      </div>
    </footer>
  );
}
