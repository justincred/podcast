# AudioRepurpose - Technical Architecture

This document provides a deep dive into the technical architecture, design decisions, and implementation details of AudioRepurpose.

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Patterns](#architecture-patterns)
4. [Data Flow](#data-flow)
5. [Database Design](#database-design)
6. [API Design](#api-design)
7. [Background Processing](#background-processing)
8. [AI Integration](#ai-integration)
9. [Security](#security)
10. [Scalability](#scalability)
11. [Monitoring & Observability](#monitoring--observability)

---

## System Overview

AudioRepurpose follows a **microservices-oriented architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Next.js 14 SPA (TypeScript + React)              │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTPS / REST
┌──────────────────────▼──────────────────────────────────────────┐
│                      API Gateway Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │       FastAPI Backend (Python 3.11 + Uvicorn)            │  │
│  │  - Request Validation (Pydantic)                         │  │
│  │  - JWT Authentication                                     │  │
│  │  - Rate Limiting                                          │  │
│  │  - CORS Middleware                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────┬────────────────────────────────────┬────────────────┬────┘
       │                                    │                │
       │ Database Queries                   │ Job Dispatch   │ File Ops
       │                                    │                │
┌──────▼─────────┐    ┌──────────────────▼─────┐    ┌──────▼──────┐
│   PostgreSQL   │    │   Redis (Broker)       │    │    MinIO    │
│   - Users      │    │   - Celery Queue       │    │  S3 Storage │
│   - Jobs       │    │   - Rate Limit Cache   │    │  - Audio    │
│   - Results    │    │   - Session Store      │    │    Files    │
└────────────────┘    └──────────────────┬─────┘    └─────────────┘
                                         │
                      ┌──────────────────▼─────────────────────┐
                      │     Celery Worker Pool (Async)         │
                      │  - Audio Download                      │
                      │  - Transcription (OpenAI Whisper)      │
                      │  - Content Generation (GPT-4)          │
                      │  - Result Storage                      │
                      └────────────────────────────────────────┘
                                         │
                      ┌──────────────────▼─────────────────────┐
                      │          OpenAI API                    │
                      │  - Whisper (Transcription)             │
                      │  - GPT-4 (Content Generation)          │
                      └────────────────────────────────────────┘
```

### Key Components

1. **Frontend (Next.js 14)**: Server-side rendering, client-side interactivity
2. **API Gateway (FastAPI)**: RESTful API with automatic documentation
3. **Task Queue (Celery + Redis)**: Asynchronous background processing
4. **Database (PostgreSQL)**: Relational data persistence
5. **Object Storage (MinIO/S3)**: Audio file storage
6. **AI Services (OpenAI)**: Transcription and content generation

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11 | Primary backend language |
| **FastAPI** | 0.104+ | Modern async web framework |
| **Uvicorn** | 0.24+ | ASGI server |
| **SQLAlchemy** | 2.0+ | ORM for database operations |
| **Alembic** | 1.12+ | Database migrations |
| **Celery** | 5.3+ | Distributed task queue |
| **Redis** | 7.0+ | Message broker & cache |
| **PostgreSQL** | 15+ | Primary database |
| **OpenAI SDK** | 1.3+ | AI API integration |
| **Boto3** | 1.29+ | S3/MinIO client |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.0+ | React framework with SSR |
| **React** | 18.2+ | UI library |
| **TypeScript** | 5.3+ | Type safety |
| **Tailwind CSS** | 3.3+ | Utility-first CSS |
| **Axios** | 1.6+ | HTTP client |
| **Lucide React** | 0.294+ | Icon library |

### Infrastructure

| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Local orchestration |
| **MinIO** | S3-compatible object storage (local dev) |
| **AWS S3** | Object storage (production) |

---

## Architecture Patterns

### 1. Layered Architecture

```
┌─────────────────────────────────────┐
│       Presentation Layer            │  ← Next.js Components
├─────────────────────────────────────┤
│       API Layer                     │  ← FastAPI Routes
├─────────────────────────────────────┤
│       Business Logic Layer          │  ← Services & Tasks
├─────────────────────────────────────┤
│       Data Access Layer             │  ← SQLAlchemy Models
├─────────────────────────────────────┤
│       Data Storage Layer            │  ← PostgreSQL, Redis, S3
└─────────────────────────────────────┘
```

**Benefits**:
- Clear separation of concerns
- Easy to test each layer independently
- Simple to modify or replace layers

### 2. Repository Pattern

Database access is abstracted through SQLAlchemy models:

```python
# app/models/user.py
class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True)
    # ...
```

**Benefits**:
- Decouples business logic from data access
- Easier to mock for testing
- Can swap database implementations

### 3. Dependency Injection

FastAPI's built-in DI system for database sessions and authentication:

```python
@router.get("/jobs/{job_id}")
async def get_job(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ...
```

**Benefits**:
- Automatic resource management (session closing)
- Easy to test with mocked dependencies
- Clean, declarative code

### 4. Service Layer Pattern

Business logic encapsulated in service classes:

```python
# app/services/ai.py
class AIService:
    async def transcribe_audio(self, file_path: str) -> str:
        # Encapsulates OpenAI API calls
```

**Benefits**:
- Reusable across endpoints
- Easier to test
- Clear API boundaries

---

## Data Flow

### Upload & Processing Flow

```
1. User uploads audio via Next.js frontend
   │
   ├─→ FormData with file + optional title
   │
2. POST /api/v1/audio/process
   │
   ├─→ Validate file type & size
   ├─→ Check user quota (free: 3/month, pro: unlimited)
   ├─→ Upload to MinIO/S3
   ├─→ Create Job record in PostgreSQL (status: pending)
   ├─→ Increment user's monthly_uploads_used
   ├─→ Dispatch Celery task: process_audio_task
   │
   └─→ Return JobResponse with job_id
   │
3. Celery Worker picks up task
   │
   ├─→ Update job status to "processing"
   ├─→ Download audio from storage
   ├─→ Call OpenAI Whisper API for transcription
   ├─→ Update job progress: 40%
   ├─→ Call GPT-4 to generate blog post
   ├─→ Update job progress: 60%
   ├─→ Call GPT-4 to generate outline
   ├─→ Update job progress: 80%
   ├─→ Call GPT-4 to generate social posts
   ├─→ Update job progress: 90%
   ├─→ Save all results to Job record
   ├─→ Update job status to "completed"
   ├─→ Update job progress: 100%
   │
   └─→ (Optional) Send webhook notification
   │
4. Frontend polls GET /api/v1/jobs/{job_id} every 2 seconds
   │
   └─→ Display results when status = "completed"
```

### Authentication Flow

```
1. User registers: POST /api/v1/auth/register
   │
   ├─→ Validate email format & password strength
   ├─→ Hash password with bcrypt
   ├─→ Create User record
   ├─→ Generate JWT token with user_id in payload
   │
   └─→ Return { user, access_token }

2. User stores token in localStorage

3. Subsequent requests include: Authorization: Bearer <token>
   │
   ├─→ FastAPI middleware validates JWT
   ├─→ Extracts user_id from token
   ├─→ Loads User from database
   │
   └─→ Injects current_user into route handler
```

---

## Database Design

### Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    tier VARCHAR(10) NOT NULL DEFAULT 'free',  -- 'free' or 'pro'
    monthly_uploads_used INTEGER NOT NULL DEFAULT 0,
    last_upload_reset TIMESTAMP NOT NULL DEFAULT NOW(),
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    webhook_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Jobs table
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL,  -- 'pending', 'processing', 'completed', 'failed'
    progress INTEGER NOT NULL DEFAULT 0,
    file_url VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    title VARCHAR(500),
    transcription TEXT,
    blog_post JSONB,
    outline JSONB,
    social_posts JSONB,
    error_message TEXT,
    processing_time_seconds FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
```

### Indexing Strategy

1. **Email index**: Fast user lookups during authentication
2. **User ID index on jobs**: Efficient filtering of jobs by user
3. **Status index on jobs**: Quick filtering for monitoring
4. **Created_at descending**: Fast retrieval of recent jobs

### Why JSONB for Results?

- **Flexibility**: Schema can evolve without migrations
- **Performance**: PostgreSQL JSONB is indexed and fast
- **Queryability**: Can query nested fields if needed
- **Simplicity**: No need for separate tables for each content type

---

## API Design

### RESTful Principles

- **Resource-based URLs**: `/users`, `/jobs`, `/audio`
- **HTTP verbs**: GET (read), POST (create), DELETE (delete)
- **Status codes**: 200 (OK), 201 (Created), 401 (Unauthorized), etc.
- **JSON responses**: Consistent structure

### Authentication: JWT Bearer Tokens

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Token Payload**:
```json
{
  "sub": "user-uuid",
  "exp": 1234567890
}
```

**Why JWT?**
- Stateless (no server-side session storage)
- Self-contained (all user info in token)
- Scalable (works across multiple servers)

### Error Handling

Consistent error response format:

```json
{
  "detail": "Error message here"
}
```

HTTP status codes:
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing/invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `413`: Payload Too Large (file size exceeded)
- `429`: Too Many Requests (rate limit)
- `500`: Internal Server Error

### API Versioning

All endpoints prefixed with `/api/v1` for future compatibility.

---

## Background Processing

### Why Celery?

Audio processing can take 30-120 seconds:
- **Transcription**: 10-60 seconds (depends on file length)
- **Content generation**: 20-60 seconds (3 AI calls)

Blocking HTTP requests would:
- Timeout
- Waste server resources
- Poor UX

**Celery Benefits**:
- Asynchronous execution
- Retry mechanisms
- Task prioritization
- Distributed workers

### Task Structure

```python
@celery_app.task(bind=True, name="app.tasks.process_audio.process_audio_task")
def process_audio_task(self, job_id: str):
    # 1. Download audio from storage
    # 2. Transcribe with OpenAI Whisper
    # 3. Generate blog post with GPT-4
    # 4. Generate outline with GPT-4
    # 5. Generate social posts with GPT-4
    # 6. Update job status & results
```

### Error Handling in Tasks

```python
try:
    # Process audio
except Exception as e:
    job.status = JobStatus.FAILED
    job.error_message = str(e)
    db.commit()
    raise
```

Failed jobs:
- Status set to "failed"
- Error message stored
- User can retry with new upload

### Scheduled Tasks (Celery Beat)

```python
# Reset monthly upload counters (1st of month)
@celery_app.task(name="app.tasks.scheduled.reset_monthly_uploads")
def reset_monthly_uploads():
    # Set all users' monthly_uploads_used = 0

# Clean up old jobs (weekly)
@celery_app.task(name="app.tasks.scheduled.cleanup_old_jobs")
def cleanup_old_jobs(days_old=90):
    # Delete jobs > 90 days old
```

---

## AI Integration

### OpenAI API Usage

#### 1. Transcription (Whisper API)

```python
client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
)
```

**Cost**: ~$0.006 per minute of audio

#### 2. Content Generation (GPT-4)

```python
client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": PROMPT}
    ],
    temperature=0.7,
    max_tokens=2500
)
```

**Cost**: ~$0.01-0.03 per generation (depends on input length)

### Prompt Engineering Strategy

See `backend/app/core/prompts.py` for full templates.

**Key Principles**:
1. **Clear instructions**: Explicit output format (JSON)
2. **Examples**: Show desired structure
3. **Constraints**: Word counts, tone, platform-specific
4. **System message**: Sets context for all prompts

**Blog Post Prompt**:
- Requests: title, intro, body sections, conclusion, keywords
- Specifies: 800-1500 words, SEO-friendly
- Returns: Structured JSON

**Social Posts Prompt**:
- Requests: 5-10 posts for different platforms
- Specifies: Character limits, hashtag usage
- Returns: Array of posts with metadata

### Error Handling

- **Retry logic**: 3 attempts with exponential backoff
- **Fallback**: If JSON parsing fails, wrap raw text
- **Logging**: All API calls logged for debugging

---

## Security

### Authentication

- **Password hashing**: Bcrypt with salt
- **JWT tokens**: HS256 algorithm, 7-day expiration
- **Secret key**: Env variable, min 32 characters

### Authorization

- **User isolation**: Jobs filtered by `user_id`
- **Quota enforcement**: Checked before upload
- **File size limits**: Tier-based (50MB free, 200MB pro)

### Input Validation

- **Pydantic schemas**: Automatic validation
- **File type check**: Extension whitelist
- **SQL injection**: Protected by SQLAlchemy parameterization
- **XSS**: React auto-escapes output

### CORS

Configured origins in `app/core/config.py`:
```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourproductiondomain.com"
]
```

### Rate Limiting

(Optional) Add via FastAPI middleware:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
@router.post("/audio/process")
```

---

## Scalability

### Current Architecture Supports:

- **Horizontal scaling**: Multiple Celery workers
- **Database connection pooling**: SQLAlchemy built-in
- **Stateless API**: JWT auth, no session storage
- **Object storage**: S3 scales infinitely

### Scaling Strategy

| Load Level | Users | Uploads/day | Infrastructure |
|------------|-------|-------------|----------------|
| **MVP** | <100 | <50 | Single VPS (DigitalOcean $20/mo) |
| **Growth** | 100-1000 | 50-500 | Separate DB, 2-3 Celery workers |
| **Scale** | 1000-10k | 500-5000 | Managed DB, Auto-scaling workers |
| **Enterprise** | 10k+ | 5000+ | Kubernetes, multi-region |

### Bottlenecks & Solutions

1. **Database Queries**
   - Add read replicas
   - Cache frequent queries in Redis
   - Denormalize if needed

2. **Celery Queue**
   - Add more workers
   - Use task priorities
   - Split into separate queues (fast/slow)

3. **OpenAI API**
   - Rate limiting (free tier: 3 req/min)
   - Retry with exponential backoff
   - Consider caching common transcriptions

---

## Monitoring & Observability

### Logging

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processing job {job_id}")
logger.error(f"Failed to transcribe: {error}")
```

**Log Levels**:
- `DEBUG`: Development only
- `INFO`: Job lifecycle events
- `WARNING`: Recoverable issues
- `ERROR`: Failed operations

### Error Tracking (Optional)

Integrate Sentry:
```python
import sentry_sdk
sentry_sdk.init(dsn=settings.SENTRY_DSN)
```

### Metrics to Track

**Business Metrics**:
- Signups per day
- Uploads per day
- Free → Pro conversions
- MRR (Monthly Recurring Revenue)

**Technical Metrics**:
- API response times (p50, p95, p99)
- Celery task duration
- OpenAI API latency
- Database query times
- Error rates

**User Metrics**:
- Daily Active Users (DAU)
- Retention (Day 1, Day 7, Day 30)
- Upload success rate
- Time to result

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": check_db_connection(),
        "redis": check_redis_connection(),
        "celery": check_celery_workers(),
    }
```

---

## Future Enhancements

### Short Term (1-3 months)

- [ ] PDF/DOCX export
- [ ] Custom AI prompts (user-defined)
- [ ] Webhook notifications on job completion
- [ ] Team accounts (shared uploads)

### Medium Term (3-6 months)

- [ ] Video support (extract audio)
- [ ] Multi-language transcription
- [ ] SEO analysis and recommendations
- [ ] Integration with CMS (WordPress, Ghost)

### Long Term (6-12 months)

- [ ] Real-time transcription (WebSockets)
- [ ] Custom AI models (fine-tuned)
- [ ] Analytics dashboard (engagement metrics)
- [ ] API for third-party integrations

---

## Conclusion

This architecture balances:
- **Simplicity**: Easy to understand and modify
- **Performance**: Async processing, optimized queries
- **Scalability**: Can grow from 10 to 10,000 users
- **Cost-effectiveness**: Start cheap, scale as revenue grows

The modular design allows replacing components (e.g., switch from MinIO to S3, or GPT-4 to Claude) without major refactoring.
