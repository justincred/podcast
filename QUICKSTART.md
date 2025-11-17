# AudioRepurpose Quick Start Guide

Get your AudioRepurpose platform running in 5 minutes!

## Prerequisites

Before you begin, ensure you have:

- [x] **Docker Desktop** installed and running
- [x] **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- [x] **Git** (for cloning the repository)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd audiorepurpose
```

### 2. Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file and add your OpenAI API key
nano .env  # or use your preferred editor
```

**Required: Set your OpenAI API key**
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

All other settings have sensible defaults for local development.

### 3. Start All Services

```bash
# Build and start all services (this may take a few minutes the first time)
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d
```

This command starts:
- PostgreSQL database
- Redis cache and message broker
- MinIO object storage
- FastAPI backend server
- Celery worker for background jobs
- Celery beat for scheduled tasks
- Next.js frontend

### 4. Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

### 5. Create Your Account

1. Navigate to http://localhost:3000
2. Click "Get Started Free"
3. Fill in your details:
   - Email: your@email.com
   - Password: (minimum 8 characters)
   - Full Name: (optional)
4. Click "Create Account"

You'll be automatically logged in and redirected to the dashboard.

### 6. Upload Your First Audio File

1. On the dashboard, click "Upload Audio" or drag-and-drop
2. Select an audio file (MP3, WAV, M4A, OGG, or FLAC - max 50MB for free tier)
3. Optionally add a title
4. Click "Upload & Process"

Processing typically takes 30-90 seconds. You'll see:
- Real-time progress updates
- AI-generated transcription
- Professional blog post (800-1500 words)
- Structured outline with key points
- 5-10 social media posts

### 7. View and Export Results

Click on any job to view results. You can:
- Copy content to clipboard
- Download as text files
- Switch between different content formats using tabs

## Useful Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery-worker
docker-compose logs -f frontend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

### Restart a Service

```bash
# Restart backend only
docker-compose restart backend

# Restart Celery worker
docker-compose restart celery-worker
```

### Access Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U audiorepurpose -d audiorepurpose_db

# View tables
\dt

# View users
SELECT id, email, tier, monthly_uploads_used FROM users;

# Exit
\q
```

### Run Backend Commands

```bash
# Access backend shell
docker-compose exec backend bash

# Run Alembic migrations
docker-compose exec backend alembic upgrade head

# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## Troubleshooting

### Port Conflicts

If ports 3000, 8000, 5432, 6379, or 9000 are already in use:

1. Stop conflicting services
2. Or modify ports in `docker-compose.yml`

### OpenAI API Errors

If you see "OpenAI API key not set" errors:

1. Verify your API key is correct in `.env`
2. Restart services: `docker-compose restart backend celery-worker`
3. Check you have API credits: https://platform.openai.com/usage

### Slow Processing

If audio processing is slow:

1. Check your internet connection (API calls to OpenAI)
2. Verify Celery worker is running: `docker-compose logs celery-worker`
3. Try a shorter audio file first

### Database Errors

If you see database connection errors:

```bash
# Reset the database
docker-compose down -v
docker-compose up -d postgres
sleep 5  # Wait for PostgreSQL to start
docker-compose up -d
```

### Frontend Not Loading

```bash
# Rebuild frontend
docker-compose up --build frontend

# Check frontend logs
docker-compose logs -f frontend
```

## Next Steps

### For Development

1. **Backend Development**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Development**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### For Production

1. Review security settings in `.env`
2. Set strong passwords for all services
3. Use production-grade database (managed PostgreSQL)
4. Configure AWS S3 instead of MinIO
5. Set up proper domain and SSL certificates
6. Configure Sentry for error tracking
7. Set up Stripe for payments

### Add Features

See the main README.md "How to Extend" section for:
- Adding new content formats
- Integrating different AI providers
- Adding webhook notifications
- Implementing PDF/DOCX export

## Support

- **Documentation**: See main README.md
- **API Docs**: http://localhost:8000/docs (interactive Swagger UI)
- **GitHub Issues**: Report bugs or request features

## Test API with cURL

### Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Save the `access_token` from the response.

### Upload Audio

```bash
curl -X POST http://localhost:8000/api/v1/audio/process \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -F "file=@/path/to/your/audio.mp3" \
  -F "title=My Podcast Episode"
```

### Check Job Status

```bash
curl http://localhost:8000/api/v1/jobs/JOB_ID_HERE \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

**You're all set!** 🎉

Start transforming your audio content into written gold. If you run into issues, check the Troubleshooting section above.
