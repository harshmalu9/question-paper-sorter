import JSZip from "jszip";
import api from "@/services/api";
import type { JobCreateResponse } from "@/types/api";

const ACCEPTED_EXTENSIONS = new Set([".pdf", ".zip", ".jpg", ".jpeg", ".png"]);
const IMAGE_EXTENSIONS = new Set([".jpg", ".jpeg", ".png"]);

export function isImageFile(file: File): boolean {
  const ext = "." + file.name.split(".").pop()?.toLowerCase();
  return IMAGE_EXTENSIONS.has(ext);
}

export function isAcceptedFile(file: File): boolean {
  const ext = "." + file.name.split(".").pop()?.toLowerCase();
  return ACCEPTED_EXTENSIONS.has(ext);
}

function getExtension(name: string): string {
  return "." + name.split(".").pop()?.toLowerCase();
}

/**
 * Given a list of user-selected files, returns a single File
 * ready for upload:
 * - If all files are images, ZIP them in the browser.
 * - If a single PDF or ZIP, return as-is.
 * - Otherwise throw.
 */
export async function prepareUpload(
  files: File[],
): Promise<File> {
  if (files.length === 0) {
    throw new Error("No files selected");
  }

  // Single PDF or ZIP — upload directly.
  if (files.length === 1) {
    const ext = getExtension(files[0].name);
    if (ext === ".pdf" || ext === ".zip") {
      return files[0];
    }
  }

  // Multiple files or single image — all must be images.
  const nonImage = files.find((f) => !isImageFile(f));
  if (nonImage) {
    throw new Error(
      `Unsupported file type: ${nonImage.name}. Use PDF, ZIP, or images only.`,
    );
  }

  // Create a ZIP from the images in the browser.
  const zip = new JSZip();
  for (const file of files) {
    zip.file(file.name, file);
  }

  const blob = await zip.generateAsync({ type: "blob" });
  return new File([blob], "images.zip", { type: "application/zip" });
}

/**
 * Upload a prepared file to the backend and return the job ID.
 */
export async function uploadFile(
  file: File,
): Promise<JobCreateResponse> {
  const form = new FormData();
  form.append("file", file);

  const { data } = await api.post<JobCreateResponse>("/jobs", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
}
