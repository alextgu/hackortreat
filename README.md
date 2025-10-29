# 📹 HackOrTreat - AI-Powered LinkedIn Post Generator

Generate authentic LinkedIn posts from videos using AI analysis. Record videos on your phone, analyze them with Gemini AI, and create posts in different styles.

## 🚀 Quick Start

### Prerequisites

- Node.js (v18+)
- Python 3.8+
- Gemini API Key ([Get one free](https://aistudio.google.com/app/apikey))

### Setup

1. **Install dependencies:**
```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install Python dependencies
pip install -r backend/requirements.txt
```

2. **Configure API Key:**
```bash
# Create .env file in project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

3. **Start all servers:**
```bash
npm start
```

This starts:
- 📹 Video Server (Port 3000) - Phone video upload & AI analysis
- 🐍 Flask API (Port 5001) - LinkedIn post generation
- ⚛️  Frontend (Port 8080) - Web interface

## 📱 How It Works

### 1. Record Video
- Open `http://[your-local-ip]:3000` on your phone
- Record or select a video
- Upload for AI analysis

### 2. AI Analysis
Gemini AI automatically extracts:
- **Outfit**: Clothing, colors, style
- **Activity**: Actions, what's happening
- **Background**: Location, environment, lighting

### 3. Generate Post
- Open `http://localhost:8080`
- Choose post style (Performative, Cluely, Boardy, Serious)
- Add optional context
- Generate your LinkedIn post!

## 🎯 Post Styles

- **Performative**: Humble-brag corporate speak
- **Cluely**: Controversial hot takes
- **Boardy**: Relatable personal stories
- **Serious**: Corporate jargon heavy

## 📁 Project Structure

```
hackortreat/
├── backend/
│   ├── video/
│   │   ├── server.cjs           # Video upload & analysis server
│   │   ├── video-analyzer.cjs   # Gemini AI analyzer
│   │   └── index.html           # Phone recording UI
│   ├── content/
│   │   └── generator.py         # Post generation logic
│   ├── app.py                   # Flask API
│   └── requirements.txt
├── frontend/
│   └── src/                     # React frontend
├── data/raw/                    # Post style templates
├── uploads/                     # Uploaded videos & analysis
└── package.json
```

## 🛠️ Individual Commands

**Video server only:**
```bash
npm run start:video
```

**Flask API only:**
```bash
npm run start:api
```

**Frontend only:**
```bash
npm run dev
```

**Stop all servers:**
```bash
./stop-all.sh
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free API key at: https://aistudio.google.com/app/apikey

## 📊 API Endpoints

### Video Server (Port 3000)

- `POST /upload` - Upload video for analysis
- `GET /analysis/:filename` - Get analysis results
- `GET /videos` - List uploaded videos

### Flask API (Port 5001)

- `GET /health` - Health check
- `POST /api/generate-post` - Generate LinkedIn post
- `GET /api/patterns` - Get writing patterns
- `GET /api/datasets` - List available post styles

## 🐛 Troubleshooting

**Camera not working on phone:**
- Camera access requires HTTPS or file selection
- Use "Select Video from Camera Roll" button

**No analysis file created:**
- Check GEMINI_API_KEY is set in .env
- Verify API key is valid
- Check video size < 100MB

**Port already in use:**
```bash
./stop-all.sh
npm start
```

## 📝 License

MIT

## 🤝 Contributing

Pull requests welcome! Please ensure all tests pass and follow the existing code style.

