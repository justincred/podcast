/**
 * TypeScript type definitions for AudioRepurpose.
 */

// =============================================================================
// User Types
// =============================================================================

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

export interface AuthResponse {
  user: User;
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
}

// =============================================================================
// Job Types
// =============================================================================

export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface BlogPost {
  title: string;
  meta_description?: string;
  introduction: string;
  body_sections: Array<{
    heading: string;
    content: string;
  }>;
  conclusion: string;
  keywords: string[];
  word_count: number;
}

export interface OutlineSection {
  topic: string;
  timestamp?: string;
  key_points: string[];
  notable_quote?: string;
}

export interface Outline {
  title: string;
  overview: string;
  sections: OutlineSection[];
  action_items: string[];
  resources_mentioned: string[];
}

export interface SocialPost {
  platform: string;
  type: string;
  content: string;
  hashtags: string[];
  notes?: string;
}

export interface JobResult {
  transcription?: string;
  blog_post?: BlogPost;
  outline?: Outline;
  social_posts?: SocialPost[];
}

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

export interface JobListResponse {
  jobs: Job[];
  total: number;
  limit: number;
  offset: number;
}

// =============================================================================
// API Error Type
// =============================================================================

export interface APIError {
  detail: string;
  status?: number;
}
