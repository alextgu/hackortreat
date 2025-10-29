# 🚀 Quick Start Guide

## Start Development Servers

### Option 1: Run Both (Frontend + Backend)

**Terminal 1 - Backend API:**
```bash
npm run dev:backend
# Flask API runs on http://localhost:5001
```

**Terminal 2 - Frontend:**
```bash
npm run dev
# React app runs on http://localhost:8080
```

### Option 2: Individual Commands

**Frontend only:**
```bash
cd frontend
npm run dev
```

**Backend only:**
```bash
source venv/bin/activate
python backend/app.py
```

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:8080 | Main React app |
| **Backend API** | http://localhost:5001 | Flask REST API |
| **API Test Page** | http://localhost:8080/test-api.html | Test API endpoints |

---

## 📋 What to Do Next

1. **Start both servers** (see commands above)
2. **Open** http://localhost:8080 in your browser
3. **Test the API** at http://localhost:8080/test-api.html

---

## 🛠️ First Time Setup

Only need to do this once:

```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ..
source venv/bin/activate
pip install -r backend/requirements.txt
```

---

## 🎯 Port Reference

- **8080** - Frontend (Vite/React)
- **5001** - Backend API (Flask)
- **3000** - Video server (Node.js) - if needed

Port 5000 is avoided because macOS uses it for AirPlay.

---

## 📚 Documentation

- **API Guide**: `backend/API_GUIDE.md`
- **Quick Start**: `QUICKSTART.md`
- **This File**: Basic commands to get started

---

## ✅ You're Ready!

Just run:
```bash
# Terminal 1
npm run dev:backend

# Terminal 2 (new terminal)
npm run dev
```

Then open http://localhost:8080 🎉

