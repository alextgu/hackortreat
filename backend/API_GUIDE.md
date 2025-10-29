# Backend API Guide

## Overview
Unified Flask backend that handles:
- Video upload and analysis (via Node.js)
- LinkedIn post generation
- Pattern extraction from datasets
- Content style management

## Setup

### 1. Install Dependencies
```bash
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. Start the Server
```bash
python app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "video_upload": true,
    "content_generation": true,
    "pattern_extraction": true
  }
}
```

---

### 2. Upload Video
```http
POST /api/upload-video
Content-Type: multipart/form-data
```

**Parameters:**
- `video` (file): Video file (mp4, mov, avi, mkv, webm)
- `context` (text, optional): Context about the video

**Response:**
```json
{
  "success": true,
  "filename": "video-1234567890-example.mp4",
  "filepath": "/path/to/uploads/video.mp4",
  "context": "User provided context",
  "analysis": {
    "description": "AI-generated video description",
    "key_moments": ["moment1", "moment2"],
    "transcript": "..."
  },
  "message": "Video uploaded and analyzed successfully"
}
```

---

### 3. Generate LinkedIn Post
```http
POST /api/generate-post
Content-Type: application/json
```

**Request Body:**
```json
{
  "context": "Your post context or topic",
  "style": "professional",
  "video_analysis": {}
}
```

**Styles:**
- `professional` - Formal business tone
- `inspirational` - Motivational content
- `controversial` - Thought-provoking
- `listicle` - List-based format
- `formal` - Very professional

**Response:**
```json
{
  "success": true,
  "post": {
    "hook": "Opening line",
    "body": "Main content",
    "call_to_action": "CTA text",
    "hashtags": ["#Growth", "#Leadership"],
    "full_text": "Complete post text"
  },
  "style": "professional"
}
```

---

### 4. Extract Patterns from Dataset
```http
POST /api/extract-patterns
Content-Type: application/json
```

**Request Body:**
```json
{
  "dataset_name": "boardy"
}
```

**Response:**
```json
{
  "success": true,
  "patterns": {
    "opening_patterns": [...],
    "top_sentence_starters": [...],
    "common_phrases": [...],
    "formatting_patterns": [...],
    "tone_indicators": [...]
  },
  "message": "Patterns extracted successfully"
}
```

---

### 5. Get Current Patterns
```http
GET /api/patterns
```

**Response:**
```json
{
  "source_file": "data/raw/boardy.json",
  "total_posts": 7,
  "writing_style": {
    "opening_patterns": [...],
    "top_sentence_starters": [...],
    "common_phrases": [...],
    "formatting_patterns": [...],
    "tone_indicators": [...]
  },
  "structure": {
    "avg_length": 954.4,
    "avg_sentences": 14.6,
    "avg_paragraphs": 9.6
  },
  "vocabulary": [...],
  "emoji_usage": {...}
}
```

---

### 6. List Available Datasets
```http
GET /api/datasets
```

**Response:**
```json
{
  "datasets": ["boardy", "professional", "cluely"],
  "count": 3
}
```

---

### 7. Access Uploaded Videos
```http
GET /uploads/<filename>
```

Serves the uploaded video file for preview.

---

## Testing

### Using the Test Page
1. Open `frontend/test-api.html` in your browser
2. Test each endpoint through the UI

### Using cURL

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Upload Video:**
```bash
curl -X POST http://localhost:5000/api/upload-video \
  -F "video=@/path/to/video.mp4" \
  -F "context=Test video upload"
```

**Generate Post:**
```bash
curl -X POST http://localhost:5000/api/generate-post \
  -H "Content-Type: application/json" \
  -d '{"context": "Building a successful startup", "style": "professional"}'
```

**Extract Patterns:**
```bash
curl -X POST http://localhost:5000/api/extract-patterns \
  -H "Content-Type: application/json" \
  -d '{"dataset_name": "boardy"}'
```

---

## File Structure
```
backend/
├── app.py                 # Main Flask application
├── extractpatterns.py     # Pattern extraction script
├── generator.py           # Post generation logic
├── requirements.txt       # Python dependencies
├── video/
│   ├── server.cjs        # Node.js video server
│   └── video-analyzer.cjs # Gemini video analysis
└── content/
    ├── extractpatterns.py
    ├── generator.py
    └── server.py

data/
├── raw/                   # Input datasets
│   └── boardy.json
└── processed/             # Extracted patterns
    └── patterns.json

uploads/                   # Uploaded videos
```

---

## Error Handling

All endpoints return errors in this format:
```json
{
  "error": "Description of what went wrong"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad request (missing required fields)
- `404` - Resource not found
- `500` - Server error

---

## Next Steps

1. **Integrate Gemini API** for actual content generation in `generate_linkedin_post()`
2. **Add authentication** for production use
3. **Implement rate limiting** to prevent abuse
4. **Add file size validation** before processing
5. **Store analysis results** in a database
6. **Add more sophisticated prompt engineering** for better post generation

---

## Development

Run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

Run in production mode (with Gunicorn):
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

