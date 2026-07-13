# Job data models.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    job_id: str
    status: JobStatus = JobStatus.QUEUED
    progress: int = 0
    message: str = ""
    input_filename: str = ""
    output_directory: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
    result_files: list[str] = field(
        default_factory=list,
    )
    metadata_file: str = ""

    def to_dict(self) -> dict:
        """Serialize job to a JSON-friendly dict."""
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "progress": self.progress,
            "message": self.message,
            "input_filename": self.input_filename,
            "output_directory": self.output_directory,
            "created_at": self.created_at.isoformat(),
            "finished_at": (
                self.finished_at.isoformat()
                if self.finished_at
                else None
            ),
            "error": self.error,
            "result_files": self.result_files,
            "metadata_file": self.metadata_file,
        }
