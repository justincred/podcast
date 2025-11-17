'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { FileAudio, LogOut, Upload, Loader2 } from 'lucide-react';
import { getCurrentUser, uploadAudio, listJobs, pollJobStatus, logout } from '@/lib/api';
import type { User, Job, APIError } from '@/types';
import UploadForm from '@/components/UploadForm';
import JobCard from '@/components/JobCard';
import JobResults from '@/components/JobResults';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  // Load user and jobs on mount
  useEffect(() => {
    loadUserAndJobs();
  }, []);

  const loadUserAndJobs = async () => {
    try {
      const [userData, jobsData] = await Promise.all([
        getCurrentUser(),
        listJobs(20, 0),
      ]);

      setUser(userData);
      setJobs(jobsData.jobs);
    } catch (err) {
      const apiError = err as APIError;
      if (apiError.status === 401) {
        // Not authenticated, redirect to login
        router.push('/login');
      } else {
        setError('Failed to load data');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpload = async (file: File, title?: string) => {
    try {
      const newJob = await uploadAudio(file, title);

      // Add to jobs list
      setJobs([newJob, ...jobs]);
      setSelectedJob(newJob);

      // Start polling for updates
      pollJobStatus(newJob.job_id, (updatedJob) => {
        // Update job in list
        setJobs((prevJobs) =>
          prevJobs.map((j) => (j.job_id === updatedJob.job_id ? updatedJob : j))
        );

        // Update selected job if it's the one being updated
        if (selectedJob?.job_id === updatedJob.job_id) {
          setSelectedJob(updatedJob);
        }
      }).then((completedJob) => {
        // Final update when completed
        setJobs((prevJobs) =>
          prevJobs.map((j) => (j.job_id === completedJob.job_id ? completedJob : j))
        );
        if (selectedJob?.job_id === completedJob.job_id) {
          setSelectedJob(completedJob);
        }
      });
    } catch (err) {
      const apiError = err as APIError;
      alert(apiError.detail || 'Upload failed');
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <FileAudio className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-2xl font-bold text-gray-900">
                AudioRepurpose
              </span>
            </div>

            <div className="flex items-center space-x-6">
              {user && (
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">
                    {user.email}
                  </p>
                  <p className="text-xs text-gray-500">
                    {user.tier.toUpperCase()} • {user.uploads_remaining} uploads left
                  </p>
                </div>
              )}
              <button
                onClick={handleLogout}
                className="flex items-center text-gray-700 hover:text-gray-900"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Upload & Jobs List */}
          <div className="lg:col-span-1 space-y-6">
            {/* Upload Form */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">
                Upload Audio
              </h2>
              <UploadForm onUpload={handleUpload} user={user} />
            </div>

            {/* Jobs List */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">
                Your Jobs ({jobs.length})
              </h2>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {jobs.length === 0 ? (
                  <p className="text-gray-500 text-sm text-center py-8">
                    No jobs yet. Upload an audio file to get started!
                  </p>
                ) : (
                  jobs.map((job) => (
                    <JobCard
                      key={job.job_id}
                      job={job}
                      isSelected={selectedJob?.job_id === job.job_id}
                      onClick={() => setSelectedJob(job)}
                    />
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Right Column: Job Results */}
          <div className="lg:col-span-2">
            {selectedJob ? (
              <JobResults job={selectedJob} />
            ) : (
              <div className="bg-white rounded-lg shadow-sm p-12 text-center">
                <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No job selected
                </h3>
                <p className="text-gray-500">
                  Upload an audio file or select a job to view results
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
