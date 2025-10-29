const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../.env') });
const express = require('express');
const multer = require('multer');
const fs = require('fs');
const VideoAnalyzer = require('./video-analyzer.cjs');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize Gemini video analyzer
let videoAnalyzer = null;
if (process.env.GEMINI_API_KEY && process.env.GEMINI_API_KEY !== 'YOUR_API_KEY_HERE') {
    try {
        videoAnalyzer = new VideoAnalyzer(process.env.GEMINI_API_KEY);
        console.log('✅ Gemini AI enabled for video analysis');
    } catch (error) {
        console.warn('⚠️  Failed to initialize Gemini:', error.message);
    }
} else {
    console.warn('⚠️  Gemini API key not set. Video analysis disabled.');
    console.warn('   Add GEMINI_API_KEY to .env file to enable AI analysis.');
}

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, '../../uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadsDir);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, 'video-' + uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 500 * 1024 * 1024 // 500MB limit
    }
});

// Serve static files (frontend directory)
app.use(express.static(path.join(__dirname, '../../frontend')));

// Upload endpoint
app.post('/upload', upload.single('video'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No video file uploaded' });
    }

    console.log('Video uploaded:', req.file.filename);
    console.log('Size:', (req.file.size / 1024 / 1024).toFixed(2), 'MB');
    console.log('Saved to:', req.file.path);

    // Start video analysis in the background (don't block the response)
    let analysisPromise = null;
    if (videoAnalyzer) {
        console.log('🤖 Starting AI analysis...');
        analysisPromise = videoAnalyzer.analyzeAndSave(req.file.path)
            .then(result => {
                console.log('✅ Video analysis complete');
                return result;
            })
            .catch(error => {
                console.error('❌ Video analysis failed:', error.message);
                return null;
            });
    }

    res.json({
        success: true,
        filename: req.file.filename,
        size: req.file.size,
        path: req.file.path,
        analysis_pending: videoAnalyzer !== null
    });

    // Wait for analysis to complete (but response already sent)
    if (analysisPromise) {
        await analysisPromise;
    }
});

// Get analysis for a specific video
app.get('/analysis/:filename', (req, res) => {
    const videoFilename = req.params.filename;
    const analysisFilename = videoFilename.replace(/\.[^.]+$/, '-analysis.json');
    const analysisPath = path.join(uploadsDir, analysisFilename);

    if (!fs.existsSync(analysisPath)) {
        return res.status(404).json({ 
            error: 'Analysis not found',
            message: 'Video analysis may still be processing or AI is not enabled'
        });
    }

    try {
        const analysis = JSON.parse(fs.readFileSync(analysisPath, 'utf8'));
        res.json(analysis);
    } catch (error) {
        res.status(500).json({ error: 'Failed to read analysis file' });
    }
});

// Manually trigger analysis for an existing video
app.post('/analyze/:filename', async (req, res) => {
    if (!videoAnalyzer) {
        return res.status(503).json({ 
            error: 'AI analysis not available',
            message: 'Gemini API key not configured'
        });
    }

    const videoFilename = req.params.filename;
    const videoPath = path.join(uploadsDir, videoFilename);

    if (!fs.existsSync(videoPath)) {
        return res.status(404).json({ error: 'Video not found' });
    }

    try {
        console.log('🤖 Manual analysis requested for:', videoFilename);
        const result = await videoAnalyzer.analyzeAndSave(videoPath);
        res.json({
            success: true,
            analysis: result.analysis,
            analysis_file: path.basename(result.outputPath)
        });
    } catch (error) {
        console.error('❌ Analysis failed:', error.message);
        res.status(500).json({ 
            error: 'Analysis failed',
            message: error.message
        });
    }
});

// List uploaded videos
app.get('/videos', (req, res) => {
    fs.readdir(uploadsDir, (err, files) => {
        if (err) {
            return res.status(500).json({ error: 'Could not list videos' });
        }

        const videos = files
            .filter(file => file.endsWith('.webm') || file.endsWith('.mp4'))
            .map(file => {
                const filePath = path.join(uploadsDir, file);
                const stats = fs.statSync(filePath);
                return {
                    filename: file,
                    size: stats.size,
                    created: stats.birthtime
                };
            });

        res.json(videos);
    });
});

// Serve uploaded videos
app.use('/uploads', express.static(uploadsDir));

// Get local network IP address
function getLocalIP() {
    const { networkInterfaces } = require('os');
    const nets = networkInterfaces();
    
    for (const name of Object.keys(nets)) {
        for (const net of nets[name]) {
            // Skip internal and non-IPv4 addresses
            if (net.family === 'IPv4' && !net.internal) {
                return net.address;
            }
        }
    }
    return 'localhost';
}

app.listen(PORT, '0.0.0.0', () => {
    const localIP = getLocalIP();
    console.log('\n🚀 Phone Camera Recorder Server Started!\n');
    console.log('📱 Access from your phone:');
    console.log(`   http://${localIP}:${PORT}`);
    console.log('\n💻 Access from this computer:');
    console.log(`   http://localhost:${PORT}`);
    console.log('\n📁 Videos will be saved to:', uploadsDir);
    console.log('\n⚠️  Make sure your phone is on the same WiFi network!\n');
});

