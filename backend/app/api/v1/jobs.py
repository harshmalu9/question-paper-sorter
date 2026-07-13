# Job routes — create, poll, and list processing jobs.

from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    UploadFile,
)

from backend.app.core.config import settings
from backend.app.jobs.manager import job_manager
from backend.app.services.pipeline import run_pipeline

router = APIRouter()

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".zip"}


# -----------------------------------------------------------
# Background worker
# -----------------------------------------------------------

def _process_job(job_id: str, input_path: str, output_dir: str):
    """Run the product pipeline inside a background thread.

    Progress milestones are written to the job via
    ``job_manager.update_progress`` so the frontend can poll.
    """

    try:
        job_manager.update_progress(
            job_id, 5, "Upload complete"
        )

        job_manager.update_progress(
            job_id, 15, "Preparing files"
        )

        job_manager.update_progress(
            job_id, 35, "OCR running"
        )

        job_manager.update_progress(
            job_id, 65, "Grouping pages"
        )

        pdf_files, meta_file = run_pipeline(
            input_path=input_path,
            output_dir=output_dir,
        )

        job_manager.update_progress(
            job_id, 90, "Exporting PDFs"
        )

        # Store result filenames so the results endpoint
        # can serve them without scanning the output dir.
        job_manager.complete_job(
            job_id,
            result_files=pdf_files,
            metadata_file=meta_file,
        )

    except Exception as exc:
        job_manager.fail_job(job_id, str(exc))


# -----------------------------------------------------------
# Routes
# -----------------------------------------------------------

@router.post("/jobs")
async def create_job(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Accept a PDF or ZIP, create a job, and return immediately."""

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed.",
        )

    # Persist the uploaded file.
    content = await file.read()
    input_path = UPLOAD_DIR / file.filename
    input_path.write_bytes(content)

    # Prepare a unique output directory for this job.
    output_dir = str(UPLOAD_DIR / "results" / Path(file.filename).stem)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Register and enqueue the job.
    job = job_manager.create_job(
        input_filename=file.filename,
        output_directory=output_dir,
    )

    background_tasks.add_task(
        _process_job,
        job.job_id,
        str(input_path),
        output_dir,
    )

    return {"job_id": job.job_id, "status": job.status.value}


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Return the current status of a single job."""
    job = job_manager.get_job(job_id)
    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )
    return job.to_dict()


@router.get("/jobs")
async def list_jobs():
    """Return every job, newest first."""
    return [j.to_dict() for j in job_manager.list_jobs()]
