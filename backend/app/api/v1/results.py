# Result retrieval endpoint — returns generated file names
# for a completed job.  The actual files are served by the
# download endpoint in download.py.

from fastapi import APIRouter, HTTPException

from backend.app.jobs.manager import job_manager
from backend.app.jobs.models import JobStatus

router = APIRouter()


@router.get("/jobs/{job_id}/results")
async def get_results(job_id: str):
    """Return the list of generated files for a completed job.

    - 200: job completed, files and metadata filename included
    - 400: job failed
    - 404: job not found
    - 409: job still running or queued
    """
    job = job_manager.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.status == JobStatus.FAILED:
        raise HTTPException(
            status_code=400,
            detail="Job failed",
        )

    if job.status in (
        JobStatus.QUEUED,
        JobStatus.PROCESSING,
    ):
        raise HTTPException(
            status_code=409,
            detail="Job is still running",
        )

    return {
        "job_id": job.job_id,
        "status": job.status.value,
        "files": job.result_files,
        "metadata": job.metadata_file,
    }
