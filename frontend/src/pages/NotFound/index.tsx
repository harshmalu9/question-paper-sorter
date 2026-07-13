import { Link } from "react-router-dom";
import Section from "@/components/common/Section";
import Button from "@/components/common/Button";

export default function NotFound() {
  return (
    <Section className="pt-16 text-center">
      <p className="mb-4 text-6xl font-bold text-surface-200">404</p>
      <h1 className="mb-2 text-2xl font-semibold text-surface-800">
        Page not found
      </h1>
      <p className="mb-8 text-surface-500">
        The page you are looking for does not exist.
      </p>
      <Link to="/">
        <Button>Back to Home</Button>
      </Link>
    </Section>
  );
}
