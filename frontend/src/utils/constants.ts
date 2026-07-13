export const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export const ALLOWED_FILE_TYPES = [".pdf", ".zip"] as const;

export const MAX_FILE_SIZE_MB = 100;

export const ROUTES = {
  HOME: "/",
  PROCESSING: "/processing/:jobId",
  RESULTS: "/results/:jobId",
} as const;
