"""
Scheduled Celery tasks (Celery Beat).

These tasks run on a schedule for maintenance operations.
"""
from datetime import datetime, timedelta

from app.tasks.celery_app import celery_app
from app.db.base import SessionLocal
from app.models import User, Job


@celery_app.task(name="app.tasks.scheduled.reset_monthly_uploads")
def reset_monthly_uploads():
    """
    Reset monthly upload counters for all users.
    Runs on the 1st of each month at midnight.
    """
    db = SessionLocal()

    try:
        users = db.query(User).all()
        reset_count = 0

        for user in users:
            user.monthly_uploads_used = 0
            user.last_upload_reset = datetime.utcnow()
            reset_count += 1

        db.commit()
        print(f"Reset monthly uploads for {reset_count} users")

        return {"status": "success", "users_reset": reset_count}

    except Exception as e:
        print(f"Error resetting monthly uploads: {str(e)}")
        db.rollback()
        raise

    finally:
        db.close()


@celery_app.task(name="app.tasks.scheduled.cleanup_old_jobs")
def cleanup_old_jobs(days_old: int = 90):
    """
    Delete jobs older than specified days.
    Runs every Sunday at 2 AM.

    Args:
        days_old: Delete jobs older than this many days (default 90)
    """
    db = SessionLocal()

    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)

        # Find old jobs
        old_jobs = db.query(Job).filter(Job.created_at < cutoff_date).all()

        deleted_count = 0
        for job in old_jobs:
            # Optional: Delete audio file from storage as well
            # try:
            #     from app.services.storage import storage_service
            #     storage_service.delete_file(job.file_url)
            # except:
            #     pass

            db.delete(job)
            deleted_count += 1

        db.commit()
        print(f"Deleted {deleted_count} jobs older than {days_old} days")

        return {"status": "success", "jobs_deleted": deleted_count}

    except Exception as e:
        print(f"Error cleaning up old jobs: {str(e)}")
        db.rollback()
        raise

    finally:
        db.close()
