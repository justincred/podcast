'use client';

import { useState, useRef } from 'react';
import { Upload, FileAudio } from 'lucide-react';
import { formatFileSize } from '@/lib/utils';
import type { User } from '@/types';

interface UploadFormProps {
  onUpload: (file: File, title?: string) => Promise<void>;
  user: User | null;
}

export default function UploadForm({ onUpload, user }: UploadFormProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedExtensions = ['mp3', 'wav', 'm4a', 'ogg', 'flac'];
  const maxFileSizeMB = user?.tier === 'pro' ? 200 : 50;
  const maxFileSizeBytes = maxFileSizeMB * 1024 * 1024;

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError('');

    // Validate file type
    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!extension || !allowedExtensions.includes(extension)) {
      setError(`Invalid file type. Allowed: ${allowedExtensions.join(', ')}`);
      return;
    }

    // Validate file size
    if (file.size > maxFileSizeBytes) {
      setError(`File too large. Maximum size: ${maxFileSizeMB}MB for ${user?.tier} tier`);
      return;
    }

    setSelectedFile(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedFile) {
      setError('Please select a file');
      return;
    }

    if (user && user.uploads_remaining <= 0) {
      setError('Monthly upload limit reached. Upgrade to Pro for unlimited uploads.');
      return;
    }

    setIsUploading(true);
    setError('');

    try {
      await onUpload(selectedFile, title || undefined);

      // Reset form
      setSelectedFile(null);
      setTitle('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      setError('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
          {error}
        </div>
      )}

      {/* File Input */}
      <div>
        <label
          htmlFor="file-upload"
          className="block w-full border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-primary-500 transition-colors"
        >
          <input
            ref={fileInputRef}
            id="file-upload"
            type="file"
            accept=".mp3,.wav,.m4a,.ogg,.flac"
            onChange={handleFileSelect}
            className="sr-only"
          />
          <FileAudio className="h-12 w-12 text-gray-400 mx-auto mb-2" />
          <p className="text-sm text-gray-600">
            {selectedFile ? (
              <>
                <span className="font-medium text-gray-900">{selectedFile.name}</span>
                <br />
                <span className="text-xs text-gray-500">
                  {formatFileSize(selectedFile.size)}
                </span>
              </>
            ) : (
              <>
                Click to upload or drag and drop
                <br />
                <span className="text-xs text-gray-500">
                  MP3, WAV, M4A, OGG, FLAC (max {maxFileSizeMB}MB)
                </span>
              </>
            )}
          </p>
        </label>
      </div>

      {/* Title Input */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
          Title (Optional)
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="e.g., Episode 42: How to Build SaaS"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={!selectedFile || isUploading || (user?.uploads_remaining || 0) <= 0}
        className="w-full flex items-center justify-center px-4 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isUploading ? (
          <>
            <Upload className="h-5 w-5 mr-2 animate-spin" />
            Processing...
          </>
        ) : (
          <>
            <Upload className="h-5 w-5 mr-2" />
            Upload & Process
          </>
        )}
      </button>

      {user && (
        <p className="text-xs text-gray-500 text-center">
          {user.uploads_remaining} upload{user.uploads_remaining !== 1 ? 's' : ''} remaining this month
        </p>
      )}
    </form>
  );
}
