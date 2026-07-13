# In-memory job manager singleton.

import uuid
from datetime import datetime, timezone
from typing import Optional

from backend.app.jobs.models import Job, JobStatus


class JobManager:
    """Thread-safe in-memory store for processing jobs."""

    def __init__(self):
        self._jobs: dict[str, Job] = {}

    def create_job(
        self,
        input_filename: str,
        output_directory: str,
    ) -> Job:
        """Create a new job and return it."""
        job = Job(
            job_id=str(uuid.uuid4()),
            input_filename=input_filename,
            output_directory=output_directory,
        )
        self._jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Return a job by ID, or None."""
        return self._jobs.get(job_id)

    def update_progress(
        self,
        job_id: str,
        progress: int,
        message: str,
    ) -> None:
        """Update progress percentage and message."""
        job = self._jobs.get(job_id)
        if job is None:
            return
        job.progress = progress
        job.message = message
        job.status = JobStatus.PROCESSING

    def complete_job(
        self,
        job_id: str,
        result_files: Optional[list[str]] = None,
        metadata_file: str = "",
    ) -> None:
        """Mark a job as completed.

        Stores the list of generated PDF filenames and the
        metadata.json filename so result retrieval endpoints
        can serve them without scanning the output directory.
        """
        job = self._jobs.get(job_id)
        if job is None:
            return
        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.message = "Completed"
        job.finished_at = datetime.now(timezone.utc)
        job.result_files = result_files or []
        job.metadata_file = metadata_file

    def fail_job(
        self, job_id: str, error: str
    ) -> None:
        """Mark a job as failed with an error message."""
        job = self._jobs.get(job_id)
        if job is None:
            return
        job.status = JobStatus.FAILED
        job.error = error
        job.finished_at = datetime.now(timezone.utc)

    def list_jobs(self) -> list[Job]:
        """Return all jobs, newest first."""
        return sorted(
            self._jobs.values(),
            key=lambda j: j.created_at,
            reverse=True,
        )


# Module-level singleton.
job_manager = JobManager()
