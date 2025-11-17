'use client';

import Link from 'next/link';
import { FileAudio, FileText, Share2, Zap } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <FileAudio className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-2xl font-bold text-gray-900">
                AudioRepurpose
              </span>
            </div>
            <div className="flex space-x-4">
              <Link
                href="/login"
                className="px-4 py-2 text-gray-700 hover:text-gray-900"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                Get Started Free
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
            Transform Your Audio into
            <span className="text-primary-600"> Written Content</span>
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Upload your podcast, interview, or meeting recording. Get AI-generated
            blog posts, outlines, and social media content in minutes.
          </p>
          <div className="mt-10">
            <Link
              href="/register"
              className="inline-flex items-center px-8 py-4 text-lg font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 shadow-lg"
            >
              <Zap className="mr-2 h-5 w-5" />
              Start Repurposing Free
            </Link>
            <p className="mt-4 text-sm text-gray-500">
              3 free uploads per month. No credit card required.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white p-8 rounded-xl shadow-md">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mb-4">
              <FileAudio className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Upload Audio
            </h3>
            <p className="text-gray-600">
              Support for MP3, WAV, M4A, OGG, and FLAC files up to 50MB
              (200MB for Pro users).
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-8 rounded-xl shadow-md">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mb-4">
              <FileText className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Generate Blog Posts
            </h3>
            <p className="text-gray-600">
              AI-powered blog posts with proper structure, SEO optimization,
              and 800-1500 words.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-8 rounded-xl shadow-md">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mb-4">
              <Share2 className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Social Media Posts
            </h3>
            <p className="text-gray-600">
              Get 5-10 ready-to-post social media updates optimized for
              LinkedIn, Twitter, and more.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="bg-primary-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">1</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Upload Audio</h3>
            <p className="text-sm text-gray-600">
              Upload your podcast or audio file
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">2</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI Transcribes</h3>
            <p className="text-sm text-gray-600">
              OpenAI Whisper transcribes your audio
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">3</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Generate Content</h3>
            <p className="text-sm text-gray-600">
              GPT-4 creates blog posts and social content
            </p>
          </div>

          <div className="text-center">
            <div className="bg-primary-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">4</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Download & Share</h3>
            <p className="text-sm text-gray-600">
              Copy, edit, and publish your content
            </p>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Simple, Transparent Pricing
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Free Tier */}
          <div className="bg-white p-8 rounded-xl shadow-md border-2 border-gray-200">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Free</h3>
            <div className="mb-4">
              <span className="text-4xl font-bold">$0</span>
              <span className="text-gray-600">/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                3 uploads per month
              </li>
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Up to 50MB file size
              </li>
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                All content formats
              </li>
            </ul>
            <Link
              href="/register"
              className="block w-full text-center px-6 py-3 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 font-medium"
            >
              Get Started
            </Link>
          </div>

          {/* Pro Tier */}
          <div className="bg-white p-8 rounded-xl shadow-md border-2 border-primary-600">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-2xl font-bold text-gray-900">Pro</h3>
              <span className="px-3 py-1 bg-primary-100 text-primary-700 text-xs font-semibold rounded-full">
                POPULAR
              </span>
            </div>
            <div className="mb-4">
              <span className="text-4xl font-bold">$19</span>
              <span className="text-gray-600">/month</span>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Unlimited uploads
              </li>
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Up to 200MB file size
              </li>
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Priority processing
              </li>
              <li className="flex items-center text-gray-700">
                <svg className="h-5 w-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                API access
              </li>
            </ul>
            <Link
              href="/register"
              className="block w-full text-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium"
            >
              Upgrade to Pro
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <p className="text-gray-400">
              © 2025 AudioRepurpose. Built with Next.js, FastAPI, and OpenAI.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
