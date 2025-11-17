"""
Audio upload and processing API routes.
"""
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models import User, Job, JobStatus
from app.schemas.job import JobResponse
from app.api.deps import get_current_user
from app.services.storage import storage_service
from app.tasks.process_audio import process_audio_task
from app.core.config import settings


router = APIRouter(prefix="/audio", tags=["Audio Processing"])


@router.post("/process", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def process_audio(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload an audio file and create a processing job.

    This endpoint:
    1. Validates the file type and size
    2. Checks user's quota
    3. Uploads file to storage (S3/MinIO)
    4. Creates a job in the database
    5. Dispatches Celery task for background processing
    6. Returns job ID for status tracking

    Args:
        file: Audio file upload (MP3, WAV, M4A, OGG, FLAC)
        title: Optional title for the content
        current_user: Authenticated user
        db: Database session

    Returns:
        Job information with job_id for tracking

    Raises:
        HTTPException: If validation fails or quota exceeded
    """
    # Step 1: Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower().replace(".", "")

    if file_extension not in settings.ALLOWED_EXTENSIONS_LIST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS_LIST)}",
        )

    # Step 2: Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > current_user.max_file_size_bytes:
        max_mb = current_user.max_file_size_bytes / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {max_mb:.0f}MB for {current_user.tier} tier",
        )

    # Step 3: Check user quota
    if current_user.uploads_remaining <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Monthly upload limit reached. Upgrade to Pro for unlimited uploads.",
        )

    # Step 4: Upload file to storage
    try:
        file_url = storage_service.upload_file(
            file.file,
            file.filename,
            content_type=file.content_type,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}",
        )

    # Step 5: Create job in database
    job = Job(
        user_id=current_user.id,
        file_url=file_url,
        file_name=file.filename,
        file_size_bytes=file_size,
        title=title,
        status=JobStatus.PENDING,
        progress=0,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Step 6: Increment user's monthly upload counter
    current_user.monthly_uploads_used += 1
    db.commit()

    # Step 7: Dispatch Celery task for background processing
    process_audio_task.delay(str(job.id))

    # Step 8: Return job info
    return JobResponse.from_job(job)
