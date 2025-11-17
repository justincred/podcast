"""
Celery application configuration for background task processing.
"""
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


# Initialize Celery app
celery_app = Celery(
    "audiorepurpose",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# Auto-discover tasks from tasks module
celery_app.autodiscover_tasks(["app.tasks"])

# Scheduled tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    # Reset monthly upload counters on the 1st of each month at midnight
    "reset-monthly-uploads": {
        "task": "app.tasks.scheduled.reset_monthly_uploads",
        "schedule": crontab(minute=0, hour=0, day_of_month=1),
    },
    # Clean up old jobs older than 90 days
    "cleanup-old-jobs": {
        "task": "app.tasks.scheduled.cleanup_old_jobs",
        "schedule": crontab(minute=0, hour=2, day_of_week=0),  # Every Sunday at 2 AM
    },
}
