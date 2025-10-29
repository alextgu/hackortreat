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
  const response = await fetch(`${CONTENT_API_URL}/api/generate-post`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      context: request.context || 'LinkedIn post',
      style: request.postType,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Failed to generate post' }));
    throw new Error(error.error || 'Failed to generate post');
  }

  const data = await response.json();
  return {
    post: data.post?.full_text || data.post || 'Post generated!',
    style: data.style || request.postType,
  };
}

/**
 * Upload a video to the Flask API (which handles video analysis)
 */
export async function uploadVideo(file: File): Promise<VideoUploadResponse> {
  const formData = new FormData();
  formData.append('video', file);
  formData.append('context', 'Video for LinkedIn post generation');

  const response = await fetch(`${CONTENT_API_URL}/api/upload-video`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Failed to upload video' }));
    throw new Error(error.error || 'Failed to upload video');
  }

  const data = await response.json();
  return {
    success: data.success || true,
    filename: data.filename,
    size: file.size,
    path: data.filepath || '',
    analysis_pending: !!data.analysis,
  };
}

/**
 * Get video analysis results
 */
export async function getVideoAnalysis(filename: string): Promise<VideoAnalysis> {
  // For now, return mock data since analysis is embedded in upload response
  // TODO: Implement proper analysis retrieval endpoint if needed
  return {
    outfit: {
      description: "Analysis in progress...",
      items: [],
      colors: []
    },
    activity: {
      description: "Analyzing video content...",
      actions: [],
      intensity: "medium"
    },
    background: {
      description: "Processing background...",
      location_type: "unknown",
      environment: "unknown",
      lighting: "natural"
    },
    summary: "Video analysis is being processed. This may take a moment."
  };
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

