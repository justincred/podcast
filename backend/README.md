# AudioRepurpose Backend Documentation

Complete documentation for the FastAPI + Celery backend.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Setup & Installation](#setup--installation)
4. [Configuration](#configuration)
5. [Database](#database)
6. [API Endpoints](#api-endpoints)
7. [Background Tasks](#background-tasks)
8. [Services](#services)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Common Tasks](#common-tasks)
12. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │   Schemas    │  │  Middleware  │     │
│  │  (API Endpoints)│  (Validation)│  │  (CORS, Auth)│     │
│  └──────┬───────┘  └──────────────┘  └──────────────┘     │
│         │                                                    │
│  ┌──────▼───────────────────────────────────────────┐     │
│  │              Dependencies Layer                   │     │
│  │  - get_db() → Database sessions                   │     │
│  │  - get_current_user() → Authentication           │     │
│  └──────┬───────────────────────────────────────────┘     │
│         │                                                    │
│  ┌──────▼───────────────────────────────────────────┐     │
│  │              Services Layer                       │     │
│  │  - AIService (OpenAI integration)                 │     │
│  │  - StorageService (S3/MinIO)                      │     │
│  └──────┬───────────────────────────────────────────┘     │
│         │                                                    │
│  ┌──────▼───────────────────────────────────────────┐     │
│  │          Database Models (SQLAlchemy)             │     │
│  │  - User, Job                                      │     │
│  └──────┬───────────────────────────────────────────┘     │
└─────────┼───────────────────────────────────────────────────┘
          │
    ┌─────▼─────┐           ┌──────────────┐
    │PostgreSQL │           │ Celery Workers│
    │ Database  │           │  (Async Tasks)│
    └───────────┘           └──────────────┘
```

### Technology Stack

- **FastAPI 0.104+**: Modern async web framework
- **Uvicorn**: ASGI server for production
- **SQLAlchemy 2.0**: Async ORM
- **Alembic**: Database migrations
- **Celery 5.3**: Distributed task queue
- **Redis**: Message broker
- **PostgreSQL 15**: Primary database
- **OpenAI SDK**: AI integration
- **Boto3**: S3/MinIO client

---

## Project Structure

```
backend/
├── app/
│   ├── api/                      # API layer
│   │   ├── routes/               # Endpoint definitions
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   ├── audio.py          # Audio upload endpoints
│   │   │   └── jobs.py           # Job management endpoints
│   │   └── deps.py               # Dependency injection
│   │
│   ├── core/                     # Core functionality
│   │   ├── config.py             # Configuration (from env)
│   │   ├── security.py           # JWT, password hashing
│   │   └── prompts.py            # AI prompt templates
│   │
│   ├── db/                       # Database
│   │   └── base.py               # Database session management
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py           # Export all models
│   │   ├── user.py               # User model
│   │   └── job.py                # Job model
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── user.py               # User validation schemas
│   │   └── job.py                # Job validation schemas
│   │
│   ├── services/                 # Business logic
│   │   ├── ai.py                 # OpenAI integration
│   │   └── storage.py            # S3/MinIO integration
│   │
│   ├── tasks/                    # Celery tasks
│   │   ├── celery_app.py         # Celery configuration
│   │   ├── process_audio.py      # Main processing task
│   │   └── scheduled.py          # Scheduled tasks (beat)
│   │
│   └── main.py                   # FastAPI application
│
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   ├── env.py                    # Alembic environment
│   └── script.py.mako            # Migration template
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_auth.py              # Authentication tests
│   ├── test_audio.py             # Audio upload tests
│   └── test_jobs.py              # Job tests
│
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
└── README.md                     # This file
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- OpenAI API key

### Local Development Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp ../.env.example ../.env
# Edit .env and set OPENAI_API_KEY

# 4. Start PostgreSQL and Redis
# Option A: Using Docker
docker-compose up -d postgres redis

# Option B: Using local installations
# (Ensure PostgreSQL and Redis are running)

# 5. Run database migrations
alembic upgrade head

# 6. Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. In another terminal, start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info

# 8. (Optional) Start Celery beat for scheduled tasks
celery -A app.tasks.celery_app beat --loglevel=info
```

### Docker Setup

```bash
# Start all services with Docker Compose
docker-compose up --build backend celery-worker
```

### Verify Installation

```bash
# Test API health
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","service":"audiorepurpose-backend"}

# View API documentation
open http://localhost:8000/docs
```

---

## Configuration

Configuration is managed via environment variables using Pydantic Settings.

### Environment Variables

See `app/core/config.py` for all available settings.

**Required:**
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

**Optional (with defaults):**
```bash
# General
ENVIRONMENT=development
DEBUG=true
PROJECT_NAME=AudioRepurpose

# Database
POSTGRES_USER=audiorepurpose
POSTGRES_PASSWORD=changeme_securepwd123
POSTGRES_DB=audiorepurpose_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

# OpenAI
OPENAI_TRANSCRIPTION_MODEL=whisper-1
OPENAI_CHAT_MODEL=gpt-4-turbo-preview

# Storage
STORAGE_TYPE=minio  # or 's3'
MINIO_ENDPOINT=localhost:9000

# Usage Limits
FREE_TIER_MONTHLY_UPLOADS=3
PRO_TIER_MONTHLY_UPLOADS=999999
MAX_FILE_SIZE_MB_FREE=50
MAX_FILE_SIZE_MB_PRO=200
```

### Configuration Class

```python
from app.core.config import settings

# Access configuration
print(settings.OPENAI_API_KEY)
print(settings.DATABASE_URL)
print(settings.FREE_TIER_MONTHLY_UPLOADS)
```

---

## Database

### Models

#### User Model (`app/models/user.py`)

```python
class User(Base):
    __tablename__ = "users"

    id: UUID              # Primary key
    email: str            # Unique, indexed
    hashed_password: str  # Bcrypt hash
    full_name: str        # Optional
    tier: UserTier        # 'free' or 'pro'
    monthly_uploads_used: int
    last_upload_reset: datetime
    stripe_customer_id: str      # Optional
    stripe_subscription_id: str  # Optional
    webhook_url: str             # Optional
    created_at: datetime
    updated_at: datetime

    # Relationships
    jobs: List[Job]  # One-to-many
```

**Properties:**
- `is_pro` → bool: Check if user has Pro tier
- `uploads_remaining` → int: Remaining uploads for current month
- `max_file_size_bytes` → int: Max file size based on tier

#### Job Model (`app/models/job.py`)

```python
class Job(Base):
    __tablename__ = "jobs"

    id: UUID              # Primary key
    user_id: UUID         # Foreign key to users
    status: JobStatus     # 'pending', 'processing', 'completed', 'failed'
    progress: int         # 0-100
    file_url: str         # S3/MinIO URL
    file_name: str
    file_size_bytes: int
    title: str            # Optional
    transcription: str    # Result
    blog_post: dict       # JSONB
    outline: dict         # JSONB
    social_posts: list    # JSONB
    error_message: str    # If failed
    processing_time_seconds: float
    created_at: datetime
    started_at: datetime
    completed_at: datetime

    # Relationships
    user: User  # Many-to-one
```

**Properties:**
- `is_completed` → bool
- `is_failed` → bool
- `is_processing` → bool
- `to_dict()` → dict: Serialize for API

### Migrations

#### Create a New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new field to User"

# Edit the generated file in alembic/versions/
# Review the upgrade() and downgrade() functions

# Apply migration
alembic upgrade head
```

#### Common Migration Commands

```bash
# Show current migration version
alembic current

# Show migration history
alembic history

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>
```

#### Example Migration

```python
# alembic/versions/2024_01_15_1234-add_webhook_url.py

def upgrade() -> None:
    op.add_column('users', sa.Column('webhook_url', sa.String(500), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'webhook_url')
```

### Database Queries

#### Using SQLAlchemy

```python
from sqlalchemy.orm import Session
from app.models import User, Job, JobStatus

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_jobs(db: Session, user_id: str, limit: int = 10):
    return db.query(Job)\
        .filter(Job.user_id == user_id)\
        .order_by(Job.created_at.desc())\
        .limit(limit)\
        .all()

def update_job_status(db: Session, job_id: str, status: JobStatus):
    job = db.query(Job).filter(Job.id == job_id).first()
    job.status = status
    db.commit()
    db.refresh(job)
    return job
```

---

## API Endpoints

### Authentication (`/api/v1/auth`)

#### Register User

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "full_name": "John Doe"  // optional
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "tier": "free",
    "monthly_uploads_used": 0,
    "uploads_remaining": 3,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response (200):**
```json
{
  "user": { ... },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "tier": "free",
  "uploads_remaining": 2
}
```

### Audio Processing (`/api/v1/audio`)

#### Upload Audio

```http
POST /api/v1/audio/process
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <audio_file.mp3>
title: "My Podcast Episode"  // optional
```

**Response (202):**
```json
{
  "job_id": "uuid",
  "status": "pending",
  "progress": 0,
  "file_name": "audio.mp3",
  "title": "My Podcast Episode",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400`: Invalid file type/size
- `413`: File too large
- `429`: Upload quota exceeded

### Jobs (`/api/v1/jobs`)

#### Get Job by ID

```http
GET /api/v1/jobs/{job_id}
Authorization: Bearer <token>
```

**Response (200) - Processing:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "progress": 45,
  "file_name": "audio.mp3",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Response (200) - Completed:**
```json
{
  "job_id": "uuid",
  "status": "completed",
  "progress": 100,
  "result": {
    "transcription": "Full transcription text...",
    "blog_post": {
      "title": "...",
      "introduction": "...",
      "body_sections": [...],
      "conclusion": "...",
      "word_count": 1200
    },
    "outline": {
      "title": "...",
      "sections": [...]
    },
    "social_posts": [...]
  },
  "processing_time_seconds": 45.2,
  "completed_at": "2024-01-15T10:31:00Z"
}
```

#### List User Jobs

```http
GET /api/v1/jobs?limit=10&offset=0
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "jobs": [...],
  "total": 25,
  "limit": 10,
  "offset": 0
}
```

#### Delete Job

```http
DELETE /api/v1/jobs/{job_id}
Authorization: Bearer <token>
```

**Response (204):** No content

---

## Background Tasks

### Celery Configuration

Located in `app/tasks/celery_app.py`:

```python
celery_app = Celery(
    "audiorepurpose",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Task settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_time_limit=1800,  # 30 minutes max
)
```

### Main Processing Task

`app/tasks/process_audio.py`:

```python
@celery_app.task(bind=True)
def process_audio_task(self, job_id: str):
    # 1. Download audio from storage
    # 2. Transcribe with OpenAI Whisper
    # 3. Generate blog post
    # 4. Generate outline
    # 5. Generate social posts
    # 6. Update job status
```

**Task Flow:**
```
1. Download audio (progress: 20%)
2. Transcribe (progress: 40%)
3. Generate blog post (progress: 60%)
4. Generate outline (progress: 80%)
5. Generate social posts (progress: 90%)
6. Save results (progress: 100%)
```

### Scheduled Tasks

`app/tasks/scheduled.py`:

```python
# Reset monthly uploads (1st of month)
@celery_app.task
def reset_monthly_uploads():
    # Set all users' monthly_uploads_used = 0
    pass

# Clean up old jobs (weekly)
@celery_app.task
def cleanup_old_jobs(days_old=90):
    # Delete jobs older than 90 days
    pass
```

### Running Celery

```bash
# Worker (process tasks)
celery -A app.tasks.celery_app worker --loglevel=info

# Beat (scheduled tasks)
celery -A app.tasks.celery_app beat --loglevel=info

# Monitor tasks
celery -A app.tasks.celery_app inspect active
celery -A app.tasks.celery_app inspect stats
```

---

## Services

### AI Service (`app/services/ai.py`)

Handles all OpenAI API interactions.

```python
from app.services.ai import ai_service

# Transcribe audio
transcription = await ai_service.transcribe_audio("path/to/audio.mp3")

# Generate blog post
blog_post = await ai_service.generate_blog_post(transcription)

# Generate outline
outline = await ai_service.generate_outline(transcription)

# Generate social posts
social_posts = await ai_service.generate_social_posts(transcription)
```

### Storage Service (`app/services/storage.py`)

Manages file uploads to S3/MinIO.

```python
from app.services.storage import storage_service

# Upload file
url = storage_service.upload_file(
    file=file_obj,
    file_name="audio.mp3",
    content_type="audio/mpeg"
)

# Download file
storage_service.download_file(url, "local/path.mp3")

# Delete file
storage_service.delete_file(url)

# Get presigned URL (temporary access)
presigned_url = storage_service.get_presigned_url(url, expiration=3600)
```

---

## Testing

### Setup Test Environment

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Create test database
createdb audiorepurpose_test

# Set test environment
export DATABASE_URL=postgresql://user:pass@localhost:5432/audiorepurpose_test
export ENVIRONMENT=test
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_register_user

# Run with output
pytest -v -s
```

### Example Test

```python
# tests/test_auth.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert "access_token" in data
```

---

## Deployment

### Environment Setup

```bash
# Production settings
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-db-url>
REDIS_URL=<production-redis-url>
OPENAI_API_KEY=<your-key>
```

### Using Docker

```bash
# Build production image
docker build -t audiorepurpose-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=$DATABASE_URL \
  -e REDIS_URL=$REDIS_URL \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  audiorepurpose-backend
```

### Platform-Specific Guides

#### Heroku

```bash
# Create app
heroku create audiorepurpose-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head

# Scale workers
heroku ps:scale web=1 worker=1
```

#### DigitalOcean App Platform

```yaml
# .do/app.yaml
name: audiorepurpose
services:
  - name: api
    github:
      repo: your-username/audiorepurpose
      branch: main
    dockerfile_path: backend/Dockerfile
    envs:
      - key: OPENAI_API_KEY
        scope: RUN_AND_BUILD_TIME
        value: ${OPENAI_API_KEY}
databases:
  - name: db
    engine: PG
    version: "15"
```

---

## Common Tasks

### Add a New API Endpoint

1. **Create route in `app/api/routes/`**:

```python
# app/api/routes/my_feature.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter(prefix="/my-feature", tags=["My Feature"])

@router.get("/")
async def get_my_feature(current_user = Depends(get_current_user)):
    return {"message": "Hello from my feature"}
```

2. **Register router in `app/main.py`**:

```python
from app.api.routes import my_feature

app.include_router(my_feature.router, prefix=settings.API_V1_PREFIX)
```

### Add a New Database Model

1. **Create model in `app/models/`**:

```python
# app/models/my_model.py
from sqlalchemy import Column, String
from app.db.base import Base

class MyModel(Base):
    __tablename__ = "my_models"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
```

2. **Create migration**:

```bash
alembic revision --autogenerate -m "Add MyModel"
alembic upgrade head
```

### Add a New Celery Task

```python
# app/tasks/my_task.py
from app.tasks.celery_app import celery_app

@celery_app.task
def my_background_task(arg1, arg2):
    # Do work
    return result

# Dispatch from API
from app.tasks.my_task import my_background_task
my_background_task.delay(arg1, arg2)
```

### Customize AI Prompts

Edit `app/core/prompts.py`:

```python
CUSTOM_PROMPT = """
Your custom prompt here with {transcription} placeholder.
"""

# Use in service
from app.core.prompts import format_prompt, CUSTOM_PROMPT

prompt = format_prompt(CUSTOM_PROMPT, transcription)
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
pg_isready

# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL

# Reset database
dropdb audiorepurpose_db
createdb audiorepurpose_db
alembic upgrade head
```

### Celery Worker Not Processing

```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Check Celery worker logs
celery -A app.tasks.celery_app inspect active

# Restart worker
# Stop current worker (Ctrl+C)
celery -A app.tasks.celery_app worker --loglevel=debug
```

### OpenAI API Errors

```python
# Check API key
from app.core.config import settings
print(settings.OPENAI_API_KEY[:10])  # First 10 chars

# Test API
from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)
response = client.models.list()
```

### Import Errors

```bash
# Ensure you're in virtual environment
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org
- **Celery Documentation**: https://docs.celeryq.dev
- **OpenAI API Reference**: https://platform.openai.com/docs

## Need Help?

- Check the main [README.md](../README.md) for project overview
- See [ARCHITECTURE.md](../ARCHITECTURE.md) for design decisions
- Review API docs at http://localhost:8000/docs
- Check Docker logs: `docker-compose logs -f backend`
