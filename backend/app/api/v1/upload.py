# Upload route — accepts .pdf / .zip files,
# saves them to the configured upload directory,
# returns filename + size.

from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.core.config import settings

router = APIRouter()

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".zip"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed.",
        )

    # Read and save the file
    content = await file.read()
    dest = UPLOAD_DIR / file.filename
    dest.write_bytes(content)

    return {
        "filename": file.filename,
        "size_bytes": len(content),
    }
