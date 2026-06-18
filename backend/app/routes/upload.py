# Upload route — accepts .pdf / .zip files,
# saves them to backend/uploads/, returns filename + size.

from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

# Resolve upload directory relative to this file:
# backend/app/routes/upload.py -> backend/uploads/
UPLOAD_DIR = (
    Path(__file__).resolve().parent.parent.parent / "uploads"
)
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
