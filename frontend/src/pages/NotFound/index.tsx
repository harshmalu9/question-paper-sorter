import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <p className="text-8xl font-bold tracking-tighter text-muted/60">
        404
      </p>
      <h1 className="mt-4 text-2xl font-bold tracking-tight text-foreground">
        Page not found
      </h1>
      <p className="mt-2 max-w-sm text-muted-foreground">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link to="/" className="mt-8">
        <Button size="lg">Return Home</Button>
      </Link>
    </div>
  );
}
