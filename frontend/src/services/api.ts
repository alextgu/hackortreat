// API service for connecting to local Flask and Node.js backends

const CONTENT_API_URL = import.meta.env.VITE_CONTENT_API_URL || 'http://localhost:5001';
const VIDEO_API_URL = import.meta.env.VITE_VIDEO_API_URL || 'http://localhost:3000';

export interface GeneratePostRequest {
  postType: string;
  context: string;
}

export interface GeneratePostResponse {
  post: string;
  style: string;
}

export interface VideoUploadResponse {
  success: boolean;
  filename: string;
  size: number;
  path: string;
  analysis_pending: boolean;
}

export interface VideoAnalysis {
  outfit: {
    description: string;
    items: string[];
    colors: string[];
  };
  activity: {
    description: string;
    actions: string[];
    intensity: string;
  };
  background: {
    description: string;
    location_type: string;
    environment: string;
    lighting: string;
  };
  summary: string;
  analyzed_at?: string;
  video_file?: string;
  video_size_mb?: number;
}

/**
 * Generate a LinkedIn post using the Flask content API
 */
export async function generatePost(request: GeneratePostRequest): Promise<GeneratePostResponse> {
  const response = await fetch(`${CONTENT_API_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      topic: request.context || 'LinkedIn',
      details: request.context,
      style: request.postType,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Failed to generate post' }));
    throw new Error(error.error || 'Failed to generate post');
  }

  return response.json();
}

/**
 * Upload a video to the Node.js video server
 */
export async function uploadVideo(file: File): Promise<VideoUploadResponse> {
  const formData = new FormData();
  formData.append('video', file);

  const response = await fetch(`${VIDEO_API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Failed to upload video' }));
    throw new Error(error.error || 'Failed to upload video');
  }

  return response.json();
}

/**
 * Get video analysis results
 */
export async function getVideoAnalysis(filename: string): Promise<VideoAnalysis> {
  const response = await fetch(`${VIDEO_API_URL}/analysis/${filename}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Analysis not ready yet. Please wait...');
    }
    const error = await response.json().catch(() => ({ error: 'Failed to get analysis' }));
    throw new Error(error.error || 'Failed to get analysis');
  }

  return response.json();
}

/**
 * Health check for content API
 */
export async function checkContentAPIHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${CONTENT_API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Get list of uploaded videos
 */
export async function getVideos(): Promise<any[]> {
  const response = await fetch(`${VIDEO_API_URL}/videos`);

  if (!response.ok) {
    throw new Error('Failed to get videos');
  }

  return response.json();
}

