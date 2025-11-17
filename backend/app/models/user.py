"""
User database model.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class UserTier(str, enum.Enum):
    """User subscription tier"""
    FREE = "free"
    PRO = "pro"


class User(Base):
    """
    User model for authentication and subscription management.

    Tracks user credentials, subscription tier, and usage quotas.
    """
    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Authentication
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    # Subscription tier
    tier = Column(Enum(UserTier), default=UserTier.FREE, nullable=False)

    # Usage tracking
    monthly_uploads_used = Column(Integer, default=0, nullable=False)
    last_upload_reset = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Stripe integration (for Pro tier)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)

    # Optional: Webhook URL for job completion notifications
    webhook_url = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    jobs = relationship("Job", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email} ({self.tier})>"

    @property
    def is_pro(self) -> bool:
        """Check if user has Pro subscription"""
        return self.tier == UserTier.PRO

    @property
    def uploads_remaining(self) -> int:
        """Get remaining uploads for current month"""
        from app.core.config import settings

        max_uploads = (
            settings.PRO_TIER_MONTHLY_UPLOADS
            if self.is_pro
            else settings.FREE_TIER_MONTHLY_UPLOADS
        )
        return max(0, max_uploads - self.monthly_uploads_used)

    @property
    def max_file_size_bytes(self) -> int:
        """Get maximum file size based on tier"""
        from app.core.config import settings

        return (
            settings.MAX_FILE_SIZE_BYTES_PRO
            if self.is_pro
            else settings.MAX_FILE_SIZE_BYTES_FREE
        )
