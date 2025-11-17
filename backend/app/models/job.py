"""
Job database model for audio processing tasks.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class JobStatus(str, enum.Enum):
    """Job processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base):
    """
    Job model for tracking audio processing tasks.

    Each job represents one audio file upload and its generated content.
    """
    __tablename__ = "jobs"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Job status
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False, index=True)
    progress = Column(Integer, default=0, nullable=False)  # 0-100

    # File information
    file_url = Column(String, nullable=False)  # S3/MinIO URL
    file_name = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    title = Column(String, nullable=True)  # Optional user-provided title

    # Processing results
    transcription = Column(Text, nullable=True)
    blog_post = Column(JSONB, nullable=True)  # JSON structure with title, content, etc.
    outline = Column(JSONB, nullable=True)  # JSON structure with sections
    social_posts = Column(JSONB, nullable=True)  # Array of social media posts

    # Error handling
    error_message = Column(Text, nullable=True)

    # Performance metrics
    processing_time_seconds = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="jobs")

    def __repr__(self):
        return f"<Job {self.id} ({self.status})>"

    @property
    def is_completed(self) -> bool:
        """Check if job has completed successfully"""
        return self.status == JobStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """Check if job has failed"""
        return self.status == JobStatus.FAILED

    @property
    def is_processing(self) -> bool:
        """Check if job is currently being processed"""
        return self.status in [JobStatus.PENDING, JobStatus.PROCESSING]

    def to_dict(self) -> dict:
        """
        Convert job to dictionary for API responses.

        Returns:
            Dictionary representation of job
        """
        return {
            "job_id": str(self.id),
            "status": self.status.value,
            "progress": self.progress,
            "file_name": self.file_name,
            "title": self.title,
            "transcription": self.transcription,
            "blog_post": self.blog_post,
            "outline": self.outline,
            "social_posts": self.social_posts,
            "error_message": self.error_message,
            "processing_time_seconds": self.processing_time_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
