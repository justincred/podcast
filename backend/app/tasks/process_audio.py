"""
Celery task for processing audio files.

This is the main background task that handles:
1. Downloading audio from storage
2. Transcribing with OpenAI Whisper
3. Generating blog post, outline, and social posts with GPT-4
4. Updating job status in database
"""
import os
import time
from datetime import datetime
from uuid import UUID

from app.tasks.celery_app import celery_app
from app.db.base import SessionLocal
from app.models import Job, JobStatus
from app.services.storage import storage_service
from app.services.ai import ai_service


@celery_app.task(bind=True, name="app.tasks.process_audio.process_audio_task")
def process_audio_task(self, job_id: str):
    """
    Process an audio file: transcribe and generate content.

    Args:
        job_id: UUID of the job to process

    Returns:
        Dictionary with processing results
    """
    db = SessionLocal()
    start_time = time.time()

    try:
        # Get job from database
        job = db.query(Job).filter(Job.id == UUID(job_id)).first()
        if not job:
            raise Exception(f"Job {job_id} not found")

        # Update job status to processing
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()
        job.progress = 10
        db.commit()

        # Step 1: Download audio file from storage
        print(f"[Job {job_id}] Downloading audio file...")
        local_audio_path = f"/tmp/uploads/{job_id}.audio"
        os.makedirs("/tmp/uploads", exist_ok=True)

        storage_service.download_file(job.file_url, local_audio_path)
        job.progress = 20
        db.commit()

        # Step 2: Transcribe audio
        print(f"[Job {job_id}] Transcribing audio...")
        import asyncio
        transcription = asyncio.run(ai_service.transcribe_audio(local_audio_path))

        job.transcription = transcription
        job.progress = 40
        db.commit()

        # Step 3: Generate blog post
        print(f"[Job {job_id}] Generating blog post...")
        blog_post = asyncio.run(ai_service.generate_blog_post(transcription))

        job.blog_post = blog_post
        job.progress = 60
        db.commit()

        # Step 4: Generate outline
        print(f"[Job {job_id}] Generating outline...")
        outline = asyncio.run(ai_service.generate_outline(transcription))

        job.outline = outline
        job.progress = 80
        db.commit()

        # Step 5: Generate social media posts
        print(f"[Job {job_id}] Generating social media posts...")
        social_posts = asyncio.run(ai_service.generate_social_posts(transcription))

        job.social_posts = social_posts
        job.progress = 90
        db.commit()

        # Step 6: Mark job as completed
        processing_time = time.time() - start_time
        job.status = JobStatus.COMPLETED
        job.progress = 100
        job.completed_at = datetime.utcnow()
        job.processing_time_seconds = processing_time
        db.commit()

        print(f"[Job {job_id}] Completed in {processing_time:.2f} seconds")

        # Clean up local file
        try:
            os.remove(local_audio_path)
        except:
            pass

        # TODO: Send webhook notification if user has webhook_url configured
        # if job.user.webhook_url:
        #     send_webhook_notification(job.user.webhook_url, job.to_dict())

        return {
            "job_id": job_id,
            "status": "completed",
            "processing_time": processing_time,
        }

    except Exception as e:
        # Handle errors
        print(f"[Job {job_id}] Error: {str(e)}")

        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            job.processing_time_seconds = time.time() - start_time
            db.commit()

        # Clean up local file if exists
        try:
            os.remove(local_audio_path)
        except:
            pass

        raise

    finally:
        db.close()
