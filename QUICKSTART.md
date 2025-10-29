# 🚀 Quick Start Guide

## What's Been Built

A full-stack Flask API that connects your frontend to:
- **Video Upload & Analysis** (using Gemini AI via Node.js)
- **LinkedIn Post Generation** (using extracted patterns)
- **Pattern Extraction** from datasets
- **Style-based content generation**

---

## 🎯 Start the Backend Server

### Option 1: Using the startup script
```bash
./start-server.sh
```

### Option 2: Manual start
```bash
source venv/bin/activate
python backend/app.py
```

The server will run on **http://localhost:5000**

---

## 🧪 Test the API

### Option 1: Use the Test Page
1. Start the Flask server
2. Open `frontend/test-api.html` in your browser
3. Test each endpoint through the UI

### Option 2: Use cURL
```bash
# Health check
curl http://localhost:5000/health

# Upload video
curl -X POST http://localhost:5000/api/upload-video \
  -F "video=@path/to/video.mp4" \
  -F "context=My video description"

# Generate post
curl -X POST http://localhost:5000/api/generate-post \
  -H "Content-Type: application/json" \
  -d '{"context": "Building a startup", "style": "professional"}'

# Extract patterns
curl -X POST http://localhost:5000/api/extract-patterns \
  -H "Content-Type: application/json" \
  -d '{"dataset_name": "boardy"}'
```

---

## 📁 Project Structure

```
hackortreat/
├── backend/
│   ├── app.py                    # 🆕 Main Flask API server
│   ├── extractpatterns.py        # Pattern extraction
│   ├── generator.py              # Post generation
│   ├── requirements.txt          # Python dependencies
│   ├── video/
│   │   ├── server.cjs           # Node video server
│   │   └── video-analyzer.cjs   # Gemini video analysis
│   └── API_GUIDE.md             # 🆕 Full API documentation
│
├── frontend/
│   ├── test-api.html            # 🆕 API testing interface
│   └── index.html               # Your main app
│
├── data/
│   ├── raw/
│   │   └── boardy.json          # Sample dataset (7 posts)
│   └── processed/
│       └── patterns.json        # Extracted patterns
│
├── uploads/                     # Video uploads go here
├── venv/                        # Python virtual environment
├── start-server.sh              # 🆕 Quick start script
└── .env                         # API keys (create this)
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check API status |
| `/api/upload-video` | POST | Upload & analyze video |
| `/api/generate-post` | POST | Generate LinkedIn post |
| `/api/extract-patterns` | POST | Extract writing patterns |
| `/api/patterns` | GET | Get extracted patterns |
| `/api/datasets` | GET | List available datasets |
| `/uploads/<filename>` | GET | Access uploaded videos |

See `backend/API_GUIDE.md` for detailed documentation.

---

## 🎨 Frontend Integration Example

```javascript
// Upload video
const formData = new FormData();
formData.append('video', videoFile);
formData.append('context', 'My video context');

const response = await fetch('http://localhost:5000/api/upload-video', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log('Video analysis:', result.analysis);

// Generate post
const postResponse = await fetch('http://localhost:5000/api/generate-post', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        context: 'My startup journey',
        style: 'inspirational',
        video_analysis: result.analysis
    })
});

const post = await postResponse.json();
console.log('Generated post:', post.post.full_text);
```

---

## 🔄 Workflow

1. **Upload Video** → Get AI analysis
2. **Extract Patterns** → Learn writing style from dataset
3. **Generate Post** → Create content using patterns + video context
4. **Use Post** → Display in your frontend

---

## 📊 Current Data

- **Dataset**: `boardy.json` with 7 posts
- **Patterns Extracted**: ✅
  - Opening patterns
  - Sentence starters
  - Common phrases
  - Formatting styles
  - Tone indicators

Run pattern extraction:
```bash
curl -X POST http://localhost:5000/api/extract-patterns \
  -H "Content-Type: application/json" \
  -d '{"dataset_name": "boardy"}'
```

---

## 🚧 Next Steps

### To integrate with your frontend:
1. Update your React/Vue/etc. code to call these endpoints
2. Replace the test page with your actual UI
3. Add authentication if needed
4. Deploy to production

### To improve generation:
1. Integrate Gemini API directly in `app.py`
2. Add more sophisticated prompt engineering
3. Use extracted patterns in prompts
4. Fine-tune based on user feedback

---

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Find process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
export FLASK_RUN_PORT=5001
python backend/app.py
```

**Import errors:**
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

**CORS issues:**
Flask-CORS is already configured, but if you have issues:
- Check that the frontend is making requests to the correct URL
- Verify CORS headers in browser dev tools

---

## 📚 Documentation

- **Full API Docs**: `backend/API_GUIDE.md`
- **Pattern Extraction**: `backend/extractpatterns.py`
- **Video Analysis**: `backend/video/video-analyzer.cjs`

---

## ✅ You're All Set!

Your backend API is ready to connect with your frontend. Start the server and open the test page to try it out!

```bash
./start-server.sh
```

Then open: `frontend/test-api.html` in your browser 🎉

