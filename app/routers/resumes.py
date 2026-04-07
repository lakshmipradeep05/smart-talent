import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import BatchUploadResponse, UploadResult, ResumeProfile
from app.services import store
from app.services.resume_parser import parse_resume

# APIRouter is like a mini-app — we group resume-related routes here
# prefix="/resumes" means every route in this file starts with /resumes
router = APIRouter(prefix="/resumes", tags=["resumes"])

# Which file types we accept
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".jpg", ".jpeg", ".png"}


@router.post("/upload", response_model=BatchUploadResponse)
async def upload_resumes(
    files: list[UploadFile] = File(...),   # accepts multiple files at once
    job_role: str = Form(default="General"),  # which role these resumes are for
):
    batch_id = str(uuid.uuid4())[:8]   # short unique ID for this upload batch
    results: list[UploadResult] = []
    successful = 0
    failed = 0

    for file in files:
        # Check if file extension is supported
        ext = Path(file.filename or "").suffix.lower()

        if ext not in SUPPORTED_EXTENSIONS:
            results.append(UploadResult(
                filename=file.filename or "unknown",
                status="unsupported",
                error=f"'{ext}' is not supported. Use PDF, DOCX, JPG or PNG.",
            ))
            failed += 1
            continue   # skip to next file

        try:
            content = await file.read()   # read raw bytes from uploaded file

            if len(content) == 0:
                raise ValueError("File is empty")

            # For now we create a basic profile — parser comes in next step
            profile = parse_resume(
                file_bytes=content,
                filename=file.filename or "unknown",
                job_role=job_role,
                upload_batch=batch_id,
            )
            store.save_resume(profile)
            successful += 1

            results.append(UploadResult(
                filename=file.filename,
                status="success",
                resume_id=profile.id,
            ))

        except Exception as exc:
            results.append(UploadResult(
                filename=file.filename or "unknown",
                status="failed",
                error=str(exc),
            ))
            failed += 1

    return BatchUploadResponse(
        batch_id=batch_id,
        job_role=job_role,
        total_files=len(files),
        successful=successful,
        failed=failed,
        results=results,
    )


@router.get("/", response_model=list[ResumeProfile])
def list_resumes(job_role: str | None = None):
    """Get all uploaded resumes, optionally filtered by job role."""
    if job_role:
        return store.get_resumes_by_role(job_role)
    return store.get_all_resumes()


@router.get("/{resume_id}", response_model=ResumeProfile)
def get_resume(resume_id: str):
    """Get a single resume by its ID."""
    resume = store.get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.delete("/{resume_id}")
def delete_resume(resume_id: str):
    if not store.delete_resume(resume_id):
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Deleted successfully"}