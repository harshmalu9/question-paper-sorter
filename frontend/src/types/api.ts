export type JobStatus = "queued" | "processing" | "completed" | "failed";

export interface Job {
  job_id: string;
  status: JobStatus;
  progress: number;
  message: string;
  input_filename: string;
  output_directory: string;
  created_at: string;
  finished_at: string | null;
  error: string | null;
  result_files: string[];
  metadata_file: string;
}

export interface JobCreateResponse {
  job_id: string;
  status: JobStatus;
}

export interface JobResultsResponse {
  job_id: string;
  status: JobStatus;
  files: string[];
  metadata: string;
}
