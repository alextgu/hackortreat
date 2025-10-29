# 🎥 HackOrTreat - AI-Powered Video Recorder & Content Generator

A unified platform combining:
- 📹 **Wireless iPhone Video Recording** with automatic upload
- 🤖 **AI Video Analysis** using Google Gemini (outfit, activity, background)
- ✍️ **LinkedIn Content Generator** (from teammate's contribution)

---

## 📁 Project Structure

```
hackortreat/
├── frontend/                    # Web interface
│   └── index.html              # Video recording UI
├── backend/
│   ├── video/                  # Video recording & AI analysis
│   │   ├── server.js           # Node.js server (video upload)
│   │   └── video-analyzer.js   # Gemini AI video analysis
│   ├── content/                # LinkedIn content generation
│   │   ├── server.py           # Flask server (content API)
│   │   ├── generator.py        # Post generation logic
│   │   └── extractpatterns.py # Pattern extraction
│   └── requirements.txt        # Python dependencies
├── data/                       # Training data for content gen
│   ├── professional.json
│   └── processed/
│       └── patterns.json
├── uploads/                    # Uploaded videos & analysis
├── .env                        # Environment variables (API keys)
├── .gitignore                  # Git ignore rules
├── package.json                # Node.js dependencies
├── test-analyzer.js            # Test script for video AI
├── GEMINI_SETUP.md            # Gemini API setup guide
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

#### Node.js (Video Recording System)
```bash
npm install
```

#### Python (Content Generator)
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_key_here

# Server Ports
PORT=3000
FLASK_PORT=5000
```

**Get your Gemini API key:** https://makersuite.google.com/app/apikey

### 3. Start the Servers

#### Option A: Video Recording Server (Node.js)
```bash
npm start
# or
npm run start:video
```

Access at: `http://192.168.1.XXX:3000` (shown in console)

#### Option B: Content Generator Server (Flask)
```bash
npm run start:content
```

Access at: `http://localhost:5000`

#### Option C: Run Both (in separate terminals)
```bash
# Terminal 1
npm run start:video

# Terminal 2
npm run start:content
```

---

## 📱 Feature 1: Video Recording with AI Analysis

### How It Works

1. **Open on iPhone** - Navigate to server URL in Safari
2. **Tap "Record Video"** - Native iOS Camera app opens
3. **Record** - Capture your video (3-60 seconds)
4. **Tap "Use Video"** - Returns to browser with video
5. **Auto-Upload** - Video uploads to your laptop
6. **AI Analysis** - Gemini automatically analyzes:
   - 👔 **Outfit** (clothing, colors, style)
   - 🎬 **Activity** (actions, movements)
   - 🏞️ **Background** (location, lighting, environment)

### Technical Details

- **Frontend:** HTML5 Media Capture API (no HTTPS needed!)
- **Backend:** Node.js + Express + Multer
- **AI:** Google Gemini 1.5 Flash
- **Storage:** Local filesystem (`uploads/`)
- **Analysis Format:** JSON files (`*-analysis.json`)

### Example Analysis Output

```json
{
  "outfit": {
    "description": "Person wearing blue t-shirt and jeans",
    "items": ["t-shirt", "jeans"],
    "colors": ["blue", "dark blue"]
  },
  "activity": {
    "description": "Walking and waving at camera",
    "actions": ["walking", "waving"],
    "intensity": "medium"
  },
  "background": {
    "description": "Indoor living room with natural lighting",
    "location_type": "indoor",
    "lighting": "natural daylight"
  },
  "summary": "Person in casual attire walking indoors"
}
```

### API Endpoints (Video Server - Port 3000)

```
GET  /                          - Serve video recording UI
POST /upload                    - Upload video file
GET  /analysis/:filename        - Get AI analysis for video
POST /analyze/:filename         - Manually trigger analysis
GET  /videos                    - List all uploaded videos
```

---

## ✍️ Feature 2: LinkedIn Content Generator

### How It Works

Generate performative LinkedIn posts based on extracted patterns from professional posts.

### API Endpoints (Content Server - Port 5000)

```
GET  /health                    - Health check
POST /generate                  - Generate LinkedIn post

Request Body:
{
  "topic": "AI in healthcare",
  "details": "Improved diagnostics",
  "style": "professional"
}

Response:
{
  "post": "Generated LinkedIn post...",
  "style": "professional"
}
```

### Technical Details

- **Framework:** Flask + CORS
- **NLP:** spaCy for text analysis
- **Data:** Pattern extraction from professional posts
- **Generation:** Template-based with AI enhancement

---

## 🔧 Development

### File Structure Explained

#### Frontend (`frontend/`)
- **index.html** - Single-page app for video recording
  - Camera trigger
  - Video preview
  - Upload progress
  - AI analysis display

#### Backend - Video (`backend/video/`)
- **server.js** - Express server
  - Static file serving
  - Video upload handling
  - Gemini API integration
  - Analysis storage
- **video-analyzer.js** - Gemini video analysis module
  - Video to base64 conversion
  - Prompt engineering
  - JSON parsing
  - File management

#### Backend - Content (`backend/content/`)
- **server.py** - Flask API server
- **generator.py** - Post generation logic
- **extractpatterns.py** - Pattern analysis
  - Opening patterns
  - Emoji usage
  - Hashtag analysis
  - Structure metrics

#### Data (`data/`)
- Training data for content generation
- Processed patterns

---

## 🧪 Testing

### Test Video AI Analysis

```bash
# Analyze an existing video
npm run test-ai uploads/video-123.MOV
```

Output:
```
📹 Video Analysis Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👔 OUTFIT: Blue t-shirt and jeans...
🎬 ACTIVITY: Walking and waving...
🏞️ BACKGROUND: Indoor living room...
📝 SUMMARY: Casual indoor scene...
```

### Test Content Generator

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI automation",
    "details": "Workflow optimization",
    "style": "professional"
  }'
```

---

## 📚 Documentation

- **GEMINI_SETUP.md** - Detailed Gemini API configuration
- **QUICK_START.md** - Quick reference for video recording
- This README - Complete project overview

---

## 🔐 Security & Privacy

### Environment Variables
- Never commit `.env` file
- Use `.env.template` for reference
- Regenerate keys if exposed

### Video Storage
- Videos stored locally in `uploads/`
- Not uploaded to cloud by default
- Analysis files contain no video data (only metadata)

### Network Security
- Video server: Local WiFi only by default
- Content server: localhost by default
- Use HTTPS for production deployment

---

## 🚢 Deployment

### Local Development
Already configured! Just run `npm start`

### Production Deployment

#### Video Server (Heroku/Railway)
```bash
# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here

# Deploy
git push heroku main
```

#### Content Server (Python Anywhere/Heroku)
```bash
# Add Procfile
echo "web: python backend/content/server.py" > Procfile

# Deploy
git push heroku main
```

---

## 💰 Costs & Limits

### Google Gemini API (Free Tier)
- 15 requests/minute
- 1,500 requests/day
- Perfect for development

### Infrastructure
- Local development: **$0**
- Storage: Local disk (free)
- Network: Local WiFi (free)

---

## 🤝 Team Integration

This project combines:
1. **Your work:** Video recording system with AI analysis
2. **Teammate's work:** LinkedIn content generator

Both systems are now unified under one codebase with:
- ✅ Shared `.env` configuration
- ✅ Unified `.gitignore`
- ✅ Organized folder structure
- ✅ Combined documentation

---

## 📊 Use Cases

### Video Analysis Use Cases
- Fashion/outfit analysis
- Activity recognition training data
- Scene understanding datasets
- Real-time event logging
- Behavioral analysis

### Content Generator Use Cases
- LinkedIn post creation
- Content strategy analysis
- Engagement pattern detection
- Professional writing assistance

---

## 🐛 Troubleshooting

### Video Server Issues

**"Cannot access camera"**
- Use Safari on iPhone (not Chrome)
- Refresh the page
- Check WiFi connection

**"Analysis not available"**
- Verify `GEMINI_API_KEY` in `.env`
- Check API quota limits
- Video must be under 100MB

**"Upload failed"**
- Ensure server is running
- Check network connection
- Verify uploads directory exists

### Content Server Issues

**"Module not found"**
```bash
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
```

**"Port already in use"**
```bash
# Change port in .env
FLASK_PORT=5001
```

---

## 🎯 Roadmap

### Planned Features
- [ ] Real-time video streaming
- [ ] Multi-user support
- [ ] Cloud storage integration (S3/GCS)
- [ ] Video editing capabilities
- [ ] Batch video analysis
- [ ] Integration between video analysis and content gen
- [ ] Dashboard for analytics
- [ ] Mobile app (React Native)

---

## 📝 Contributing

This is a team project. Both video and content features are actively developed.

### Code Style
- **JavaScript:** ES6+, async/await
- **Python:** PEP 8 compliance
- **Comments:** Clear and concise

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes
git add .
git commit -m "feat: your feature description"

# Push and create PR
git push origin feature/your-feature
```

---

## 📄 License

MIT License - Free to use and modify

---

## 🎉 Acknowledgments

- Google Gemini AI for video analysis
- W3C HTML Media Capture specification
- Flask and Express communities
- Team collaboration on this project!

---

## 📞 Support

For issues or questions:
1. Check documentation (GEMINI_SETUP.md, QUICK_START.md)
2. Review troubleshooting section above
3. Check server logs for errors

---

**Built with ❤️ for HackOrTreat**
