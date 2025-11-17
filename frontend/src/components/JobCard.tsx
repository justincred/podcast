'use client';

import { FileAudio, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { cn } from '@/lib/utils';
import type { Job } from '@/types';

interface JobCardProps {
  job: Job;
  isSelected: boolean;
  onClick: () => void;
}

export default function JobCard({ job, isSelected, onClick }: JobCardProps) {
  const statusConfig = {
    pending: {
      icon: Loader2,
      iconClass: 'text-yellow-500 animate-spin',
      bgClass: 'bg-yellow-50',
      textClass: 'text-yellow-700',
      label: 'Pending',
    },
    processing: {
      icon: Loader2,
      iconClass: 'text-blue-500 animate-spin',
      bgClass: 'bg-blue-50',
      textClass: 'text-blue-700',
      label: 'Processing',
    },
    completed: {
      icon: CheckCircle,
      iconClass: 'text-green-500',
      bgClass: 'bg-green-50',
      textClass: 'text-green-700',
      label: 'Completed',
    },
    failed: {
      icon: XCircle,
      iconClass: 'text-red-500',
      bgClass: 'bg-red-50',
      textClass: 'text-red-700',
      label: 'Failed',
    },
  };

  const config = statusConfig[job.status];
  const StatusIcon = config.icon;

  return (
    <button
      onClick={onClick}
      className={cn(
        'w-full text-left p-4 rounded-lg border-2 transition-all',
        isSelected
          ? 'border-primary-500 bg-primary-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      )}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center space-x-2 flex-1 min-w-0">
          <FileAudio className="h-5 w-5 text-gray-400 flex-shrink-0" />
          <div className="min-w-0 flex-1">
            <p className="font-medium text-gray-900 truncate text-sm">
              {job.title || job.file_name}
            </p>
            {job.title && (
              <p className="text-xs text-gray-500 truncate">{job.file_name}</p>
            )}
          </div>
        </div>
        <StatusIcon className={cn('h-5 w-5 flex-shrink-0', config.iconClass)} />
      </div>

      <div className="flex items-center justify-between">
        <span className={cn('text-xs px-2 py-1 rounded-full', config.bgClass, config.textClass)}>
          {config.label}
          {job.status === 'processing' && ` ${job.progress}%`}
        </span>
        <span className="text-xs text-gray-500">
          {formatDistanceToNow(new Date(job.created_at), { addSuffix: true })}
        </span>
      </div>

      {job.status === 'processing' && (
        <div className="mt-2 w-full bg-gray-200 rounded-full h-1.5">
          <div
            className="bg-primary-600 h-1.5 rounded-full transition-all duration-300"
            style={{ width: `${job.progress}%` }}
          />
        </div>
      )}
    </button>
  );
}
