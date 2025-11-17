'use client';

import { useState } from 'react';
import { Loader2, FileText, List, Share2, Copy, Download, CheckCircle } from 'lucide-react';
import { formatDuration, copyToClipboard, downloadTextFile } from '@/lib/utils';
import type { Job, BlogPost, Outline, SocialPost } from '@/types';

interface JobResultsProps {
  job: Job;
}

type Tab = 'blog' | 'outline' | 'social' | 'transcription';

export default function JobResults({ job }: JobResultsProps) {
  const [activeTab, setActiveTab] = useState<Tab>('blog');
  const [copiedItem, setCopiedItem] = useState<string | null>(null);

  const handleCopy = async (text: string, itemId: string) => {
    const success = await copyToClipboard(text);
    if (success) {
      setCopiedItem(itemId);
      setTimeout(() => setCopiedItem(null), 2000);
    }
  };

  const handleDownload = (content: string, filename: string) => {
    downloadTextFile(content, filename);
  };

  // Show loading state
  if (job.status === 'pending' || job.status === 'processing') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-12 text-center">
        <Loader2 className="h-16 w-16 text-primary-600 mx-auto mb-4 animate-spin" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Processing your audio...
        </h3>
        <p className="text-gray-500 mb-4">
          This usually takes 30-90 seconds depending on file length
        </p>
        <div className="max-w-xs mx-auto">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${job.progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-2">{job.progress}% complete</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (job.status === 'failed') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-12 text-center">
        <div className="text-red-500 mb-4">
          <svg className="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">Processing Failed</h3>
        <p className="text-gray-500 mb-4">{job.error_message || 'An error occurred'}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  // Show results
  const result = job.result;
  if (!result) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-12 text-center">
        <p className="text-gray-500">No results available</p>
      </div>
    );
  }

  const tabs = [
    { id: 'blog' as Tab, label: 'Blog Post', icon: FileText },
    { id: 'outline' as Tab, label: 'Outline', icon: List },
    { id: 'social' as Tab, label: 'Social Posts', icon: Share2 },
    { id: 'transcription' as Tab, label: 'Transcription', icon: FileText },
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900">
              {job.title || job.file_name}
            </h2>
            {job.processing_time_seconds && (
              <p className="text-sm text-gray-500 mt-1">
                Processed in {formatDuration(job.processing_time_seconds)}
              </p>
            )}
          </div>
          <CheckCircle className="h-8 w-8 text-green-500" />
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6" aria-label="Tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm
                  ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="h-5 w-5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'blog' && result.blog_post && (
          <BlogPostView blogPost={result.blog_post} onCopy={handleCopy} onDownload={handleDownload} copiedItem={copiedItem} />
        )}

        {activeTab === 'outline' && result.outline && (
          <OutlineView outline={result.outline} onCopy={handleCopy} onDownload={handleDownload} copiedItem={copiedItem} />
        )}

        {activeTab === 'social' && result.social_posts && (
          <SocialPostsView posts={result.social_posts} onCopy={handleCopy} copiedItem={copiedItem} />
        )}

        {activeTab === 'transcription' && result.transcription && (
          <TranscriptionView transcription={result.transcription} onCopy={handleCopy} onDownload={handleDownload} copiedItem={copiedItem} />
        )}
      </div>
    </div>
  );
}

// Blog Post View
function BlogPostView({ blogPost, onCopy, onDownload, copiedItem }: { blogPost: BlogPost; onCopy: (text: string, id: string) => void; onDownload: (content: string, filename: string) => void; copiedItem: string | null }) {
  const fullContent = `${blogPost.title}\n\n${blogPost.introduction}\n\n${blogPost.body_sections.map(s => `## ${s.heading}\n\n${s.content}`).join('\n\n')}\n\n${blogPost.conclusion}`;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-500">
          {blogPost.word_count} words • {blogPost.keywords?.join(', ')}
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onCopy(fullContent, 'blog')}
            className="flex items-center px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
          >
            {copiedItem === 'blog' ? <CheckCircle className="h-4 w-4 mr-2" /> : <Copy className="h-4 w-4 mr-2" />}
            {copiedItem === 'blog' ? 'Copied!' : 'Copy'}
          </button>
          <button
            onClick={() => onDownload(fullContent, `${blogPost.title}.txt`)}
            className="flex items-center px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <Download className="h-4 w-4 mr-2" />
            Download
          </button>
        </div>
      </div>

      <div className="prose max-w-none">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{blogPost.title}</h1>
        {blogPost.meta_description && (
          <p className="text-gray-600 italic mb-6">{blogPost.meta_description}</p>
        )}
        <div className="text-gray-700 leading-relaxed">
          <p className="mb-6">{blogPost.introduction}</p>
          {blogPost.body_sections.map((section, idx) => (
            <div key={idx} className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-3">{section.heading}</h2>
              <p>{section.content}</p>
            </div>
          ))}
          <p className="mb-6">{blogPost.conclusion}</p>
        </div>
      </div>
    </div>
  );
}

// Outline View
function OutlineView({ outline, onCopy, onDownload, copiedItem }: { outline: Outline; onCopy: (text: string, id: string) => void; onDownload: (content: string, filename: string) => void; copiedItem: string | null }) {
  const fullContent = `${outline.title}\n\n${outline.overview}\n\n${outline.sections.map(s => `## ${s.topic}${s.timestamp ? ` [${s.timestamp}]` : ''}\n${s.key_points.map(p => `- ${p}`).join('\n')}`).join('\n\n')}`;

  return (
    <div className="space-y-6">
      <div className="flex justify-end space-x-2">
        <button
          onClick={() => onCopy(fullContent, 'outline')}
          className="flex items-center px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
        >
          {copiedItem === 'outline' ? <CheckCircle className="h-4 w-4 mr-2" /> : <Copy className="h-4 w-4 mr-2" />}
          {copiedItem === 'outline' ? 'Copied!' : 'Copy'}
        </button>
        <button
          onClick={() => onDownload(fullContent, 'outline.txt')}
          className="flex items-center px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <Download className="h-4 w-4 mr-2" />
          Download
        </button>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">{outline.title}</h2>
        <p className="text-gray-600 mb-6">{outline.overview}</p>

        <div className="space-y-6">
          {outline.sections.map((section, idx) => (
            <div key={idx} className="border-l-4 border-primary-500 pl-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {section.topic}
                {section.timestamp && (
                  <span className="ml-2 text-sm text-gray-500">[{section.timestamp}]</span>
                )}
              </h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {section.key_points.map((point, pidx) => (
                  <li key={pidx}>{point}</li>
                ))}
              </ul>
              {section.notable_quote && (
                <blockquote className="mt-2 italic text-gray-600 border-l-2 border-gray-300 pl-4">
                  "{section.notable_quote}"
                </blockquote>
              )}
            </div>
          ))}
        </div>

        {outline.action_items && outline.action_items.length > 0 && (
          <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-2">Action Items</h4>
            <ul className="list-disc list-inside space-y-1 text-gray-700">
              {outline.action_items.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

// Social Posts View
function SocialPostsView({ posts, onCopy, copiedItem }: { posts: SocialPost[]; onCopy: (text: string, id: string) => void; copiedItem: string | null }) {
  return (
    <div className="space-y-4">
      {posts.map((post, idx) => (
        <div key={idx} className="border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="px-2 py-1 text-xs font-semibold bg-primary-100 text-primary-700 rounded">
                {post.platform.toUpperCase()}
              </span>
              <span className="text-xs text-gray-500">{post.type}</span>
            </div>
            <button
              onClick={() => onCopy(post.content + '\n\n' + post.hashtags.join(' '), `social-${idx}`)}
              className="flex items-center px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
            >
              {copiedItem === `social-${idx}` ? <CheckCircle className="h-3 w-3 mr-1" /> : <Copy className="h-3 w-3 mr-1" />}
              {copiedItem === `social-${idx}` ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <p className="text-gray-800 mb-3 whitespace-pre-wrap">{post.content}</p>
          {post.hashtags && post.hashtags.length > 0 && (
            <p className="text-primary-600 text-sm">
              {post.hashtags.join(' ')}
            </p>
          )}
          {post.notes && (
            <p className="text-xs text-gray-500 mt-2 italic">{post.notes}</p>
          )}
        </div>
      ))}
    </div>
  );
}

// Transcription View
function TranscriptionView({ transcription, onCopy, onDownload, copiedItem }: { transcription: string; onCopy: (text: string, id: string) => void; onDownload: (content: string, filename: string) => void; copiedItem: string | null }) {
  return (
    <div className="space-y-4">
      <div className="flex justify-end space-x-2">
        <button
          onClick={() => onCopy(transcription, 'transcription')}
          className="flex items-center px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
        >
          {copiedItem === 'transcription' ? <CheckCircle className="h-4 w-4 mr-2" /> : <Copy className="h-4 w-4 mr-2" />}
          {copiedItem === 'transcription' ? 'Copied!' : 'Copy'}
        </button>
        <button
          onClick={() => onDownload(transcription, 'transcription.txt')}
          className="flex items-center px-3 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <Download className="h-4 w-4 mr-2" />
          Download
        </button>
      </div>
      <div className="p-4 bg-gray-50 rounded-lg">
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{transcription}</p>
      </div>
    </div>
  );
}
