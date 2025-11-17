"""
Job status and results API routes.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models import User, Job
from app.schemas.job import JobResponse, JobListResponse
from app.api.deps import get_current_user


router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get job status and results by job ID.

    Args:
        job_id: UUID of the job
        current_user: Authenticated user
        db: Database session

    Returns:
        Job information including status, progress, and results (if completed)

    Raises:
        HTTPException: If job not found or doesn't belong to user
    """
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Ensure job belongs to current user
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this job",
        )

    return JobResponse.from_job(job)


@router.get("", response_model=JobListResponse)
async def list_jobs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all jobs for the current user with pagination.

    Args:
        limit: Number of jobs to return (1-100, default 10)
        offset: Number of jobs to skip (default 0)
        current_user: Authenticated user
        db: Database session

    Returns:
        Paginated list of jobs
    """
    # Get total count
    total = db.query(Job).filter(Job.user_id == current_user.id).count()

    # Get jobs with pagination, ordered by creation date (newest first)
    jobs = (
        db.query(Job)
        .filter(Job.user_id == current_user.id)
        .order_by(Job.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return JobListResponse(
        jobs=[JobResponse.from_job(job) for job in jobs],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a job and its associated data.

    Args:
        job_id: UUID of the job to delete
        current_user: Authenticated user
        db: Database session

    Raises:
        HTTPException: If job not found or doesn't belong to user
    """
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Ensure job belongs to current user
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job",
        )

    # Optional: Delete file from storage as well
    # try:
    #     storage_service.delete_file(job.file_url)
    # except:
    #     pass

    db.delete(job)
    db.commit()

    return None
