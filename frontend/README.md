# AudioRepurpose Frontend Documentation

Complete documentation for the Next.js 14 frontend application.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Setup & Installation](#setup--installation)
4. [Routing](#routing)
5. [Components](#components)
6. [State Management](#state-management)
7. [API Integration](#api-integration)
8. [Styling](#styling)
9. [TypeScript Types](#typescript-types)
10. [Development Workflow](#development-workflow)
11. [Testing](#testing)
12. [Deployment](#deployment)
13. [Common Tasks](#common-tasks)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js 14 App                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │         App Router (src/app/)                    │  │
│  │  - Server Components (default)                   │  │
│  │  - Client Components ('use client')              │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                                          │
│  ┌────────────▼─────────────────────────────────────┐  │
│  │         React Components (src/components/)       │  │
│  │  - Reusable UI components                        │  │
│  │  - Form components                               │  │
│  │  - Display components                            │  │
│  └────────────┬─────────────────────────────────────┘  │
│               │                                          │
│  ┌────────────▼─────────────────────────────────────┐  │
│  │         API Client (src/lib/api.ts)              │  │
│  │  - HTTP requests to backend                      │  │
│  │  - Authentication management                     │  │
│  │  - Error handling                                │  │
│  └────────────┬─────────────────────────────────────┘  │
└───────────────┼──────────────────────────────────────────┘
                │
         ┌──────▼──────┐
         │   Backend   │
         │  FastAPI    │
         └─────────────┘
```

### Technology Stack

- **Next.js 14**: React framework with App Router
- **React 18.2**: UI library with Server Components
- **TypeScript 5.3**: Type-safe JavaScript
- **Tailwind CSS 3.3**: Utility-first CSS
- **Axios 1.6**: HTTP client
- **Lucide React**: Icon library
- **React Hook Form 7.48**: Form management
- **date-fns**: Date formatting

---

## Project Structure

```
frontend/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── (auth)/                 # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx        # Login page
│   │   │   └── register/
│   │   │       └── page.tsx        # Registration page
│   │   ├── dashboard/
│   │   │   └── page.tsx            # Dashboard (authenticated)
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Home/landing page
│   │   └── globals.css             # Global styles
│   │
│   ├── components/                 # Reusable components
│   │   ├── UploadForm.tsx          # Audio upload form
│   │   ├── JobCard.tsx             # Job list item
│   │   └── JobResults.tsx          # Results viewer
│   │
│   ├── lib/                        # Utility libraries
│   │   ├── api.ts                  # Backend API client
│   │   └── utils.ts                # Helper functions
│   │
│   └── types/                      # TypeScript types
│       └── index.ts                # Type definitions
│
├── public/                         # Static assets
│   ├── favicon.ico
│   └── logo.png                    # (Add your logo)
│
├── package.json                    # Dependencies
├── tsconfig.json                   # TypeScript config
├── tailwind.config.js              # Tailwind config
├── next.config.js                  # Next.js config
├── postcss.config.js               # PostCSS config
├── Dockerfile                      # Container definition
└── README.md                       # This file
```

---

## Setup & Installation

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running (see `backend/README.md`)

### Local Development

```bash
# 1. Install dependencies
npm install

# 2. Set up environment variables
# Create .env.local (or use existing .env)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 3. Start development server
npm run dev

# 4. Open browser
open http://localhost:3000
```

### Available Scripts

```bash
npm run dev          # Start development server (with hot reload)
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler check
```

### Docker Setup

```bash
# Build image
docker build -t audiorepurpose-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  audiorepurpose-frontend
```

---

## Routing

Next.js 14 uses the **App Router** (file-system based routing).

### Route Structure

```
/                          → app/page.tsx (Landing page)
/login                     → app/(auth)/login/page.tsx
/register                  → app/(auth)/register/page.tsx
/dashboard                 → app/dashboard/page.tsx
```

### Route Groups

`(auth)` is a **route group** - the folder name doesn't appear in the URL:
- `app/(auth)/login/page.tsx` → `/login` (not `/auth/login`)

### Navigation

```tsx
import Link from 'next/link';

// Declarative navigation
<Link href="/dashboard">Go to Dashboard</Link>

// Programmatic navigation
'use client'
import { useRouter } from 'next/navigation';

const router = useRouter();
router.push('/dashboard');
router.back();
```

### Layouts

**Root Layout** (`app/layout.tsx`):
- Wraps all pages
- Sets up fonts, metadata
- Provides global context

```tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Server vs Client Components

**Server Components** (default):
- Run on server
- Can fetch data directly
- Smaller bundle size
- Cannot use hooks like `useState`, `useEffect`

**Client Components** (with `'use client'`):
- Run in browser
- Can use React hooks
- Interactive features
- Access to browser APIs

```tsx
// Server Component (default)
export default function Page() {
  return <div>Static content</div>;
}

// Client Component
'use client';
import { useState } from 'react';

export default function Page() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## Components

### Component Philosophy

- **Reusable**: Components should be generic enough for reuse
- **Single Responsibility**: Each component does one thing well
- **Typed**: All props have TypeScript interfaces
- **Documented**: Complex logic has inline comments

### Core Components

#### UploadForm (`src/components/UploadForm.tsx`)

Handles audio file uploads.

**Props:**
```tsx
interface UploadFormProps {
  onUpload: (file: File, title?: string) => Promise<void>;
  user: User | null;
}
```

**Features:**
- Drag-and-drop support
- File validation (type, size)
- Tier-based size limits
- Quota checking
- Loading states

**Usage:**
```tsx
<UploadForm
  onUpload={async (file, title) => {
    const job = await uploadAudio(file, title);
    console.log('Job created:', job.job_id);
  }}
  user={currentUser}
/>
```

#### JobCard (`src/components/JobCard.tsx`)

Displays a job in the list.

**Props:**
```tsx
interface JobCardProps {
  job: Job;
  isSelected: boolean;
  onClick: () => void;
}
```

**Features:**
- Status indicator with icons
- Progress bar for processing jobs
- Relative timestamps
- Clickable to select

**Usage:**
```tsx
<JobCard
  job={job}
  isSelected={selectedJob?.job_id === job.job_id}
  onClick={() => setSelectedJob(job)}
/>
```

#### JobResults (`src/components/JobResults.tsx`)

Displays job results with tabs.

**Props:**
```tsx
interface JobResultsProps {
  job: Job;
}
```

**Features:**
- Tab navigation (Blog, Outline, Social, Transcription)
- Copy to clipboard
- Download as text
- Loading/error states
- Formatted display for each content type

**Usage:**
```tsx
<JobResults job={completedJob} />
```

### Creating a New Component

```tsx
// src/components/MyComponent.tsx
'use client';

import { useState } from 'react';

interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export default function MyComponent({ title, onAction }: MyComponentProps) {
  const [isActive, setIsActive] = useState(false);

  return (
    <div className="p-4 bg-white rounded-lg">
      <h2 className="text-xl font-bold">{title}</h2>
      <button
        onClick={() => {
          setIsActive(!isActive);
          onAction?.();
        }}
        className="mt-2 px-4 py-2 bg-primary-600 text-white rounded"
      >
        {isActive ? 'Active' : 'Inactive'}
      </button>
    </div>
  );
}
```

---

## State Management

### Local State (useState)

For component-specific state:

```tsx
'use client';
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### Lifting State Up

Share state between components by lifting it to a common parent:

```tsx
export default function Parent() {
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  return (
    <>
      <JobList onSelect={setSelectedJob} />
      <JobDetails job={selectedJob} />
    </>
  );
}
```

### URL State (useSearchParams)

Store state in URL query parameters:

```tsx
'use client';
import { useSearchParams, useRouter } from 'next/navigation';

export default function FilteredList() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const filter = searchParams.get('filter') || 'all';

  const setFilter = (newFilter: string) => {
    router.push(`?filter=${newFilter}`);
  };

  return (
    <select value={filter} onChange={(e) => setFilter(e.target.value)}>
      <option value="all">All</option>
      <option value="completed">Completed</option>
    </select>
  );
}
```

### Local Storage

Persist state across sessions:

```tsx
'use client';
import { useState, useEffect } from 'react';

export default function ThemeToggle() {
  const [theme, setTheme] = useState('light');

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('theme');
    if (saved) setTheme(saved);
  }, []);

  // Save to localStorage on change
  const updateTheme = (newTheme: string) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <button onClick={() => updateTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme}
    </button>
  );
}
```

### Future: Context API

For deeply nested components (not currently used, but here's how):

```tsx
// src/contexts/AuthContext.tsx
'use client';
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext<{
  user: User | null;
  setUser: (user: User | null) => void;
}>({ user: null, setUser: () => {} });

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

// Usage in components
function MyComponent() {
  const { user, setUser } = useAuth();
  // ...
}
```

---

## API Integration

### API Client (`src/lib/api.ts`)

Centralized API communication with the backend.

### Authentication

```tsx
import { login, register, logout, getCurrentUser } from '@/lib/api';

// Register
const { user, access_token } = await register({
  email: 'user@example.com',
  password: 'password123',
  full_name: 'John Doe'
});

// Login
const { user, access_token } = await login({
  email: 'user@example.com',
  password: 'password123'
});

// Get current user
const user = await getCurrentUser();

// Logout
logout(); // Clears token from localStorage
```

### Audio Upload

```tsx
import { uploadAudio } from '@/lib/api';

const file = new File(['...'], 'audio.mp3', { type: 'audio/mpeg' });
const job = await uploadAudio(file, 'My Podcast Title');

console.log('Job ID:', job.job_id);
console.log('Status:', job.status);
```

### Job Management

```tsx
import { getJob, listJobs, deleteJob, pollJobStatus } from '@/lib/api';

// Get single job
const job = await getJob('job-uuid');

// List jobs with pagination
const { jobs, total } = await listJobs(10, 0);

// Delete job
await deleteJob('job-uuid');

// Poll until completion
await pollJobStatus(
  'job-uuid',
  (updatedJob) => {
    console.log('Progress:', updatedJob.progress);
    setJob(updatedJob); // Update UI
  },
  2000 // Poll every 2 seconds
);
```

### Error Handling

```tsx
import { APIError } from '@/types';

try {
  await uploadAudio(file);
} catch (err) {
  const apiError = err as APIError;

  if (apiError.status === 401) {
    // Unauthorized - redirect to login
    router.push('/login');
  } else if (apiError.status === 429) {
    // Rate limited
    alert('Upload quota exceeded');
  } else {
    // Generic error
    alert(apiError.detail || 'An error occurred');
  }
}
```

### Adding New API Endpoints

```tsx
// In src/lib/api.ts

export async function myNewEndpoint(params: MyParams): Promise<MyResponse> {
  try {
    const response = await apiClient.post<MyResponse>('/my-endpoint', params);
    return response.data;
  } catch (error) {
    throw handleAPIError(error);
  }
}
```

---

## Styling

### Tailwind CSS

Utility-first CSS framework. Classes are applied directly to elements.

#### Common Patterns

**Layout:**
```tsx
<div className="flex items-center justify-between">
  <div className="w-1/2">Left</div>
  <div className="w-1/2">Right</div>
</div>
```

**Spacing:**
```tsx
<div className="p-4 m-2">       {/* padding: 1rem, margin: 0.5rem */}
<div className="px-6 py-3">     {/* padding-x: 1.5rem, padding-y: 0.75rem */}
<div className="mt-4 mb-6">     {/* margin-top: 1rem, margin-bottom: 1.5rem */}
```

**Colors:**
```tsx
<div className="bg-primary-600 text-white">  {/* Background + text color */}
<div className="border-gray-300">            {/* Border color */}
<div className="hover:bg-primary-700">       {/* Hover state */}
```

**Typography:**
```tsx
<h1 className="text-3xl font-bold">Title</h1>
<p className="text-sm text-gray-600">Small gray text</p>
```

**Responsive:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* 1 column on mobile, 2 on tablet, 3 on desktop */}
</div>
```

#### Customization

Edit `tailwind.config.js`:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7', // Your brand color
          700: '#0369a1',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

#### Utility Functions

Use `cn()` from `src/lib/utils.ts` for conditional classes:

```tsx
import { cn } from '@/lib/utils';

<button className={cn(
  'px-4 py-2 rounded',
  isActive ? 'bg-primary-600' : 'bg-gray-300',
  isDisabled && 'opacity-50 cursor-not-allowed'
)}>
  Button
</button>
```

### Global Styles

`src/app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles */
:root {
  --primary-color: #0284c7;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
```

---

## TypeScript Types

### Type Definitions (`src/types/index.ts`)

#### User Types

```tsx
export type UserTier = 'free' | 'pro';

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  tier: UserTier;
  monthly_uploads_used: number;
  uploads_remaining: number;
  created_at: string;
}
```

#### Job Types

```tsx
export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface Job {
  job_id: string;
  status: JobStatus;
  progress: number;
  file_name: string;
  title?: string;
  result?: JobResult;
  error_message?: string;
  processing_time_seconds?: number;
  created_at: string;
  completed_at?: string;
}
```

#### Using Types

```tsx
import { User, Job, JobStatus } from '@/types';

// Function parameters
function processJob(job: Job): void {
  console.log(job.status);
}

// Component props
interface MyComponentProps {
  user: User;
  onUpdate: (user: User) => void;
}

// State
const [job, setJob] = useState<Job | null>(null);
const [jobs, setJobs] = useState<Job[]>([]);
```

### Type Safety Best Practices

```tsx
// ✅ Good - Explicit types
const users: User[] = await fetchUsers();

// ❌ Avoid - Implicit any
const users = await fetchUsers(); // TypeScript doesn't know the type

// ✅ Good - Optional chaining
const title = job?.result?.blog_post?.title;

// ❌ Avoid - Manual null checks
const title = job && job.result && job.result.blog_post && job.result.blog_post.title;

// ✅ Good - Type guards
if (job.status === 'completed' && job.result) {
  console.log(job.result.transcription);
}
```

---

## Development Workflow

### Hot Reload

Next.js dev server automatically reloads on file changes:

```bash
npm run dev
# Edit any file → browser auto-refreshes
```

### TypeScript Checking

```bash
# Check types without running
npm run type-check

# Fix type errors before committing
```

### Linting

```bash
# Run ESLint
npm run lint

# Auto-fix issues
npm run lint -- --fix
```

### Environment Variables

**Public variables** (available in browser):
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Private variables** (server-side only):
```bash
SECRET_API_KEY=xxx  # Not accessible in browser
```

**Usage:**
```tsx
// Available in browser
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// Server components only
const secret = process.env.SECRET_API_KEY;
```

### Debugging

**Browser DevTools:**
```tsx
console.log('Debug:', variable);
console.table(arrayOfObjects);
debugger; // Pause execution
```

**React DevTools:**
- Install browser extension
- Inspect component tree
- View props and state

**Next.js DevTools:**
```bash
npm run dev
# Open http://localhost:3000
# Check terminal for errors and warnings
```

---

## Testing

### Setup

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom jest jest-environment-jsdom
```

### Example Test

```tsx
// __tests__/components/JobCard.test.tsx
import { render, screen } from '@testing-library/react';
import JobCard from '@/components/JobCard';

describe('JobCard', () => {
  it('renders job information', () => {
    const mockJob = {
      job_id: '123',
      status: 'completed',
      file_name: 'test.mp3',
      progress: 100,
      created_at: '2024-01-15T10:00:00Z',
    };

    render(
      <JobCard job={mockJob} isSelected={false} onClick={() => {}} />
    );

    expect(screen.getByText('test.mp3')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
  });
});
```

### Run Tests

```bash
npm test
npm test -- --coverage
```

---

## Deployment

### Build for Production

```bash
# Create optimized build
npm run build

# Test production build locally
npm run start
```

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deploy
vercel --prod
```

### Netlify

```bash
# netlify.toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Docker

```bash
# Build production image
docker build -t audiorepurpose-frontend .

# Run
docker run -p 3000:3000 audiorepurpose-frontend
```

### Environment Variables

Set in your deployment platform:
- Vercel: Project Settings → Environment Variables
- Netlify: Site Settings → Build & deploy → Environment
- Docker: Pass via `-e` flag or docker-compose

---

## Common Tasks

### Add a New Page

```bash
# Create file
touch src/app/my-page/page.tsx
```

```tsx
// src/app/my-page/page.tsx
export default function MyPage() {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold">My Page</h1>
    </div>
  );
}
```

Access at: `http://localhost:3000/my-page`

### Add a New Component

```tsx
// src/components/MyButton.tsx
interface MyButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export default function MyButton({ label, onClick, variant = 'primary' }: MyButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded ${
        variant === 'primary' ? 'bg-primary-600 text-white' : 'bg-gray-300'
      }`}
    >
      {label}
    </button>
  );
}

// Usage
import MyButton from '@/components/MyButton';

<MyButton label="Click me" onClick={() => alert('Clicked!')} />
```

### Change Brand Colors

Edit `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      primary: {
        500: '#3b82f6', // Change this
        600: '#2563eb', // And this
        700: '#1d4ed8', // And this
      },
    },
  },
}
```

### Add Custom Fonts

```tsx
// app/layout.tsx
import { Inter, Roboto } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });
const roboto = Roboto({ weight: '400', subsets: ['latin'] });

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

### Add Loading States

```tsx
'use client';
import { useState } from 'react';

export default function MyForm() {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      await submitData();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button disabled={isLoading} onClick={handleSubmit}>
      {isLoading ? 'Loading...' : 'Submit'}
    </button>
  );
}
```

### Form Validation

```tsx
'use client';
import { useState } from 'react';

export default function ContactForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!email.includes('@')) {
      setError('Invalid email');
      return;
    }

    // Submit
    console.log('Valid email:', email);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="border p-2 rounded"
      />
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **React Documentation**: https://react.dev
- **TypeScript Documentation**: https://www.typescriptlang.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Lucide Icons**: https://lucide.dev

## Need Help?

- Check main [README.md](../README.md)
- See [ARCHITECTURE.md](../ARCHITECTURE.md)
- Review [backend/README.md](../backend/README.md) for API details
- Check browser console for errors
- Use React DevTools for debugging

---

Built with ❤️ using Next.js 14, TypeScript, and Tailwind CSS
