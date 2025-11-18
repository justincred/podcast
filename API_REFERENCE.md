# AudioRepurpose API Reference

Complete REST API documentation for the AudioRepurpose backend.

## Base URL

```
Development: http://localhost:8000
Production:  https://your-domain.com
```

## Authentication

All authenticated endpoints require a JWT bearer token in the Authorization header.

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Obtaining a Token

1. Register a new user or login
2. Extract `access_token` from response
3. Include in subsequent requests

Token expiration: **7 days** (configurable)

---

## Endpoints

### Authentication

#### Register User

Create a new user account.

```http
POST /api/v1/auth/register
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "full_name": "John Doe"  // optional
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
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

**Error Responses:**

| Status | Description |
|--------|-------------|
| 400 | Email already registered |
| 422 | Validation error (invalid email, short password) |

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

---

#### Login

Authenticate with email and password.

```http
POST /api/v1/auth/login
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "tier": "free",
    "monthly_uploads_used": 1,
    "uploads_remaining": 2,
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 401 | Incorrect email or password |

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

---

#### Get Current User

Retrieve authenticated user's information.

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "tier": "free",
  "monthly_uploads_used": 1,
  "uploads_remaining": 2,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 401 | Invalid or missing token |
| 404 | User not found |

**Example:**
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### Audio Processing

#### Upload Audio

Upload an audio file for processing.

```http
POST /api/v1/audio/process
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file` (required): Audio file (MP3, WAV, M4A, OGG, FLAC)
- `title` (optional): Title for the content

**File Constraints:**
- **Free tier**: Max 50MB
- **Pro tier**: Max 200MB
- **Allowed formats**: mp3, wav, m4a, ogg, flac

**Response (202 Accepted):**
```json
{
  "job_id": "650e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "progress": 0,
  "file_name": "podcast-episode-42.mp3",
  "title": "Episode 42: Building SaaS",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 400 | Invalid file type or format |
| 401 | Unauthorized (missing/invalid token) |
| 413 | File too large for tier |
| 429 | Monthly upload quota exceeded |

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/audio/process \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@podcast.mp3" \
  -F "title=My Podcast Episode"
```

---

### Jobs

#### Get Job by ID

Retrieve job status and results.

```http
GET /api/v1/jobs/{job_id}
Authorization: Bearer <token>
```

**Path Parameters:**
- `job_id`: UUID of the job

**Response (200 OK) - Pending/Processing:**
```json
{
  "job_id": "650e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "file_name": "podcast-episode-42.mp3",
  "title": "Episode 42: Building SaaS",
  "result": null,
  "error_message": null,
  "processing_time_seconds": null,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": null
}
```

**Response (200 OK) - Completed:**
```json
{
  "job_id": "650e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "file_name": "podcast-episode-42.mp3",
  "title": "Episode 42: Building SaaS",
  "result": {
    "transcription": "Welcome to episode 42 where we discuss...",
    "blog_post": {
      "title": "Building a Successful SaaS Product",
      "meta_description": "Learn the key strategies for building a SaaS product...",
      "introduction": "Starting a SaaS business can be challenging...",
      "body_sections": [
        {
          "heading": "Finding Product-Market Fit",
          "content": "The first step in building a SaaS product..."
        },
        {
          "heading": "Pricing Strategy",
          "content": "Choosing the right pricing model is crucial..."
        }
      ],
      "conclusion": "Building a SaaS product requires patience...",
      "keywords": ["saas", "product development", "startup"],
      "word_count": 1243
    },
    "outline": {
      "title": "Building a Successful SaaS Product",
      "overview": "This episode covers strategies for building and scaling SaaS products",
      "sections": [
        {
          "topic": "Finding Product-Market Fit",
          "timestamp": "00:05:23",
          "key_points": [
            "Talk to potential customers early",
            "Iterate based on feedback",
            "Focus on solving real problems"
          ],
          "notable_quote": "Product-market fit is when customers pull the product from you"
        },
        {
          "topic": "Pricing Strategy",
          "timestamp": "00:12:45",
          "key_points": [
            "Start with value-based pricing",
            "Consider freemium model",
            "Don't undervalue your product"
          ]
        }
      ],
      "action_items": [
        "Research competitor pricing",
        "Interview 10 potential customers",
        "Create landing page to validate demand"
      ],
      "resources_mentioned": [
        "The Lean Startup by Eric Ries",
        "https://stripe.com/atlas"
      ]
    },
    "social_posts": [
      {
        "platform": "linkedin",
        "type": "insight",
        "content": "🚀 Building a SaaS product? Here's the #1 mistake founders make:\n\nThey build in isolation without talking to customers.\n\nProduct-market fit happens when customers are pulling the product from you, not when you're pushing it to them.\n\nStart with conversations, not code.",
        "hashtags": ["#SaaS", "#ProductDevelopment", "#Startups"],
        "notes": "Post during business hours for max engagement"
      },
      {
        "platform": "twitter",
        "type": "quote",
        "content": "\"Product-market fit is when customers pull the product from you\" 💡\n\nThis changes everything about how you approach building.",
        "hashtags": ["#SaaS", "#Startups"],
        "notes": "Thread-starter style"
      },
      {
        "platform": "linkedin",
        "type": "listicle",
        "content": "3 keys to SaaS pricing strategy:\n\n1️⃣ Start with value-based pricing\n2️⃣ Consider a freemium tier for growth\n3️⃣ Don't undervalue your product\n\nPricing is part of your positioning. Choose wisely.",
        "hashtags": ["#SaaS", "#Pricing", "#Business"]
      }
    ]
  },
  "error_message": null,
  "processing_time_seconds": 47.3,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:31:00Z"
}
```

**Response (200 OK) - Failed:**
```json
{
  "job_id": "650e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "progress": 40,
  "file_name": "podcast-episode-42.mp3",
  "result": null,
  "error_message": "Transcription failed: Audio file appears to be corrupted",
  "processing_time_seconds": 12.5,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:15Z"
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 401 | Unauthorized |
| 403 | Job belongs to another user |
| 404 | Job not found |

**Example:**
```bash
curl http://localhost:8000/api/v1/jobs/650e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

#### List User Jobs

Get paginated list of user's jobs.

```http
GET /api/v1/jobs?limit=10&offset=0
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (optional): Number of jobs to return (1-100, default: 10)
- `offset` (optional): Number of jobs to skip (default: 0)

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "job_id": "650e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "progress": 100,
      "file_name": "podcast-episode-42.mp3",
      "title": "Episode 42",
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:31:00Z"
    },
    {
      "job_id": "750e8400-e29b-41d4-a716-446655440001",
      "status": "processing",
      "progress": 60,
      "file_name": "podcast-episode-41.mp3",
      "title": "Episode 41",
      "created_at": "2024-01-14T15:20:00Z",
      "completed_at": null
    }
  ],
  "total": 25,
  "limit": 10,
  "offset": 0
}
```

**Pagination Example:**
```bash
# First page (jobs 1-10)
curl "http://localhost:8000/api/v1/jobs?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Second page (jobs 11-20)
curl "http://localhost:8000/api/v1/jobs?limit=10&offset=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

#### Delete Job

Delete a job and its results.

```http
DELETE /api/v1/jobs/{job_id}
Authorization: Bearer <token>
```

**Path Parameters:**
- `job_id`: UUID of the job

**Response (204 No Content):**
No response body.

**Error Responses:**

| Status | Description |
|--------|-------------|
| 401 | Unauthorized |
| 403 | Job belongs to another user |
| 404 | Job not found |

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/jobs/650e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### Health Check

#### Get API Health

Check if API is running.

```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "audiorepurpose-backend"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

## Data Models

### User

```typescript
{
  id: string;                    // UUID
  email: string;                 // Unique email address
  full_name: string | null;      // Optional full name
  tier: "free" | "pro";          // Subscription tier
  monthly_uploads_used: number;  // Current month's upload count
  uploads_remaining: number;     // Remaining uploads this month
  created_at: string;            // ISO 8601 datetime
}
```

### Job

```typescript
{
  job_id: string;                      // UUID
  status: JobStatus;                   // See JobStatus below
  progress: number;                    // 0-100
  file_name: string;                   // Original filename
  title?: string;                      // Optional title
  result?: JobResult;                  // Present when completed
  error_message?: string;              // Present when failed
  processing_time_seconds?: number;    // Processing duration
  created_at: string;                  // ISO 8601 datetime
  completed_at?: string;               // ISO 8601 datetime
}
```

### JobStatus

```typescript
type JobStatus =
  | "pending"      // Waiting to be processed
  | "processing"   // Currently being processed
  | "completed"    // Successfully completed
  | "failed";      // Failed with error
```

### JobResult

```typescript
{
  transcription?: string;        // Full audio transcription
  blog_post?: BlogPost;          // Generated blog post
  outline?: Outline;             // Structured outline
  social_posts?: SocialPost[];   // Social media posts
}
```

### BlogPost

```typescript
{
  title: string;                          // Blog post title
  meta_description?: string;              // SEO description
  introduction: string;                   // Opening paragraph(s)
  body_sections: BodySection[];           // Main content sections
  conclusion: string;                     // Closing paragraph(s)
  keywords: string[];                     // SEO keywords
  word_count: number;                     // Total word count
}

interface BodySection {
  heading: string;    // Section heading (H2)
  content: string;    // Section content (paragraphs)
}
```

### Outline

```typescript
{
  title: string;                        // Outline title
  overview: string;                     // Brief summary
  sections: OutlineSection[];           // Main sections
  action_items: string[];               // Actionable takeaways
  resources_mentioned: string[];        // Books, links, etc.
}

interface OutlineSection {
  topic: string;              // Section topic
  timestamp?: string;         // Time in audio (HH:MM:SS)
  key_points: string[];       // Bullet points
  notable_quote?: string;     // Memorable quote
}
```

### SocialPost

```typescript
{
  platform: string;     // "linkedin" | "twitter" | "instagram"
  type: string;         // "insight" | "quote" | "question" | "listicle" | "teaser"
  content: string;      // Post text
  hashtags: string[];   // Hashtag suggestions
  notes?: string;       // Optional posting tips
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted, processing async |
| 204 | No Content | Successful with no response body |
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 413 | Payload Too Large | File size exceeds limit |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit or quota exceeded |
| 500 | Internal Server Error | Server error |

---

## Rate Limits

Current rate limits (configurable):

- **Per minute**: 10 requests
- **Per hour**: 100 requests

Rate limit headers (future implementation):
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1640995200
```

---

## Usage Quotas

### Free Tier
- **Monthly uploads**: 3
- **Max file size**: 50MB
- **Resets**: 1st of each month at 00:00 UTC

### Pro Tier ($19/month)
- **Monthly uploads**: Unlimited
- **Max file size**: 200MB
- **Priority queue**: Jobs processed faster

---

## Webhooks (Future)

Users can set a webhook URL to receive notifications when jobs complete.

**Webhook Payload:**
```json
{
  "event": "job.completed",
  "job_id": "650e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:31:00Z",
  "processing_time_seconds": 47.3
}
```

**Headers:**
```http
POST https://your-webhook-url.com/webhook
Content-Type: application/json
X-AudioRepurpose-Signature: sha256=...
```

---

## Code Examples

### JavaScript/TypeScript

```typescript
// Using fetch API
const API_URL = 'http://localhost:8000/api/v1';
let token: string | null = null;

// Register
async function register(email: string, password: string) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  token = data.access_token;
  return data;
}

// Upload audio
async function uploadAudio(file: File, title?: string) {
  const formData = new FormData();
  formData.append('file', file);
  if (title) formData.append('title', title);

  const response = await fetch(`${API_URL}/audio/process`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData,
  });
  return await response.json();
}

// Get job
async function getJob(jobId: string) {
  const response = await fetch(`${API_URL}/jobs/${jobId}`, {
    headers: { 'Authorization': `Bearer ${token}` },
  });
  return await response.json();
}

// Poll job until complete
async function pollJob(jobId: string, onProgress: (job: any) => void) {
  while (true) {
    const job = await getJob(jobId);
    onProgress(job);

    if (job.status === 'completed' || job.status === 'failed') {
      return job;
    }

    await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2s
  }
}
```

### Python

```python
import requests
import time

API_URL = 'http://localhost:8000/api/v1'
token = None

# Register
def register(email: str, password: str):
    global token
    response = requests.post(f'{API_URL}/auth/register', json={
        'email': email,
        'password': password,
    })
    data = response.json()
    token = data['access_token']
    return data

# Upload audio
def upload_audio(file_path: str, title: str = None):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'title': title} if title else {}
        response = requests.post(
            f'{API_URL}/audio/process',
            headers={'Authorization': f'Bearer {token}'},
            files=files,
            data=data,
        )
    return response.json()

# Get job
def get_job(job_id: str):
    response = requests.get(
        f'{API_URL}/jobs/{job_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    return response.json()

# Poll job until complete
def poll_job(job_id: str, on_progress=None):
    while True:
        job = get_job(job_id)
        if on_progress:
            on_progress(job)

        if job['status'] in ['completed', 'failed']:
            return job

        time.sleep(2)  # Wait 2 seconds
```

### cURL

```bash
# Set variables
API_URL="http://localhost:8000/api/v1"
EMAIL="test@example.com"
PASSWORD="testpass123"

# Register
curl -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" \
  | jq '.access_token' > token.txt

# Set token
TOKEN=$(cat token.txt | tr -d '"')

# Upload audio
JOB_ID=$(curl -X POST "$API_URL/audio/process" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@podcast.mp3" \
  -F "title=My Podcast" \
  | jq -r '.job_id')

# Check status
curl "$API_URL/jobs/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.status'

# Get results when complete
curl "$API_URL/jobs/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.result'
```

---

## Best Practices

### 1. Token Management

```typescript
// Store token securely
localStorage.setItem('auth_token', token);

// Include in all requests
const headers = {
  'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
};

// Handle 401 errors (token expired)
if (response.status === 401) {
  localStorage.removeItem('auth_token');
  redirectToLogin();
}
```

### 2. Error Handling

```typescript
async function apiRequest(url: string, options: RequestInit) {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

### 3. Polling

```typescript
// Use exponential backoff for polling
async function pollWithBackoff(jobId: string) {
  let delay = 1000; // Start with 1 second
  const maxDelay = 10000; // Max 10 seconds

  while (true) {
    const job = await getJob(jobId);

    if (job.status === 'completed' || job.status === 'failed') {
      return job;
    }

    await sleep(delay);
    delay = Math.min(delay * 1.5, maxDelay); // Increase delay
  }
}
```

### 4. File Validation

```typescript
// Validate before upload
function validateAudioFile(file: File, userTier: 'free' | 'pro'): string | null {
  const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/x-m4a', 'audio/ogg'];
  const maxSize = userTier === 'pro' ? 200 * 1024 * 1024 : 50 * 1024 * 1024;

  if (!allowedTypes.includes(file.type)) {
    return 'Invalid file type. Please upload MP3, WAV, M4A, or OGG.';
  }

  if (file.size > maxSize) {
    return `File too large. Maximum size: ${maxSize / 1024 / 1024}MB`;
  }

  return null; // Valid
}
```

---

## Interactive API Documentation

Visit the Swagger UI for interactive API testing:

```
http://localhost:8000/docs
```

Features:
- Try all endpoints directly in browser
- See request/response schemas
- Generate code examples
- View authentication requirements

---

## Support

- **Main Documentation**: [README.md](README.md)
- **Backend Guide**: [backend/README.md](backend/README.md)
- **Frontend Guide**: [frontend/README.md](frontend/README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

**API Version**: 1.0
**Last Updated**: January 2025
