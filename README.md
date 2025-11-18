# AudioRepurpose 🎙️ → 📝

**Transform your audio content into engaging written content automatically.**

AudioRepurpose uses AI to transcribe audio files and generate multiple content formats: blog posts, outlines, and social media posts. Perfect for podcasters, content creators, and marketers.

[![Production Ready](https://img.shields.io/badge/status-production--ready-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

## 🚀 Features

### MVP Feature Set
- **Audio Upload**: Support for MP3, WAV, M4A, OGG (up to 100MB free tier)
- **AI Transcription**: OpenAI Whisper API integration
- **Content Generation**:
  - Long-form blog post (800-1500 words)
  - Structured outline (bullet points with timestamps)
  - 5-10 social media posts (LinkedIn/Twitter optimized)
- **Async Processing**: Background job queue with real-time status updates
- **User Authentication**: JWT-based auth with usage tracking
- **Freemium Model**: Free tier (3 uploads/month) + Pro tier (unlimited)

### Tech Stack
- **Backend**: Python 3.11 + FastAPI + Celery + Redis
- **Frontend**: Next.js 14 (App Router) + TypeScript + TailwindCSS
- **Database**: PostgreSQL 15
- **Storage**: S3-compatible (MinIO for local, AWS S3 for production)
- **AI**: OpenAI API (Whisper + GPT-4)
- **Infrastructure**: Docker + Docker Compose

## 📋 Prerequisites

- Docker & Docker Compose
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

## 🏃 Quick Start

### 1. Clone and Configure

```bash
git clone <your-repo-url>
cd audiorepurpose

# Copy environment variables
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

### 2. Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

### 4. Test the System

```bash
# Create a test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

## 🛠️ Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start FastAPI dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start Next.js dev server
npm run dev
```

## 📚 Documentation

This project includes comprehensive documentation for developers:

- **[README.md](README.md)** - This file: Project overview, quick start, features
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive and design decisions
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete REST API documentation
- **[backend/README.md](backend/README.md)** - Backend development guide
- **[frontend/README.md](frontend/README.md)** - Frontend development guide
- **[SUMMARY.md](SUMMARY.md)** - Implementation summary and next steps

### Interactive API Docs

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## 📚 API Documentation

### Authentication

#### Register User
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

#### Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

# Returns:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

### Audio Processing

#### Upload Audio
```bash
POST /api/v1/audio/process
Authorization: Bearer <token>
Content-Type: multipart/form-data

# Form data:
# - file: audio file (MP3, WAV, M4A, OGG)
# - title: optional title

# Returns:
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2025-11-17T10:30:00Z"
}
```

#### Check Job Status
```bash
GET /api/v1/jobs/{job_id}
Authorization: Bearer <token>

# Returns:
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "result": {
    "transcription": "Full transcription text...",
    "blog_post": {
      "title": "...",
      "content": "...",
      "word_count": 1200
    },
    "outline": {
      "sections": [...]
    },
    "social_posts": [
      {
        "platform": "linkedin",
        "content": "...",
        "hashtags": ["#podcast", "#AI"]
      }
    ]
  },
  "processing_time_seconds": 45.2
}
```

#### Get User Jobs
```bash
GET /api/v1/jobs?limit=10&offset=0
Authorization: Bearer <token>

# Returns paginated list of user's jobs
```

## 🏗️ Architecture Details

### Backend Flow

1. **Upload**: User uploads audio file via Next.js frontend
2. **Validation**: FastAPI validates file type, size, user quota
3. **Storage**: File saved to S3/MinIO with unique UUID
4. **Job Creation**: Job record created in PostgreSQL with status "pending"
5. **Task Dispatch**: Celery task dispatched to worker queue
6. **Processing**:
   - Worker downloads audio from storage
   - Calls OpenAI Whisper API for transcription
   - Uses GPT-4 with specialized prompts to generate:
     - Blog post (with title, intro, body, conclusion)
     - Outline (structured with timestamps)
     - Social posts (platform-specific formats)
7. **Result Storage**: All generated content saved to database
8. **Webhook**: Optional webhook notification on completion

### Prompt Engineering

The system uses carefully crafted prompts for each content type:

- **Blog Post**: Instructed to write engaging, SEO-friendly content with proper structure
- **Outline**: Creates scannable bullet points with key timestamps
- **Social Posts**: Platform-specific (LinkedIn: professional, Twitter: concise with hashtags)

See `backend/app/core/prompts.py` for full prompt templates.

### Database Schema

```sql
-- Users table
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  hashed_password VARCHAR,
  full_name VARCHAR,
  tier VARCHAR (free/pro),
  monthly_uploads_used INT,
  created_at TIMESTAMP
)

-- Jobs table
jobs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  status VARCHAR (pending/processing/completed/failed),
  file_url VARCHAR,
  file_name VARCHAR,
  file_size_bytes INT,
  transcription TEXT,
  blog_post JSONB,
  outline JSONB,
  social_posts JSONB,
  error_message TEXT,
  processing_time_seconds FLOAT,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
)
```

## 💰 Monetization Plan

### Tier Structure

| Feature | Free Tier | Pro Tier |
|---------|-----------|----------|
| **Price** | $0/month | $19/month |
| **Uploads** | 3/month | Unlimited |
| **File Size** | Up to 50MB | Up to 200MB |
| **Content Formats** | All 3 types | All 3 types + custom |
| **Priority Processing** | ❌ | ✅ |
| **API Access** | ❌ | ✅ |
| **Export Formats** | JSON only | JSON, PDF, DOCX |
| **Support** | Community | Email support |

### Stripe Integration

1. **Setup Stripe Products**:
   - Create product "AudioRepurpose Pro" at $19/month
   - Add webhook endpoint: `/api/v1/webhooks/stripe`

2. **Implementation**:
   ```python
   # Backend handles subscription creation
   POST /api/v1/billing/create-checkout-session

   # Stripe webhook updates user tier
   POST /api/v1/webhooks/stripe
   ```

3. **Usage Tracking**:
   - Middleware checks user tier before processing
   - Monthly counter resets automatically
   - Graceful degradation for expired subscriptions

### Revenue Projections

**Conservative Estimate** (12 months):
- Month 1-3: 50 free users, 5 pro ($95/mo)
- Month 4-6: 200 free users, 20 pro ($380/mo)
- Month 7-9: 500 free users, 50 pro ($950/mo)
- Month 10-12: 1000 free users, 100 pro ($1,900/mo)

**Operating Costs**:
- OpenAI API: ~$0.50-2 per upload (varies by audio length)
- Hosting (DigitalOcean/AWS): $50-150/month
- Storage (S3): $10-30/month

**Break-even**: ~15-20 Pro subscribers

## 📈 Marketing & User Acquisition Strategy

### Phase 1: Launch (Month 1-2) - Get First 100 Users

#### Target Audience
1. **Podcasters** (Primary)
   - Pain point: Spending hours repurposing content manually
   - Where they hang out: Podcast Movement Facebook groups, r/podcasting, Podcast Host forums

2. **Content Creators** (Secondary)
   - YouTubers who do interviews/commentary
   - LinkedIn content creators
   - Newsletter writers

3. **Marketers** (Tertiary)
   - Agency workers who handle client podcasts
   - B2B marketers doing thought leadership

#### Launch Strategy

**Pre-Launch (2 weeks before):**
```markdown
1. Build in Public
   - Post daily updates on Twitter/LinkedIn
   - Show: "Here's what our AI generated from Joe Rogan's podcast"
   - Use hashtags: #buildinpublic #indiehackers #AItools

2. Create Demo Video
   - 60-second screen recording showing full workflow
   - Upload sample audio → get results in 30 seconds
   - Post on Twitter, LinkedIn, Product Hunt teaser

3. Beta Tester Outreach (aim for 20)
   - Reach out to 50 podcasters with <10k followers
   - Message: "Free lifetime Pro account for feedback"
   - Ask them to post about it once
```

**Launch Week:**
```markdown
Day 1: Product Hunt Launch
- Post at 12:01 AM PST
- Title: "Turn your podcast into a blog post in 30 seconds"
- Ask beta testers to upvote/comment
- Goal: Top 10 of the day = 300-500 signups

Day 2-3: Reddit Strategy
- r/podcasting: "I built a tool to repurpose podcast content (feedback welcome)"
- r/SaaS: Show technical architecture
- r/entrepreneur: Focus on content marketing angle
- Don't spam - provide value, mention tool naturally

Day 4-5: Content Blitz
- Publish: "I analyzed 50 podcasts with AI - here's what I learned"
- Post on Medium, Dev.to, LinkedIn
- Include AudioRepurpose demo at end

Day 6-7: Community Engagement
- Comment on every mention
- Fix bugs fast
- Ship feature requests quickly
```

### Phase 2: Growth (Month 3-6) - Get to 500 Users

#### Content Marketing

**SEO-Optimized Blog Posts** (2 per week):
```
- "How to Repurpose Podcast Content [2025 Complete Guide]"
- "10 Ways to Turn One Podcast into 20 Pieces of Content"
- "Best AI Tools for Podcasters (Comparison)"
- "From Audio to Blog: Repurposing Strategy for Creators"
```

**Video Content**:
- YouTube tutorials: "Podcast to LinkedIn Posts in 1 Click"
- TikTok/Reels: Quick before/after demos
- Loom walkthroughs for onboarding emails

#### Partnership Strategy

**Podcast Hosting Platforms**:
- Reach out to Buzzsprout, Transistor, Captivate for integration
- Offer revenue share or affiliate deal
- Goal: Get listed in their "Tools" directory

**Communities**:
- Sponsor Indie Hackers newsletter ($500-1000 for 5k views)
- Join Podcast Movement online communities
- Partner with podcasting courses (affiliate deal)

**Influencer Outreach**:
- Find podcasters with 5k-50k followers
- Offer free Pro account + $50 for honest review
- Target: 10 reviews/month

### Phase 3: Scale (Month 7-12) - Get to 1000+ Users

#### Paid Acquisition (when profitable)

**Google Ads**:
```
Keywords (start with $10/day):
- "podcast transcription service"
- "repurpose podcast content"
- "audio to blog post"

Landing page variants:
A: For podcasters
B: For content marketers
C: For agencies
```

**LinkedIn Ads**:
- Target: Content Managers, Podcast Producers
- Budget: $15/day
- Ad type: Sponsored content with demo video

#### Referral Program

```
Give 1 month Pro free → Get 1 month Pro free
- Easy sharing: "Share your unique link"
- Track in database with referral_code field
- Automated email when someone signs up via your link
```

#### Case Studies

- Document 3-5 power users
- Show before/after workflow
- Include time saved, engagement metrics
- Post on website + share on social

### Metrics to Track

```python
# Week 1 Goals:
- 50 signups
- 20 audio uploads
- 5 social shares

# Month 1 Goals:
- 200 signups
- 100 active users (uploaded at least once)
- 10 paid conversions
- 20% activation rate

# Month 3 Goals:
- 500 signups
- 250 active users
- 50 paid conversions
- $950 MRR

# Key Metrics Dashboard:
- Signup → Upload conversion (target: 50%)
- Free → Pro conversion (target: 10% after trial)
- Churn rate (target: <5%/month)
- NPS score (target: >40)
```

### Guerrilla Marketing Tactics

**Free Value Bombs**:
1. "Repurpose This" Chrome Extension
   - Highlight text → generate social posts
   - Links back to AudioRepurpose for audio

2. Free Tools Page:
   - "Social Post Generator" (text-based, no signup)
   - "Podcast Title Generator"
   - All link to main product

3. Twitter Automation:
   - Bot that finds tweets: "spent 3 hours repurposing my podcast"
   - Auto-reply: "Hey! You might like AudioRepurpose - does this in 30 sec"
   - (Use sparingly, don't spam)

### Email Sequences

**Onboarding (5 emails over 7 days):**
1. Welcome + quick start guide
2. "Here's what others generated with AudioRepurpose" (social proof)
3. Tips: "How to optimize your audio for best results"
4. Case study: "From 3 hours to 3 minutes"
5. Upgrade offer: "Get unlimited uploads with Pro"

**Re-engagement (for inactive users):**
- Day 7: "Haven't uploaded yet? Here's what you're missing"
- Day 14: "Limited time: Free upload credits"
- Day 30: "We miss you - here's what's new"

## 🔧 How to Extend

### Add New Content Formats

1. Create prompt template in `backend/app/core/prompts.py`:
```python
EMAIL_NEWSLETTER_PROMPT = """
Generate an email newsletter from this transcription...
"""
```

2. Add generation logic in `backend/app/services/ai.py`:
```python
async def generate_newsletter(transcription: str) -> dict:
    # Call OpenAI with EMAIL_NEWSLETTER_PROMPT
    pass
```

3. Update task in `backend/app/tasks/process_audio.py` to include new format

### Add New AI Providers

Create provider abstraction in `backend/app/services/ai.py`:
```python
class AIProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        pass

    @abstractmethod
    async def generate_content(self, prompt: str, context: str) -> str:
        pass

class OpenAIProvider(AIProvider):
    # Current implementation
    pass

class AnthropicProvider(AIProvider):
    # Add Claude integration
    pass
```

### Add Webhook Notifications

1. Add webhook URL field to user model
2. Update `backend/app/tasks/process_audio.py` to send POST request on completion:
```python
if user.webhook_url:
    await send_webhook(user.webhook_url, job_data)
```

### Add PDF/DOCX Export

Install dependencies:
```bash
pip install python-docx reportlab
```

Create export service in `backend/app/services/export.py`:
```python
async def export_to_docx(job_data: dict) -> bytes:
    # Generate DOCX file
    pass
```

Add endpoint in `backend/app/api/routes/jobs.py`:
```python
@router.get("/{job_id}/export/{format}")
async def export_job(job_id: UUID, format: str):
    # Return file download
    pass
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 🚀 Deployment

### Docker Compose (VPS)

```bash
# On DigitalOcean/AWS/Hetzner
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes (Optional)

See `k8s/` directory for manifests.

### Environment Variables

See `.env.example` for all required variables.

## 📝 License

MIT License - feel free to use this for your portfolio or commercial projects.

## 🤝 Contributing

This is a portfolio project template. Feel free to fork and customize for your needs!

## 📧 Support

- Documentation: This README
- Issues: GitHub Issues
- Email: support@yoursite.com (for production)

---

Built with ❤️ by [Your Name] | [Portfolio](https://yoursite.com) | [LinkedIn](https://linkedin.com/in/yourname)
