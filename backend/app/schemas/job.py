"""
Pydantic schemas for Job API validation and serialization.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from app.models.job import JobStatus


# =============================================================================
# Job Creation
# =============================================================================

class JobCreate(BaseModel):
    """Schema for creating a new job (used internally)"""
    user_id: UUID
    file_url: str
    file_name: str
    file_size_bytes: int
    title: Optional[str] = None


# =============================================================================
# Job Response Models
# =============================================================================

class BlogPost(BaseModel):
    """Schema for blog post content"""
    title: str
    meta_description: Optional[str] = None
    introduction: str
    body_sections: List[Dict[str, str]]  # [{"heading": "...", "content": "..."}]
    conclusion: str
    keywords: List[str] = []
    word_count: int


class OutlineSection(BaseModel):
    """Schema for outline section"""
    topic: str
    timestamp: Optional[str] = None
    key_points: List[str]
    notable_quote: Optional[str] = None


class Outline(BaseModel):
    """Schema for outline content"""
    title: str
    overview: str
    sections: List[OutlineSection]
    action_items: List[str] = []
    resources_mentioned: List[str] = []


class SocialPost(BaseModel):
    """Schema for social media post"""
    platform: str  # linkedin, twitter, instagram
    type: str  # insight, quote, question, listicle, teaser
    content: str
    hashtags: List[str] = []
    notes: Optional[str] = None


class JobResult(BaseModel):
    """Schema for job processing result"""
    transcription: Optional[str] = None
    blog_post: Optional[Dict[str, Any]] = None  # BlogPost as dict
    outline: Optional[Dict[str, Any]] = None  # Outline as dict
    social_posts: Optional[List[Dict[str, Any]]] = None  # List of SocialPost as dict


class JobResponse(BaseModel):
    """Schema for job data in API responses"""
    job_id: UUID
    status: JobStatus
    progress: int = Field(..., ge=0, le=100)
    file_name: str
    title: Optional[str] = None
    result: Optional[JobResult] = None
    error_message: Optional[str] = None
    processing_time_seconds: Optional[float] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_job(cls, job):
        """
        Create JobResponse from Job model instance.

        Args:
            job: Job model instance

        Returns:
            JobResponse instance
        """
        result = None
        if job.status == JobStatus.COMPLETED:
            result = JobResult(
                transcription=job.transcription,
                blog_post=job.blog_post,
                outline=job.outline,
                social_posts=job.social_posts,
            )

        return cls(
            job_id=job.id,
            status=job.status,
            progress=job.progress,
            file_name=job.file_name,
            title=job.title,
            result=result,
            error_message=job.error_message,
            processing_time_seconds=job.processing_time_seconds,
            created_at=job.created_at,
            completed_at=job.completed_at,
        )


# =============================================================================
# Job List Response
# =============================================================================

class JobListResponse(BaseModel):
    """Schema for paginated job list"""
    jobs: List[JobResponse]
    total: int
    limit: int
    offset: int
